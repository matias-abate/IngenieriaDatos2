# app/repositories/friends_repo.py
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from fastapi import HTTPException

class FriendsRepo:
    """
    Guarda amistades como documentos individuales:
      { _id: ObjectId(), user_id: ObjectId, friend_id: ObjectId }
    Se graba dos veces para hacerla bidireccional (A→B  y  B→A).
    """
    def __init__(self, db: AsyncIOMotorDatabase):
        self.col = db["friends"]

    async def add(self, uid: str, fid: str):
        if uid == fid:
            raise HTTPException(400, "No puedes agregarte a ti mismo")
        u = ObjectId(uid); f = ObjectId(fid)
        # No crear duplicados
        await self.col.update_one(
            {"user_id": u, "friend_id": f},
            {"$setOnInsert": {"user_id": u, "friend_id": f}},
            upsert=True,
        )
        await self.col.update_one(
            {"user_id": f, "friend_id": u},
            {"$setOnInsert": {"user_id": f, "friend_id": u}},
            upsert=True,
        )

    async def remove(self, uid: str, fid: str):
        u = ObjectId(uid); f = ObjectId(fid)
        await self.col.delete_many({"user_id": u, "friend_id": f})
        await self.col.delete_many({"user_id": f, "friend_id": u})

    async def list(self, uid: str):
        u = ObjectId(uid)
        cursor = self.col.find({"user_id": u})
        return [str(d["friend_id"]) async for d in cursor]
