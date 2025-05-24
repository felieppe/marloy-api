from fastapi import HTTPException, status
import mysql.connector
from app.database import get_database_connection

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