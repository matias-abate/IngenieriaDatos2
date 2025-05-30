from fastapi import FastAPI

# importa cada router una sola vez
from app.routers.users import router as users_router
from app.routers.posts import router as posts_router
from app.routers.friends import router as friends_router
from app.routers.messages import router as messages_router

app = FastAPI(title="Mini-Red-Social")


@app.get("/")
async def root():
    """Health-check simple."""
    return {"status": "ok"}


# registra los routers
app.include_router(users_router)
app.include_router(posts_router)
app.include_router(friends_router)
app.include_router(messages_router)
