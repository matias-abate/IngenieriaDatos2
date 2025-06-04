# app/utils/security.py
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt  # pip install "python-jose[cryptography]"
from app.core.config import settings

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: int | None = None) -> str:
    """
    Genera un JWT. En `data` típicamente pasamos {"sub": username}.
    """
    to_encode = data.copy()
    if expires_delta is None:
        expire = datetime.utcnow() + timedelta(seconds=settings.jwt_expire_seconds)
    else:
        expire = datetime.utcnow() + timedelta(seconds=expires_delta)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )
    return encoded_jwt
