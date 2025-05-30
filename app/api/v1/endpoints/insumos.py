from fastapi import APIRouter, Depends, HTTPException, status, Query
import mysql.connector, math

from app.schemas.common import APIResponse, MessageResponse, APIResponsePaginated
from app.schemas.insumo import InsumoBase, InsumoCreate, InsumoUpdate
from app.dependencies import get_db

router = APIRouter()

@router.get("/", summary="Get Insumos", tags=["Insumos"], response_model=APIResponsePaginated[InsumoBase])
def get_insumos_endpoint(page: int = Query(1, ge=1, description="Page number"), page_size: int = Query(10, ge=1, le=100, description="Items per page"), db=Depends(get_db)):
    """
    Endpoint to retrieve all insumos.
    """
    try:
        cursor = db.cursor(dictionary=True)
        
        count_query = "SELECT COUNT(*) as total FROM insumos"
        cursor.execute(count_query)
        total_items = cursor.fetchone()['total']
        
        offset = (page - 1) * page_size
        query = "SELECT * FROM insumos LIMIT %s OFFSET %s"
        cursor.execute(query, (page_size, offset))

        insumos = cursor.fetchall()
        total_pages = math.ceil(total_items / page_size) if total_items > 0 else 1
        
        if not insumos:
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
            data=[InsumoBase(**insumo) for insumo in insumos],
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
        
@router.get("/{insumo_id}", summary="Get Insumo by ID", tags=["Insumos"], response_model=APIResponse[InsumoBase])
def get_insumo_by_id_endpoint(insumo_id: int, db=Depends(get_db)):
    """
    Endpoint to retrieve an insumo by its ID.
    """
    try:
        cursor = db.cursor(dictionary=True)
        query = "SELECT * FROM insumos WHERE id = %s"
        cursor.execute(query, (insumo_id,))

        insumo = cursor.fetchone()
        if not insumo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Insumo not found"
            )

        return APIResponse(
            success=True,
            data=InsumoBase(**insumo)
        )
    except mysql.connector.Error as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database connection error: {err}"
        ) from err
    finally:
        cursor.close()
        db.close()
        
@router.post("/", summary="Create Insumo", tags=["Insumos"], response_model=APIResponse[InsumoBase])
def create_insumo_endpoint(insumo: InsumoCreate, db=Depends(get_db)):
    """
    Endpoint to create a new insumo.
    """
    try:
        cursor = db.cursor(dictionary=True)
        query = """
            INSERT INTO insumos (descripcion, tipo, precio_unitario, id_proveedor)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (insumo.descripcion, insumo.tipo, insumo.precio_unitario, insumo.id_proveedor))
        db.commit()
        
        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to create insumo"
            )

        cursor.execute("SELECT * FROM insumos WHERE descripcion = %s AND tipo = %s AND precio_unitario = %s AND id_proveedor = %s", (insumo.descripcion, insumo.tipo, insumo.precio_unitario, insumo.id_proveedor,))
        created_insumo = cursor.fetchone()

        return APIResponse(
            success=True,
            data=InsumoBase(**created_insumo)
        )
    except mysql.connector.Error as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database connection error: {err}"
        ) from err
    finally:
        cursor.close()
        db.close()
        
@router.put("/{insumo_id}", summary="Update Insumo", tags=["Insumos"], response_model=APIResponse[InsumoBase])
def update_insumo_endpoint(insumo_id: int, insumo: InsumoUpdate, db=Depends(get_db)):
    """
    Endpoint to update an existing insumo.
    """
    try:
        cursor = db.cursor(dictionary=True)
        query = """
            UPDATE insumos
            SET descripcion = %s, tipo = %s, precio_unitario = %s, id_proveedor = %s
            WHERE id = %s
        """
        cursor.execute(query, (insumo.descripcion, insumo.tipo, insumo.precio_unitario, insumo.id_proveedor, insumo_id))
        db.commit()

        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Insumo not found"
            )
        
        cursor.execute("SELECT * FROM insumos WHERE id = %s", (insumo_id,))
        updated_insumo = cursor.fetchone()

        if not updated_insumo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Insumo not found"
            )

        return APIResponse(
            success=True,
            data=InsumoBase(**updated_insumo)
        )
    except mysql.connector.Error as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database connection error: {err}"
        ) from err
    finally:
        cursor.close()
        db.close()
        
@router.delete("/{insumo_id}", summary="Delete Insumo", tags=["Insumos"], response_model=APIResponse[MessageResponse])
def delete_insumo_endpoint(insumo_id: int, db=Depends(get_db)):
    """
    Endpoint to delete an insumo by its ID.
    """
    try:
        cursor = db.cursor(dictionary=True)
        query = "DELETE FROM insumos WHERE id = %s"
        cursor.execute(query, (insumo_id,))
        db.commit()

        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Insumo not found"
            )

        return APIResponse(
            success=True,
            data=MessageResponse(message="Insumo deleted successfully")
        )
    except mysql.connector.Error as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database connection error: {err}"
        ) from err
    finally:
        cursor.close()
        db.close()