# app/repositories/messages_repo.py

from bson import ObjectId
from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase
from datetime import datetime
from app.models import Message

class MessagesRepo:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.col = db["messages"]

    async def send(self, msg: Message) -> Message:
        """
        Inserta un message nuevo en la colección "messages".
        """
        payload = msg.dict(by_alias=True, exclude_none=True)
        payload["sent_at"] = msg.sent_at  # ya lo trae Message
        result = await self.col.insert_one(payload)
        payload["_id"] = result.inserted_id
        return Message(**payload)

    async def get_conversation(
        self,
        user_a: str,
        user_b: str,
        skip: int = 0,
        limit: int = 50
    ) -> list[Message]:
        """
        Devuelve los mensajes entre user_a y user_b (bidireccional),
        ordenados por "sent_at" ascendente (histórico).
        """
        try:
            oa = ObjectId(user_a)
            ob = ObjectId(user_b)
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid ObjectId")

        cursor = (
            self.col.find({
                "$or": [
                    {"sender_id": oa, "receiver_id": ob},
                    {"sender_id": ob, "receiver_id": oa}
                ]
            })
            .sort("sent_at", 1)  # orden cronológico ascendente
            .skip(skip)
            .limit(limit)
        )
        return [Message(**d) async for d in cursor]

    async def list_inbox(
        self,
        user_id: str,
        skip: int = 0,
        limit: int = 50
    ) -> list[Message]:
        """
        Devuelve los mensajes recibidos por user_id,
        orden cronológico ascendente.
        """
        try:
            uid = ObjectId(user_id)
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid ObjectId")

        cursor = (
            self.col.find({"receiver_id": uid})
            .sort("sent_at", 1)
            .skip(skip)
            .limit(limit)
        )
        return [Message(**d) async for d in cursor]

    async def list_sent(
        self,
        user_id: str,
        skip: int = 0,
        limit: int = 50
    ) -> list[Message]:
        """
        Devuelve los mensajes enviados por user_id,
        orden cronológico ascendente.
        """
        try:
            uid = ObjectId(user_id)
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid ObjectId")

        cursor = (
            self.col.find({"sender_id": uid})
            .sort("sent_at", 1)
            .skip(skip)
            .limit(limit)
        )
        return [Message(**d) async for d in cursor]

    async def delete(self, msg_id: str) -> None:
        """
        Elimina el mensaje con id msg_id (si existe).
        """
        try:
            oid = ObjectId(msg_id)
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid ObjectId")
        await self.col.delete_one({"_id": oid})
