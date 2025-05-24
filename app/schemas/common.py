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
    
class PaginatedResponse(BaseModel, Generic[T]):
    """
    Paginated response model.
    """
    items: list[T]
    total_items: int
    page: int
    page_size: int
    total_pages: int

class APIResponse(BaseModel, Generic[T]):
    success: bool
    data: T | MessageResponse | None = None
    timestamp: int = int(time.time())
    
class APIResponsePaginated(BaseModel, Generic[T]):
    success: bool
    data: list[T] | MessageResponse | None = None
    total_items: int = 0
    page: int = 1
    page_size: int = 10
    total_pages: int = 0
    timestamp: int = int(time.time())