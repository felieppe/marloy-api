"""
    Create a JWT access token with an expiration time.

    Raises:
        ValueError: If the token is invalid or has expired.

    Returns:
        str: The encoded JWT access token.
    """

from datetime import datetime, timedelta
from typing import Any
from jose import jwt

from app.config import settings

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """
    Create a JWT access token with an expiration time.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> Any:
    """
    Decode a JWT access token and return the payload.
    """
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError as exc:
        raise ValueError("Token has expired") from exc
    except jwt.JWTError as e:
        raise ValueError(f"Invalid token: {e}") from e
