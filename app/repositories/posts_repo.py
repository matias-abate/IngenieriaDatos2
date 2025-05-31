# app/repositories/posts_repo.py
from bson import ObjectId
from datetime import datetime
from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.models import Post

class PostsRepo:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.col = db["posts"]

    async def create(self, post: Post) -> Post:
        payload = post.dict(by_alias=True, exclude_none=True)
        payload["created_at"] = datetime.utcnow()
        result = await self.col.insert_one(payload)
        payload["_id"] = result.inserted_id
        return Post(**payload)

    async def get(self, post_id: str) -> Post:
        try:
            key = ObjectId(post_id)
        except Exception:
            raise HTTPException(400, "Invalid ObjectId")

        doc = await self.col.find_one({"_id": key})
        if not doc:
            raise HTTPException(404, "Post not found")
        return Post(**doc)

    async def list(self, skip: int = 0, limit: int = 20) -> list[Post]:
        cursor = (
            self.col.find({})
            .sort("created_at", -1)
            .skip(skip)
            .limit(limit)
        )
        return [Post(**d) async for d in cursor]

    async def delete(self, post_id: str) -> None:
        await self.col.delete_one({"_id": ObjectId(post_id)})
