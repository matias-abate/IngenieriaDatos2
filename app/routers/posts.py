# app/routers/posts.py
from fastapi import APIRouter, HTTPException
from app.models import Post
from app.storage import posts

router = APIRouter(prefix="/posts", tags=["posts"])   # ← ESTA variable es la que importa main.py

@router.post("", status_code=201, response_model=Post)
def create_post(post: Post):
    posts[post.id] = post
    return post
