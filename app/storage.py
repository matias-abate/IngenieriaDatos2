# app/storage.py
from typing import Dict, List
from .models import User, Post, Message

users: Dict[str, User] = {}
posts: Dict[str, Post] = {}
friends: Dict[str, List[str]] = {}      # user_id -> list[friend_id]
messages: Dict[str, Message] = {}
