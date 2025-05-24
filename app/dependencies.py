from fastapi import HTTPException, Depends, status
from app.database import get_database_connection
from fastapi.security import OAuth2PasswordBearer
import mysql.connector

from app.utils.auth import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="v1/auth/login")

def get_db():
    """Dependency to get a database connection."""
    try:
        connection = get_database_connection()
        yield connection
    except mysql.connector.Error as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database connection error: {err}"
        )
    finally:
        if connection.is_connected():
            connection.close()
            
def get_current_user(token : str = Depends(oauth2_scheme)):
    """
    Dependency to get the current user from the JWT token.
    """
    
    try:
        payload = decode_access_token(token)
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return payload
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        ) from e

def get_current_admin_user(current_user: dict = Depends(get_current_user)):
    """
    Dependency to ensure the current user is an admin.
    """
    if not current_user.get("is_admin", False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform this action",
        )
    
    return current_user