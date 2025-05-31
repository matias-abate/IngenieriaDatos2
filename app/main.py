from fastapi import FastAPI
from app.core.database import connect_to_mongo, close_mongo_connection
from app.routers.users import router as users_router
# (otros routers desactivados si aún no están listos)

app = FastAPI(title="Mini-Red-Social")

# ─── Startup / Shutdown ───────────────────────────────────────────
@app.on_event("startup")
async def startup() -> None:
    await connect_to_mongo(app)          # ← ESTA línea es clave

@app.on_event("shutdown")
async def shutdown() -> None:
    await close_mongo_connection(app)
# ──────────────────────────────────────────────────────────────────

@app.get("/")
async def root():
    return {"status": "ok"}

app.include_router(users_router)

