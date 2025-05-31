from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

client = None
db = None

async def connect_to_mongo(app):
    global client, db
    client = AsyncIOMotorClient(settings.mongo_uri)
    db = client[settings.mongo_db]
    app.state.mongo = db               # ← exacto mismo nombre

async def close_mongo_connection(app):
    client.close()
