"""Login endpoint to verify user credentials.
    This endpoint checks the provided email and password against the database.

    Raises:
        HTTPException: If the credentials are invalid or if there is a database error.
        HTTPException: If there is a database connection error.

    Returns:
        APIResponse[LoginResponseData]: A response containing the access token and isAdmin bool.
"""

from fastapi import APIRouter, Depends, HTTPException, status
import mysql.connector

from app.schemas.common import APIResponse
from app.schemas.login import LoginRequest, LoginResponseData
from app.utils.auth import create_access_token
from app.dependencies import get_db

router = APIRouter()

@router.post(
    "/",
    summary="Login",
    tags=["Autenticación"],
    response_model=APIResponse[LoginResponseData]
)
def post_login_endpoint(request: LoginRequest, db=Depends(get_db)):
    """
    Login endpoint to verify user credentials.
    """

    try:
        cursor = db.cursor()
        query = "SELECT * FROM login WHERE correo = %s AND contraseña = %s"
        cursor.execute(query, (request.correo, request.contraseña))

        user = cursor.fetchone()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )

        access_token = create_access_token(
            data={"id": user[0], "email": user[1], "is_admin": user[2]},
            expires_delta=None
        )
        access_token_data = {
            "access_token": access_token,
            "is_admin": user[2]
        }

        return APIResponse(
            success=True,
            data=LoginResponseData(**access_token_data)
        )
    except mysql.connector.Error as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database connection error: {err}"
        ) from err
    finally:
        cursor.close()
        db.close()
