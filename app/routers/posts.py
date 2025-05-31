# app/routers/posts.py
from fastapi import APIRouter, Depends, Request, status
from app.models import Post, PyObjectId, User
from app.repositories.posts_repo import PostsRepo
from app.repositories.users_repo import UsersRepo

router = APIRouter(prefix="/posts", tags=["posts"])

def get_repo(request: Request) -> PostsRepo:
    return PostsRepo(request.app.state.mongo)

def get_users_repo(request: Request) -> UsersRepo:
    return UsersRepo(request.app.state.mongo)

@router.post("", status_code=status.HTTP_201_CREATED, response_model=Post)
async def create_post(
    post: Post,
    repo: PostsRepo = Depends(get_repo),
    users_repo: UsersRepo = Depends(get_users_repo),
):
    # validar que el author exista
    await users_repo.get(str(post.author_id))
    return await repo.create(post)

@router.get("/{post_id}", response_model=Post)
async def read_post(
    post_id: str,
    repo: PostsRepo = Depends(get_repo),
):
    return await repo.get(post_id)

@router.get("", response_model=list[Post])
async def list_posts(
    skip: int = 0,
    limit: int = 20,
    repo: PostsRepo = Depends(get_repo),
):
    return await repo.list(skip, limit)

@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post_id: str,
    repo: PostsRepo = Depends(get_repo),
):
    await repo.delete(post_id)
