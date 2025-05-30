# app/routers/users.py
from fastapi import APIRouter, HTTPException
from app.models import User
from app.storage import users, friends

router = APIRouter(prefix="/users", tags=["users"])

@router.post("", status_code=201, response_model=User)
def create_user(user: User):
    if user.id in users:
        raise HTTPException(409, "id already exists")
    users[user.id] = user
    friends[user.id] = []
    return user

@router.get("/{user_id}", response_model=User)
def read_user(user_id: str):
    if user_id not in users:
        raise HTTPException(404)
    return users[user_id]

@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: str):
    users.pop(user_id, None)
    friends.pop(user_id, None)
