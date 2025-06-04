from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from neo4j import AsyncGraphDatabase
from fastapi import FastAPI
from app.core.config import settings

client: AsyncIOMotorClient | None = None
db: AsyncIOMotorDatabase   | None = None
neo_driver = None

async def connect_to_mongo(app: FastAPI):
    global client, db
    client = AsyncIOMotorClient(settings.mongo_uri)
    db = client[settings.mongo_db]
    app.state.mongo = db            # 🚩 usado por repos

async def connect_to_neo4j(app: FastAPI):
    global neo_driver
    neo_driver = AsyncGraphDatabase.driver(
        settings.neo4j_uri,
        auth=(settings.neo4j_user, settings.neo4j_password)
    )
    app.state.neo = neo_driver
  

async def startup(app: FastAPI):
    await connect_to_mongo(app)
    await connect_to_neo4j(app)

async def shutdown(app: FastAPI):
    client.close()
    await neo_driver.close()