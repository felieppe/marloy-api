from typing import TypeVar, Generic
from pydantic import BaseModel
import time

T = TypeVar("T", bound=BaseModel)

class APIResponse(BaseModel, Generic[T]):
    """
    Base API response model.
    """
    success: bool
    data: T | None = None
    timestamp: int = int(time.time())

class MessageResponse(BaseModel):
    """
    Message response model.
    """
    message: str

class APIResponse(BaseModel, Generic[T]):
    success: bool
    data: T | MessageResponse | None = None
    timestamp: int = int(time.time())