from bson import ObjectId
from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.models import User

class UsersRepo:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.col = db["users"]

    async def create(self, user: User) -> User:
        payload = user.dict(by_alias=True, exclude_none=True)   # ✅
        result = await self.col.insert_one(payload)             # Mongo crea _id
        payload["_id"] = result.inserted_id
        return User(**payload)

    async def get(self, user_id: str) -> User:
        try:
            key = ObjectId(user_id)
        except Exception:
            raise HTTPException(400, "Invalid ObjectId")        # 400 ≈ bad ID

        doc = await self.col.find_one({"_id": key})
        if not doc:
            raise HTTPException(404, "User not found")
        return User(**doc)

    async def delete(self, user_id: str) -> None:
        await self.col.delete_one({"_id": ObjectId(user_id)})
