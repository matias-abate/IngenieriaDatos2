# app/models.py
from bson import ObjectId
from pydantic import BaseModel, Field
from datetime import datetime

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if isinstance(v, ObjectId):
            return v
        if isinstance(v, str) and ObjectId.is_valid(v):   # ← opcional, acepta str válidos
            return ObjectId(v)
        raise ValueError("Invalid ObjectId")

    @classmethod
    def __modify_schema__(cls, field_schema):             # ← NUEVO
        # Swagger/OpenAPI lo tratará como string
        field_schema.update(type="string")

# ---------- MODELOS ----------
class User(BaseModel):
    id: PyObjectId | None = Field(alias="_id", default=None)
    username: str
    email: str

    class Config:
        json_encoders = {ObjectId: str}
        allow_population_by_field_name = True
        arbitrary_types_allowed = True                    # ← NUEVO


class Post(BaseModel):
    id: PyObjectId | None = Field(alias="_id", default=None)
    author_id: PyObjectId
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_encoders = {ObjectId: str}
        allow_population_by_field_name = True
        arbitrary_types_allowed = True                    # ← NUEVO


class Message(BaseModel):
    id: PyObjectId | None = Field(alias="_id", default=None)
    sender_id: PyObjectId
    receiver_id: PyObjectId
    content: str
    sent_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_encoders = {ObjectId: str}
        allow_population_by_field_name = True
