from fastapi import APIRouter, Depends, HTTPException, Query, status
import mysql.connector, math

from app.schemas.common import APIResponse, MessageResponse, APIResponsePaginated
from app.schemas.user import UserBase, UserCreate
from app.dependencies import get_db, get_current_admin_user

router = APIRouter()

@router.get("/", summary="Get Users", tags=["Users"], response_model=APIResponsePaginated[UserBase], dependencies=[Depends(get_current_admin_user)])
def get_users_endpoint(page: int = Query(1, ge=1, description="Page number"), page_size: int = Query(10, ge=1, le=100, description="Items per page"), db=Depends(get_db)):
    """
    Endpoint to retrieve all users.
    """
    try:
        cursor = db.cursor(dictionary=True)

        count_query = "SELECT COUNT(*) as total FROM login"
        cursor.execute(count_query)
        total_items = cursor.fetchone()['total']

        offset = (page - 1) * page_size
        query = "SELECT correo, es_administrador FROM login LIMIT %s OFFSET %s"
        cursor.execute(query, (page_size, offset))

        users = cursor.fetchall()
        total_pages = math.ceil(total_items / page_size) if total_items > 0 else 1

        if not users:
            return APIResponsePaginated(
                success=True,
                data=[],
                total_items=total_items,
                page=page,
                page_size=page_size,
                total_pages=total_pages
            )

        return APIResponsePaginated(
            success=True,
            data=[UserBase(**user) for user in users],
            total_items=total_items,
            page=page,
            page_size=page_size,
            total_pages=total_pages
        )
    except mysql.connector.Error as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database connection error: {err}"
        ) from err
    finally:
        cursor.close()
        db.close()

@router.get("/{user_correo}", summary="Get User by Email", tags=["Users"], response_model=APIResponse[UserBase], dependencies=[Depends(get_current_admin_user)])
def get_user_by_email_endpoint(user_correo: str, db=Depends(get_db)):
    """
    Endpoint to retrieve a user by their email.
    """
    try:
        cursor = db.cursor(dictionary=True)
        query = "SELECT correo, es_administrador FROM login WHERE correo = %s"
        cursor.execute(query, (user_correo,))
        user = cursor.fetchone()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        return APIResponse(
            success=True,
            data=UserBase(**user)
        )
    except mysql.connector.Error as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database connection error: {err}"
        ) from err
    finally:
        cursor.close()
        db.close()

@router.post("/", summary="Create User", tags=["Users"], response_model=APIResponse[UserBase], dependencies=[Depends(get_current_admin_user)])
def create_user_endpoint(user: UserCreate, db=Depends(get_db)):
    """
    Endpoint to create a new user.
    """
    try:
        cursor = db.cursor(dictionary=True)
        query = "INSERT INTO login (correo, contraseña, es_administrador) VALUES (%s, %s, %s)"
        cursor.execute(query, (user.correo, user.contraseña, user.es_administrador))
        db.commit()

        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User creation failed"
            )

        user_data = UserBase(correo=user.correo, es_administrador=user.es_administrador)
        return APIResponse(
            success=True,
            data=user_data
        )
    except mysql.connector.Error as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database connection error: {err}"
        ) from err
    finally:
        cursor.close()
        db.close()

@router.delete("/{user_correo}", summary="Delete User", tags=["Users"], response_model=MessageResponse, dependencies=[Depends(get_current_admin_user)])
def delete_user_endpoint(user_correo: str, db=Depends(get_db)):
    """
    Endpoint to delete a user by their email.
    """
    try:
        cursor = db.cursor(dictionary=True)
        query = "DELETE FROM login WHERE correo = %s"
        cursor.execute(query, (user_correo,))
        db.commit()

        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        return MessageResponse(
            success=True,
            message="User deleted successfully"
        )
    except mysql.connector.Error as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database connection error: {err}"
        ) from err
    finally:
        cursor.close()
        db.close()