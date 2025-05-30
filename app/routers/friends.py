# app/routers/friends.py
from fastapi import APIRouter, HTTPException
from app.storage import friends, users     # dicts in-memory
from app.models import User

router = APIRouter(prefix="/friends", tags=["friends"])   # ← IMPORTANTE

@router.post("/{user_id}/{friend_id}", status_code=201)
def add_friend(user_id: str, friend_id: str):
    if user_id not in users or friend_id not in users:
        raise HTTPException(404, "User not found")

    friends[user_id].append(friend_id)
    friends[friend_id].append(user_id)      # relación mutua
    return {"detail": "ok"}

@router.get("/{user_id}", response_model=list[str])
def list_friends(user_id: str):
    return friends.get(user_id, [])
