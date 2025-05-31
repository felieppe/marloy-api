from fastapi import APIRouter, Depends, HTTPException, Query, status
import mysql.connector, math

from app.schemas.common import APIResponse, MessageResponse, APIResponsePaginated
from app.schemas.maquina import MaquinaBase, MaquinaCreate
from app.dependencies import get_db, get_current_admin_user

router = APIRouter()

@router.get("/", summary="Get Maquinas", tags=["Maquinas"], response_model=APIResponsePaginated[MaquinaBase], dependencies=[Depends(get_current_admin_user)])
def get_maquinas_endpoint(page: int = Query(1, ge=1, description="Page number"), page_size: int = Query(10, ge=1, le=100, description="Items per page"), db=Depends(get_db)):
    """
    Endpoint to retrieve all maquinas.
    """
    try:
        cursor = db.cursor(dictionary=True)

        count_query = "SELECT COUNT(*) as total FROM maquinas"
        cursor.execute(count_query)
        total_items = cursor.fetchone()['total']

        offset = (page - 1) * page_size
        query = "SELECT * FROM maquinas LIMIT %s OFFSET %s"
        cursor.execute(query, (page_size, offset))

        maquinas = cursor.fetchall()
        total_pages = math.ceil(total_items / page_size) if total_items > 0 else 1

        if not maquinas:
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
            data=[MaquinaBase(**maquina) for maquina in maquinas],
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

@router.get("/{maquina_id}", summary="Get Maquina by ID", tags=["Maquinas"], response_model=APIResponse[MaquinaBase], dependencies=[Depends(get_current_admin_user)])
def get_maquina_by_id_endpoint(maquina_id: int, db=Depends(get_db)):
    """
    Endpoint to retrieve a maquina by its ID.
    """
    try:
        cursor = db.cursor(dictionary=True)
        query = "SELECT * FROM maquinas WHERE id = %s"
        cursor.execute(query, (maquina_id,))
        maquina = cursor.fetchone()

        if not maquina:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Maquina not found"
            )

        return APIResponse(
            success=True,
            data=MaquinaBase(**maquina)
        )
    except mysql.connector.Error as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database connection error: {err}"
        ) from err
    finally:
        cursor.close()
        db.close()

@router.post("/", summary="Create Maquina", tags=["Maquinas"], response_model=APIResponse[MaquinaBase], dependencies=[Depends(get_current_admin_user)])
def create_maquina_endpoint(maquina: MaquinaCreate, db=Depends(get_db)):
    """
    Endpoint to create a new maquina.
    """
    try:
        cursor = db.cursor(dictionary=True)
        insert_query = """
            INSERT INTO maquinas (modelo, id_cliente, ubicacion_cliente, costo_alquiler_mensual)
            VALUES (%s, %s, %s,%s)
        """
        cursor.execute(insert_query, (maquina.modelo, maquina.id_cliente, maquina.ubicacion_cliente, maquina.costo_alquiler_mensual))
        db.commit()

        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to create maquina"
            )

        query = "SELECT * FROM maquinas WHERE id = LAST_INSERT_ID()"
        cursor.execute(query)
        created_maquina = cursor.fetchone()

        return APIResponse(
            success=True,
            data=MaquinaBase(**created_maquina)
        )
    except mysql.connector.Error as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database connection error: {err}"
        ) from err
    finally:
        cursor.close()
        db.close()

@router.put("/{maquina_id}", summary="Update Maquina", tags=["Maquinas"], response_model=APIResponse[MaquinaBase], dependencies=[Depends(get_current_admin_user)])
def update_maquina_endpoint(maquina_id: int, maquina: MaquinaCreate, db=Depends(get_db)):
    """
    Endpoint to update an existing maquina.
    """
    try:
        cursor = db.cursor(dictionary=True)
        update_query = """
            UPDATE maquinas
            SET modelo = %s, id_cliente = %s, ubicacion_cliente = %s, costo_alquiler_mensual = %s
            WHERE id = %s
        """
        cursor.execute(update_query, (maquina.modelo, maquina.id_cliente, maquina.ubicacion_cliente, maquina.costo_alquiler_mensual, maquina_id))
        db.commit()

        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Maquina not found"
            )

        cursor.execute("SELECT * FROM maquinas WHERE id = %s", (maquina_id,))
        updated_maquina = cursor.fetchone()

        return APIResponse(
            success=True,
            data=MaquinaBase(**updated_maquina)
        )
    except mysql.connector.Error as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database connection error: {err}"
        ) from err
    finally:
        cursor.close()
        db.close()

@router.delete("/{maquina_id}", summary="Delete Maquina", tags=["Maquinas"], response_model=APIResponse[MessageResponse], dependencies=[Depends(get_current_admin_user)])
def delete_maquina_endpoint(maquina_id: int, db=Depends(get_db)):
    """
    Endpoint to delete a maquina by its ID.
    """
    try:
        cursor = db.cursor(dictionary=True)
        delete_query = "DELETE FROM maquinas WHERE id = %s"
        cursor.execute(delete_query, (maquina_id,))
        db.commit()

        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Maquina not found"
            )

        return APIResponse(
            success=True,
            data=MessageResponse(message="Maquina deleted successfully")
        )
    except mysql.connector.Error as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database connection error: {err}"
        ) from err
    finally:
        cursor.close()
        db.close()