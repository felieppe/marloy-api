"""Endpoints for managing registros de consumo.
    This module provides endpoints to create, read, update, and delete registros de consumo.

    Raises:
        HTTPException: If there is an error during database operations,
        an HTTP 500 Internal Server Error is raised.
        HTTPException: If a registro de consumo is not found,
        an HTTP 404 Not Found error is raised.
        HTTPException: If a registro de consumo cannot be created or updated,
        an HTTP 400 Bad Request error is raised.

    Returns:
        APIResponse: A response containing the created, updated, or retrieved registro de consumo.
        APIResponsePaginated: A paginated response containing a list of registros de consumo.
        MessageResponse: A response indicating the success of a delete operation.
"""

import math
import mysql.connector
from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.schemas.common import APIResponse, MessageResponse, APIResponsePaginated
from app.schemas.registro_consumo import RegistroConsumoBase, RegistroConsumoCreate
from app.dependencies import get_db

router = APIRouter()

@router.get(
    "/",
    summary="Get Registros de Consumo",
    tags=["Registros de Consumo"],
    response_model=APIResponsePaginated[RegistroConsumoBase]
)
def get_registros_consumo_endpoint(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    db=Depends(get_db)
):
    """
    Endpoint to retrieve all registros de consumo.
    """
    try:
        cursor = db.cursor(dictionary=True)

        count_query = "SELECT COUNT(*) as total FROM registro_consumo"
        cursor.execute(count_query)
        total_items = cursor.fetchone()['total']

        offset = (page - 1) * page_size
        query = "SELECT * FROM registro_consumo LIMIT %s OFFSET %s"
        cursor.execute(query, (page_size, offset))

        registros_consumo = cursor.fetchall()
        total_pages = math.ceil(total_items / page_size) if total_items > 0 else 1

        if not registros_consumo:
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
            data=[RegistroConsumoBase(**registro) for registro in registros_consumo],
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
    "/{id_consumo}",
    summary="Get Registro de Consumo by ID",
    tags=["Registros de Consumo"],
    response_model=APIResponse[RegistroConsumoBase]
)
def get_registro_consumo_by_id_endpoint(id_consumo: int, db=Depends(get_db)):
    """
    Endpoint to retrieve a registro de consumo by its ID.
    """
    try:
        cursor = db.cursor(dictionary=True)
        query = "SELECT * FROM registro_consumo WHERE id = %s"
        cursor.execute(query, (id_consumo,))
        registro_consumo = cursor.fetchone()

        if not registro_consumo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Registro de consumo not found"
            )

        return APIResponse(
            success=True,
            data=RegistroConsumoBase(**registro_consumo)
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
    summary="Create Registro de Consumo",
    tags=["Registros de Consumo"],
    response_model=APIResponse[RegistroConsumoBase]
)
def create_registro_consumo_endpoint(registro_consumo: RegistroConsumoCreate, db=Depends(get_db)):
    """
    Endpoint to create a new registro de consumo.
    """
    try:
        cursor = db.cursor(dictionary=True)
        insert_query = """
            INSERT INTO registro_consumo (id_maquina, id_insumo, fecha, cantidad_usada)
            VALUES (%s, %s, %s, %s)
            RETURNING id
        """
        cursor.execute(insert_query, (
            registro_consumo.id_maquina,
            registro_consumo.id_insumo,
            registro_consumo.fecha,
            registro_consumo.cantidad_usada
        ))
        db.commit()
        new_id = cursor.fetchone()['id']

        return APIResponse(
            success=True,
            data=RegistroConsumoBase(id=new_id, **registro_consumo.dict())
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
    "/{id_consumo}",
    summary="Update Registro de Consumo",
    tags=["Registros de Consumo"],
    response_model=APIResponse[RegistroConsumoBase]
)
def update_registro_consumo_endpoint(
    id_consumo: int,
    registro_consumo: RegistroConsumoCreate,
    db=Depends(get_db)
):
    """
    Endpoint to update an existing registro de consumo.
    """
    try:
        cursor = db.cursor(dictionary=True)
        update_query = """
            UPDATE registro_consumo
            SET id_maquina = %s, id_insumo = %s, fecha = %s, cantidad_usada = %s
            WHERE id = %s
            RETURNING id
        """
        cursor.execute(update_query, (
            registro_consumo.id_maquina,
            registro_consumo.id_insumo,
            registro_consumo.fecha,
            registro_consumo.cantidad_usada,
            id_consumo
        ))
        db.commit()
        updated_id = cursor.fetchone()['id']

        if not updated_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Registro de consumo not found"
            )

        return APIResponse(
            success=True,
            data=RegistroConsumoBase(id=updated_id, **registro_consumo.dict())
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
    "/{id_consumo}",
    summary="Delete Registro de Consumo",
    tags=["Registros de Consumo"],
    response_model=MessageResponse
)
def delete_registro_consumo_endpoint(id_consumo: int, db=Depends(get_db)):
    """
    Endpoint to delete a registro de consumo by its ID.
    """
    try:
        cursor = db.cursor(dictionary=True)
        delete_query = "DELETE FROM registro_consumo WHERE id = %s"
        cursor.execute(delete_query, (id_consumo,))
        db.commit()

        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Registro de consumo not found"
            )

        return MessageResponse(success=True, message="Registro de consumo deleted successfully")
    except mysql.connector.Error as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database connection error: {err}"
        ) from err
    finally:
        cursor.close()
        db.close()
