from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import startup, shutdown
from app.routers.auth import router as auth_router
from app.routers.users import router as users_router
from app.routers.posts import router as posts_router
from app.routers.friends import router as friends_router

app = FastAPI(title="Mini-Red-Social")

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def on_startup():
    await startup(app)

@app.on_event("shutdown")
async def on_shutdown():
    await shutdown(app)

@app.get("/")
async def root():
    return {"status": "ok"}

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(posts_router)
app.include_router(friends_router)
