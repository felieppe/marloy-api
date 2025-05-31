from fastapi import APIRouter, Depends, HTTPException, Query, status
import mysql.connector, math

from app.schemas.common import APIResponse, MessageResponse, APIResponsePaginated
from app.schemas.tecnico import TecnicoBase, TecnicoCreate
from app.dependencies import get_db, get_current_admin_user

router = APIRouter()

@router.get("/", summary="Get Tecnicos", tags=["Tecnicos"], response_model=APIResponsePaginated[TecnicoBase], dependencies=[Depends(get_current_admin_user)])
def get_tecnicos_endpoint(page: int = Query(1, ge=1, description="Page number"), page_size: int = Query(10, ge=1, le=100, description="Items per page"), db=Depends(get_db)):
    """
    Endpoint to retrieve all tecnicos.
    """
    try:
        cursor = db.cursor(dictionary=True)

        count_query = "SELECT COUNT(*) as total FROM tecnicos"
        cursor.execute(count_query)
        total_items = cursor.fetchone()['total']

        offset = (page - 1) * page_size
        query = "SELECT * FROM tecnicos LIMIT %s OFFSET %s"
        cursor.execute(query, (page_size, offset))

        tecnicos = cursor.fetchall()
        total_pages = math.ceil(total_items / page_size) if total_items > 0 else 1

        if not tecnicos:
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
            data=[TecnicoBase(**tecnico) for tecnico in tecnicos],
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

@router.get("/{tecnico_ci}", summary="Get Tecnico by CI", tags=["Tecnicos"], response_model=APIResponse[TecnicoBase], dependencies=[Depends(get_current_admin_user)])
def get_tecnico_by_id_endpoint(tecnico_ci: int, db=Depends(get_db)):
    """
    Endpoint to retrieve a tecnico by its CI.
    """
    try:
        cursor = db.cursor(dictionary=True)
        query = "SELECT * FROM tecnicos WHERE ci = %s"
        cursor.execute(query, (tecnico_ci,))
        tecnico = cursor.fetchone()

        if not tecnico:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tecnico not found"
            )

        return APIResponse(
            success=True,
            data=TecnicoBase(**tecnico)
        )
    except mysql.connector.Error as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database connection error: {err}"
        ) from err
    finally:
        cursor.close()
        db.close()

@router.post("/", summary="Create Tecnico", tags=["Tecnicos"], response_model=APIResponse[TecnicoBase], dependencies=[Depends(get_current_admin_user)])
def create_tecnico_endpoint(tecnico: TecnicoCreate, db=Depends(get_db)):
    """
    Endpoint to create a new tecnico.
    """
    try:
        cursor = db.cursor(dictionary=True)
        insert_query = """
            INSERT INTO tecnicos (ci, nombre, apellido, telefono)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(insert_query, (tecnico.ci, tecnico.nombre, tecnico.apellido, tecnico.telefono))
        db.commit()

        # Retrieve the created tecnico
        cursor.execute("SELECT * FROM tecnicos WHERE ci = %s", (tecnico.ci,))
        created_tecnico = cursor.fetchone()

        if not created_tecnico:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create tecnico"
            )

        return APIResponse(
            success=True,
            data=TecnicoBase(**created_tecnico)
        )
    except mysql.connector.Error as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database connection error: {err}"
        ) from err
    finally:
        cursor.close()
        db.close()

@router.put("/{tecnico_id}", summary="Update Tecnico", tags=["Tecnicos"], response_model=APIResponse[TecnicoBase], dependencies=[Depends(get_current_admin_user)])
def update_tecnico_endpoint(tecnico_id: int, tecnico: TecnicoCreate, db=Depends(get_db)):
    """
    Endpoint to update an existing tecnico.
    """
    try:
        cursor = db.cursor(dictionary=True)
        update_query = """
            UPDATE tecnicos
            SET nombre = %s, apellido = %s, telefono = ^s
            WHERE ci = %s
        """
        cursor.execute(update_query, (tecnico.nombre, tecnico.apellido, tecnico.telefono, tecnico_id))
        db.commit()

        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tecnico not found"
            )

        # Retrieve the updated tecnico
        cursor.execute("SELECT * FROM tecnicos WHERE ci = %s", (tecnico_id,))
        updated_tecnico = cursor.fetchone()

        return APIResponse(
            success=True,
            data=TecnicoBase(**updated_tecnico)
        )
    except mysql.connector.Error as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database connection error: {err}"
        ) from err
    finally:
        cursor.close()
        db.close()

@router.delete("/{tecnico_id}", summary="Delete Tecnico", tags=["Tecnicos"], response_model=MessageResponse, dependencies=[Depends(get_current_admin_user)])
def delete_tecnico_endpoint(tecnico_id: int, db=Depends(get_db)):
    """
    Endpoint to delete a tecnico by its CI.
    """
    try:
        cursor = db.cursor(dictionary=True)
        delete_query = "DELETE FROM tecnicos WHERE ci = %s"
        cursor.execute(delete_query, (tecnico_id,))
        db.commit()

        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tecnico not found"
            )

        return MessageResponse(
            success=True,
            message="Tecnico deleted successfully"
        )
    except mysql.connector.Error as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database connection error: {err}"
        ) from err
    finally:
        cursor.close()
        db.close()