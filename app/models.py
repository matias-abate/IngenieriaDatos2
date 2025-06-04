# app/models.py

from bson import ObjectId
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

#
# 1) Primero definimos el validador de ObjectId para Pydantic
#
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if isinstance(v, ObjectId):
            return v
        if isinstance(v, str) and ObjectId.is_valid(v):
            return ObjectId(v)
        raise ValueError("Invalid ObjectId")

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


#
# 2) Esquema para crear usuarios (input): UserCreate
#
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

    class Config:
        allow_population_by_field_name = True


#
# 3) Esquema público de usuario (output): UserPublic
#
class UserPublic(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    username: str
    email: str

    class Config:
        json_encoders = {ObjectId: str}
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


#
# 4) Definimos el esquema Post (id, author_id, content, created_at)
#
class Post(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    author_id: PyObjectId
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_encoders = {ObjectId: str}
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
