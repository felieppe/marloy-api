"""
    Endpoint to retrieve all mantenimientos.
    This endpoint allows you to retrieve a paginated list of mantenimientos.

    Raises:
        HTTPException: If there is an error with the database connection,
        an HTTP 500 Internal Server Error is raised.

    Returns:
        APIResponsePaginated: A paginated response containing the mantenimientos.
"""

import math
import mysql.connector
from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.schemas.common import APIResponse, MessageResponse, APIResponsePaginated
from app.schemas.mantenimiento import MantenimientoBase, MantenimientoCreate
from app.dependencies import get_db

router = APIRouter()

@router.get(
    "/",
    summary="Get Mantenimientos",
    tags=["Mantenimientos"],
    response_model=APIResponsePaginated[MantenimientoBase]
)
def get_mantenimientos_endpoint(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    db=Depends(get_db)
):
    """
    Endpoint to retrieve all mantenimientos.
    """
    try:
        cursor = db.cursor(dictionary=True)

        count_query = "SELECT COUNT(*) as total FROM mantenimientos"
        cursor.execute(count_query)
        total_items = cursor.fetchone()['total']

        offset = (page - 1) * page_size
        query = "SELECT * FROM mantenimientos LIMIT %s OFFSET %s"
        cursor.execute(query, (page_size, offset))

        mantenimientos = cursor.fetchall()
        total_pages = math.ceil(total_items / page_size) if total_items > 0 else 1

        if not mantenimientos:
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
            data=[MantenimientoBase(**mantenimiento) for mantenimiento in mantenimientos],
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
    "/{id_maquina}",
    summary="Get Mantenimiento by ID",
    tags=["Mantenimientos"],
    response_model=APIResponse[MantenimientoBase]
)
def get_mantenimiento_by_id_endpoint(id_maquina: int, db=Depends(get_db)):
    """
    Endpoint to retrieve a mantenimiento by its ID.
    """
    try:
        cursor = db.cursor(dictionary=True)
        query = "SELECT * FROM mantenimientos WHERE id_maquina = %s"
        cursor.execute(query, (id_maquina,))
        mantenimiento = cursor.fetchone()

        if not mantenimiento:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Mantenimiento not found"
            )

        return APIResponse(
            success=True,
            data=MantenimientoBase(**mantenimiento)
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
    summary="Create Mantenimiento",
    tags=["Mantenimientos"],
    response_model=APIResponse[MantenimientoBase]
)
def create_mantenimiento_endpoint(mantenimiento: MantenimientoCreate, db=Depends(get_db)):
    """
    Endpoint to create a new mantenimiento.
    """
    try:
        cursor = db.cursor(dictionary=True)

        query = "SELECT * FROM maquinas WHERE id = %s"
        cursor.execute(query, (mantenimiento.id_maquina,))

        maquina = cursor.fetchone()
        if not maquina:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Machine not found"
            )

        query = "SELECT * FROM tecnicos WHERE ci = %s"
        cursor.execute(query, (mantenimiento.ci_tecnico,))

        tecnico = cursor.fetchone()
        if not tecnico:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Technician not found"
            )

        insert_query = """
            INSERT INTO mantenimientos (id_maquina, ci_tecnico, tipo, fecha, observaciones)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(
            insert_query,
            (
                mantenimiento.id_maquina,
                mantenimiento.ci_tecnico,
                mantenimiento.tipo,
                mantenimiento.fecha,
                mantenimiento.observaciones
            )
        )
        db.commit()

        mantenimiento_id = cursor.lastrowid
        cursor.execute("SELECT * FROM mantenimientos WHERE id = %s", (mantenimiento_id,))
        new_mantenimiento = cursor.fetchone()

        return APIResponse(
            success=True,
            data=MantenimientoCreate(**new_mantenimiento)
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
    "/{id}",
    summary="Update Mantenimiento",
    tags=["Mantenimientos"],
    response_model=APIResponse[MantenimientoBase]
)
def update_mantenimiento_endpoint(
    mantenimiento_id: int,
    mantenimiento: MantenimientoCreate,
    db=Depends(get_db)
):
    """
    Endpoint to update an existing mantenimiento.
    """
    try:
        cursor = db.cursor(dictionary=True)
        update_query = """
            UPDATE mantenimientos
            SET id_maquina = %s, ci_tecnico = %s, tipo = %s, fecha = %s, observaciones = %s
            WHERE id = %s
        """
        cursor.execute(
            update_query,
            (
                mantenimiento.id_maquina,
                mantenimiento.ci_tecnico,
                mantenimiento.tipo,
                mantenimiento.fecha,
                mantenimiento.observaciones,
                mantenimiento_id
            )
        )
        db.commit()

        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Mantenimiento not found"
            )

        cursor.execute("SELECT * FROM mantenimientos WHERE id = %s", (mantenimiento_id,))
        updated_mantenimiento = cursor.fetchone()

        return APIResponse(
            success=True,
            data=MantenimientoBase(**updated_mantenimiento)
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
    "/{id}",
    summary="Delete Mantenimiento",
    tags=["Mantenimientos"],
    response_model=MessageResponse
)
def delete_mantenimiento_endpoint(mantenimiento_id: int, db=Depends(get_db)):
    """
    Endpoint to delete a mantenimiento by its ID.
    """
    try:
        cursor = db.cursor(dictionary=True)
        delete_query = "DELETE FROM mantenimientos WHERE id = %s"
        cursor.execute(delete_query, (mantenimiento_id,))
        db.commit()

        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Mantenimiento not found"
            )

        return MessageResponse(
            success=True,
            message="Mantenimiento deleted successfully"
        )
    except mysql.connector.Error as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database connection error: {err}"
        ) from err
    finally:
        cursor.close()
        db.close()
