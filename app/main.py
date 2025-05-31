from fastapi import FastAPI
from app.core.database import startup, shutdown
from app.routers.users import router as users_router
from app.routers.posts import router as posts_router
from app.routers.friends import router as friends_router

app = FastAPI(title="Mini-Red-Social")

@app.on_event("startup")
async def on_startup():   await startup(app)

@app.on_event("shutdown")
async def on_shutdown(): await shutdown(app)

@app.get("/")
async def root(): return {"status": "ok"}

app.include_router(users_router)
app.include_router(posts_router)
app.include_router(friends_router)
