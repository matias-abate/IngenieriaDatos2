# app/routers/users.py

from fastapi import APIRouter, Depends, HTTPException, status, Request
from app.repositories.users_repo import UsersRepo
from app.models import UserCreate, UserPublic

router = APIRouter(prefix="/users", tags=["users"])


def get_users_repo(request: Request) -> UsersRepo:
    return UsersRepo(request.app.state.mongo)


@router.post(
    "",
    response_model=UserPublic,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    user_data: UserCreate,                  # ahora usamos UserCreate
    ur: UsersRepo = Depends(get_users_repo),
):
    """
    POST /users
    - Recibe { username, email, password } (UserCreate).
    - Verifica que no exista ese username, hashea la password,
      guarda en Mongo { username, email, hashed_password }.
    - Devuelve UserPublic { id, username, email }.
    """
    existing = await ur.get_by_username(user_data.username)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un usuario con ese username",
        )

    # Importar aquí para evitar referencia circular, pero podrías hacerlo arriba:
    from app.utils.security import hash_password

    hashed_pwd = hash_password(user_data.password)
    new_user = {
        "username": user_data.username,
        "email": user_data.email,
        "hashed_password": hashed_pwd,
    }
    inserted = await ur.create_user(new_user)
    return {"_id": inserted["inserted_id"], "username": user_data.username, "email": user_data.email}


@router.get(
    "/{user_id}",
    response_model=UserPublic,  # devolvemos solo los campos públicos
)
async def read_user(user_id: str, ur: UsersRepo = Depends(get_users_repo)):
    """
    GET /users/{user_id}
    - Busca un usuario por _id en Mongo.
    - Si existe, devuelve { id, username, email } (UserPublic).
    - Si no existe, 404.
    """
    doc = await ur.get(user_id)
    if not doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return {"_id": doc["_id"], "username": doc["username"], "email": doc["email"]}
