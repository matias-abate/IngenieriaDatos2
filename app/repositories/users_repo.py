# app/repositories/users_repo.py
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId

class UsersRepo:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.col = db["users"]

    async def get_by_username(self, username: str) -> dict | None:
        doc = await self.col.find_one({"username": username})
        if doc:
            doc["id"] = str(doc["_id"])
            return doc
        return None

    async def create_user(self, user_data: dict) -> dict:
        """
        Inserta un usuario YA CON hashed_password en la colección.
        user_data debe contener al menos: { "username", "email", "hashed_password" }.
        """
        result = await self.col.insert_one(user_data)
        return {"inserted_id": result.inserted_id}

    # Podrías tener: get(user_id), update(), delete(), etc.
