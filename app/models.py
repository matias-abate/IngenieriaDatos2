# app/models.py
from pydantic import BaseModel, Field
from datetime import datetime
from uuid import uuid4

def _id():
    return uuid4().hex

class User(BaseModel):
    id: str = Field(default_factory=_id)
    username: str
    email: str

class Post(BaseModel):
    id: str = Field(default_factory=_id)
    author_id: str
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Message(BaseModel):
    id: str = Field(default_factory=_id)
    sender_id: str
    receiver_id: str
    body: str
    sent_at: datetime = Field(default_factory=datetime.utcnow)
