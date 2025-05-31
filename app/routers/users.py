
from fastapi import APIRouter, Depends, Request, status
from app.models import User
from app.repositories.users_repo import UsersRepo

router = APIRouter(prefix="/users", tags=["users"])

def get_repo(request: Request) -> UsersRepo:
    return UsersRepo(request.app.state.mongo)

@router.post("", status_code=status.HTTP_201_CREATED, response_model=User)
async def create_user(user: User, repo: UsersRepo = Depends(get_repo)):
    return await repo.create(user)

@router.get("/{user_id}", response_model=User)
async def read_user(user_id: str, repo: UsersRepo = Depends(get_repo)):
    return await repo.get(user_id)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: str, repo: UsersRepo = Depends(get_repo)):
    await repo.delete(user_id)
