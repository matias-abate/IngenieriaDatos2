# app/routers/posts.py
from fastapi import APIRouter, Depends, HTTPException, status, Request
from typing import List
from app.models import Post
from app.repositories.posts_repo import PostsRepo

router = APIRouter(prefix="/posts", tags=["posts"])

def get_posts_repo(request: Request) -> PostsRepo:
    return PostsRepo(request.app.state.mongo)

@router.post("", response_model=Post, status_code=status.HTTP_201_CREATED)
async def create_post(
    post_data: Post,
    pr: PostsRepo = Depends(get_posts_repo),
):
    inserted = await pr.create_post(post_data.model_dump(by_alias=True, exclude_none=True))
    post_data.id = inserted["inserted_id"]
    return post_data

@router.get("", response_model=List[Post])
async def list_posts(pr: PostsRepo = Depends(get_posts_repo)):
    return await pr.list_posts()
