# app/routers/posts.py

from fastapi import APIRouter, Depends, Request, HTTPException
from typing import List
from app.models import Post
from app.repositories.posts_repo import PostsRepo
from app.repositories.users_repo import UsersRepo
from app.repositories.friends_graph_repo import FriendsGraphRepo

router = APIRouter(prefix="/posts", tags=["posts"])

def get_repo(request: Request) -> PostsRepo:
    return PostsRepo(request.app.state.mongo)

def get_users_repo(request: Request) -> UsersRepo:
    return UsersRepo(request.app.state.mongo)

# Dependencia para Neo4j
def get_graph_repo(request: Request) -> FriendsGraphRepo:
    return FriendsGraphRepo(request.app.state.neo)

@router.post("", status_code=201, response_model=Post)
async def create_post(
    post: Post,
    repo: PostsRepo = Depends(get_repo),
    users_repo: UsersRepo = Depends(get_users_repo),
):
    # Valida que el autor exista (en MongoDB)
    await users_repo.get(str(post.author_id))
    return await repo.create(post)

@router.get("/{post_id}", response_model=Post)
async def read_post(
    post_id: str,
    repo: PostsRepo = Depends(get_repo),
):
    return await repo.get(post_id)

@router.get("", response_model=List[Post])
async def list_posts(
    skip: int = 0,
    limit: int = 20,
    repo: PostsRepo = Depends(get_repo),
):
    return await repo.list_all(skip, limit)   # ◀ usa list_all en lugar de list()

@router.delete("/{post_id}", status_code=204)
async def delete_post(
    post_id: str,
    repo: PostsRepo = Depends(get_repo),
):
    await repo.delete(post_id)


# ── NUEVO endpoint: Feed de posts de amigos ────────────────────────
@router.get("/feed/{uid}", response_model=List[Post])
async def feed_posts_of_friends(
    uid: str,
    skip: int = 0,
    limit: int = 20,
    posts_repo: PostsRepo = Depends(get_repo),
    graph_repo: FriendsGraphRepo = Depends(get_graph_repo),
):
    # 1) Verificar que el usuario exista en Mongo
    try:
        await UsersRepo(posts_repo.col.database).get(uid)
    except HTTPException:
        raise HTTPException(status_code=404, detail="User not found")

    # 2) Obtener la lista de amigos directos desde Neo4j
    friends_ids = await graph_repo.friends(uid)
    if not friends_ids:
        return []  # Usuario sin amigos, no hay feed

    # 3) Obtener posts en Mongo cuyos author_id estén en friends_ids
    posts = await posts_repo.list_by_author_ids(friends_ids, skip, limit)
    return posts
