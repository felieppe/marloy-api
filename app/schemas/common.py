"""
    Common response schemas for API responses.
    This module defines common response models used across the application.
"""

import time
from typing import List, TypeVar, Generic
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)

class MessageResponse(BaseModel):
    """
    Message response model.
    """
    message: str

class PaginatedResponse(BaseModel, Generic[T]):
    """
    Paginated response model.
    """
    items: List[T]
    total_items: int
    page: int
    page_size: int
    total_pages: int

class APIResponse(BaseModel, Generic[T]):
    """
    Base API response model.
    """
    success: bool
    data: T | List[T] | MessageResponse | None = None
    timestamp: int = int(time.time())

class APIResponsePaginated(BaseModel, Generic[T]):
    """
    Base API response model for paginated data.
    This model is used to standardize the response structure for paginated endpoints.
    """

    success: bool
    data: List[T] | MessageResponse | None = None
    total_items: int = 0
    page: int = 1
    page_size: int = 10
    total_pages: int = 0
    timestamp: int = int(time.time())
