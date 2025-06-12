"""Endpoints for managing proveedores.
    This module provides endpoints to create, read, update, and delete proveedores.
    It includes pagination for listing proveedores and handles database operations.

    Raises:
        HTTPException: If there is an error during database operations,
        an HTTP 500 Internal Server Error is raised.
        HTTPException: If a proveedor is not found,
        an HTTP 404 Not Found error is raised.
        HTTPException: If a proveedor cannot be created or updated,
        an HTTP 400 Bad Request error is raised.

    Returns:
        APIResponse: A response containing the created, updated, or retrieved proveedor.
        APIResponsePaginated: A paginated response containing a list of proveedores.
        MessageResponse: A response indicating the success of a delete operation.
"""

import math
import mysql.connector
from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.schemas.common import APIResponse, MessageResponse, APIResponsePaginated
from app.schemas.proveedor import ProveedorBase, ProveedorCreate, ProveedorUpdate
from app.dependencies import get_db, get_current_admin_user

router = APIRouter()

@router.get(
    "/",
    summary="Get Proveedores",
    tags=["Proveedores"],
    response_model=APIResponsePaginated[ProveedorBase],
    dependencies=[Depends(get_current_admin_user)]
)
def get_proveedores_endpoint(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    db=Depends(get_db)
):
    """
    Endpoint to retrieve all proveedores.
    """
    try:
        cursor = db.cursor(dictionary=True)

        count_query = "SELECT COUNT(*) as total FROM proveedores"
        cursor.execute(count_query)
        total_items = cursor.fetchone()['total']

        offset = (page - 1) * page_size
        query = "SELECT * FROM proveedores LIMIT %s OFFSET %s"
        cursor.execute(query, (page_size, offset))

        proveedores = cursor.fetchall()
        total_pages = math.ceil(total_items / page_size) if total_items > 0 else 1

        if not proveedores:
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
            data=[ProveedorBase(**proveedor) for proveedor in proveedores],
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

@router.get(
    "/{proveedor_id}",
    summary="Get Proveedor by ID",
    tags=["Proveedores"],
    response_model=APIResponse[ProveedorBase],
    dependencies=[Depends(get_current_admin_user)]
)
def get_proveedor_by_id_endpoint(proveedor_id: int, db=Depends(get_db)):
    """
    Endpoint to retrieve a proveedor by its ID.
    """
    try:
        cursor = db.cursor(dictionary=True)
        query = "SELECT * FROM proveedores WHERE id = %s"
        cursor.execute(query, (proveedor_id,))

        proveedor = cursor.fetchone()
        if not proveedor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Proveedor not found"
            )

        return APIResponse(
            success=True,
            data=ProveedorBase(**proveedor)
        )
    except mysql.connector.Error as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database connection error: {err}"
        ) from err
    finally:
        cursor.close()
        db.close()

@router.post(
    "/",
    summary="Create Proveedor",
    tags=["Proveedores"],
    response_model=APIResponse[ProveedorBase],
    dependencies=[Depends(get_current_admin_user)]
)
def create_proveedor_endpoint(proveedor: ProveedorCreate, db=Depends(get_db)):
    """
    Endpoint to create a new proveedor.
    """
    try:
        cursor = db.cursor(dictionary=True)
        query = "INSERT INTO proveedores (nombre, contacto) VALUES (%s, %s)"
        cursor.execute(query, (proveedor.nombre, proveedor.contacto))
        db.commit()

        # proveedor.id = cursor.lastrowid
        return APIResponse(
            success=True,
            data=ProveedorCreate(**proveedor.dict())
        )
    except mysql.connector.Error as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database connection error: {err}"
        ) from err
    finally:
        cursor.close()
        db.close()

@router.put(
    "/{proveedor_id}",
    summary="Update Proveedor",
    tags=["Proveedores"],
    response_model=APIResponse[ProveedorBase],
    dependencies=[Depends(get_current_admin_user)]
)
def update_proveedor_endpoint(proveedor_id: int, proveedor: ProveedorUpdate, db=Depends(get_db)):
    """
    Endpoint to update an existing proveedor.
    """
    try:
        cursor = db.cursor(dictionary=True)
        query = "UPDATE proveedores SET nombre = %s, contacto = %s WHERE id = %s"
        cursor.execute(query, (proveedor.nombre, proveedor.contacto, proveedor_id))
        db.commit()

        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Proveedor not found"
            )

        return APIResponse(
            success=True,
            data=ProveedorUpdate(**proveedor.dict())
        )
    except mysql.connector.Error as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database connection error: {err}"
        ) from err
    finally:
        cursor.close()
        db.close()

@router.delete(
    "/{proveedor_id}",
    summary="Delete Proveedor",
    tags=["Proveedores"],
    response_model=APIResponse[MessageResponse],
    dependencies=[Depends(get_current_admin_user)]
)
def delete_proveedor_endpoint(proveedor_id: int, db=Depends(get_db)):
    """
    Endpoint to delete a proveedor by its ID.
    """
    try:
        cursor = db.cursor(dictionary=True)
        query = "DELETE FROM proveedores WHERE id = %s"
        cursor.execute(query, (proveedor_id,))
        db.commit()

        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Proveedor not found"
            )

        return APIResponse(
            success=True,
            data=MessageResponse(message="Proveedor deleted successfully")
        )
    except mysql.connector.Error as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database connection error: {err}"
        ) from err
    finally:
        cursor.close()
        db.close()
