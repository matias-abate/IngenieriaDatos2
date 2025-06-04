# app/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from app.repositories.users_repo import UsersRepo
from app.utils.security import verify_password, hash_password, create_access_token
from app.models import UserCreate, UserPublic

router = APIRouter(prefix="/auth", tags=["auth"])

def get_users_repo(request: Request) -> UsersRepo:
    return UsersRepo(request.app.state.mongo)

@router.post(
    "/register",
    response_model=UserPublic,
    status_code=status.HTTP_201_CREATED,
)
async def register_user(
    user_data: UserCreate,
    ur: UsersRepo = Depends(get_users_repo),
):
    """
    POST /auth/register
    Recibe JSON { "username", "email", "password" }.
    1) Chequea que existan los campos.
    2) Verifica que no haya otro usuario con el mismo username.
    3) Hashea la password.
    4) Inserta { username, email, hashed_password } en Mongo.
    5) Devuelve el usuario recién creado (id, username, email).
    """
    username = user_data.username
    email = user_data.email
    password = user_data.password

    existing = await ur.get_by_username(username)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un usuario con ese username",
        )

    hashed_pwd = hash_password(password)
    new_user = {
        "username": username,
        "email": email,
        "hashed_password": hashed_pwd,
    }
    inserted = await ur.create_user(new_user)
    return {"_id": inserted["inserted_id"], "username": username, "email": email}


@router.post(
    "/login",
    response_model=dict,  # devolvemos { access_token, token_type }
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    ur: UsersRepo = Depends(get_users_repo),
):
    """
    POST /auth/login
    Recibe form-urlencoded con keys: username, password.
    1) Busca usuario por username en Mongo.
    2) Verifica contraseña con verify_password.
    3) Si ok, genera JWT y devuelve { access_token, token_type: "bearer" }.
    """
    user = await ur.get_by_username(form_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña inválidos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # user["hashed_password"] existe porque en get_by_username retornamos ese campo
    if not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña inválidos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}
