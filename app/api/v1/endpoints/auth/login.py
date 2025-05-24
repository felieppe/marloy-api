from fastapi import APIRouter, Depends, HTTPException, status
import mysql.connector

from app.schemas.common import APIResponse
from app.schemas.login import LoginRequest, LoginResponseData
from app.dependencies import get_db

router = APIRouter()

@router.post("/", summary="Login", tags=["Login"], response_model=APIResponse[LoginResponseData])
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

        access_token_data = {
            "access_token": "", # Missing JWT gen.
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
