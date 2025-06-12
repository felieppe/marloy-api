""" Health check endpoint to verify the API and database connection.
    This endpoint checks if the API is running and if it can connect to the database.

    Raises:
        HTTPException: If the database connection fails,
        an HTTP 503 Service Unavailable error is raised.

    Returns:
        APIResponse: A response indicating the health status of the API.
"""

import mysql.connector
from fastapi import APIRouter, Depends, HTTPException, status

from app.schemas.common import APIResponse, MessageResponse
from app.dependencies import get_db

router = APIRouter()

@router.get(
    "/",
    summary="Health Check",
    tags=["Health"],
    response_model=APIResponse[MessageResponse]
)
def get_health_endpoint(db=Depends(get_db)):
    """
    Health check endpoint to verify the API and database connection.
    """
    try:
        cursor = db.cursor()
        cursor.execute("SELECT 1")
        cursor.fetchone()

        return APIResponse(success=True, data=MessageResponse(message="API is healthy!"))
    except mysql.connector.Error as err:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Database connection error: {err}"
        ) from err
    finally:
        cursor.close()
