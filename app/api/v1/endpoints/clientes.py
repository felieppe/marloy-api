from fastapi import APIRouter, Depends, HTTPException, Query, status
import mysql.connector, math

from app.schemas.common import APIResponse, MessageResponse, APIResponsePaginated
from app.schemas.cliente import ClienteBase, ClienteCreate
from app.dependencies import get_db

router = APIRouter()

@router.get("/", summary="Get Clientes", tags=["Clientes"], response_model=APIResponsePaginated[ClienteBase])
def get_clientes_endpoint(page: int = Query(1, ge=1, description="Page number"), page_size: int = Query(10, ge=1, le=100, description="Items per page"), db=Depends(get_db)):
    """
    Endpoint to retrieve all clientes.
    """
    try:
        cursor = db.cursor(dictionary=True)

        count_query = "SELECT COUNT(*) as total FROM clientes"
        cursor.execute(count_query)
        total_items = cursor.fetchone()['total']

        offset = (page - 1) * page_size
        query = "SELECT * FROM clientes LIMIT %s OFFSET %s"
        cursor.execute(query, (page_size, offset))

        clientes = cursor.fetchall()
        total_pages = math.ceil(total_items / page_size) if total_items > 0 else 1

        if not clientes:
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
            data=[ClienteBase(**cliente) for cliente in clientes],
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

@router.get("/{cliente_id}", summary="Get Cliente by ID", tags=["Clientes"], response_model=APIResponse[ClienteBase])
def get_cliente_by_id_endpoint(cliente_id: int, db=Depends(get_db)):
    """
    Endpoint to retrieve a cliente by its ID.
    """
    try:
        cursor = db.cursor(dictionary=True)
        query = "SELECT * FROM clientes WHERE id = %s"
        cursor.execute(query, (cliente_id,))
        cliente = cursor.fetchone()

        if not cliente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cliente not found"
            )

        return APIResponse(
            success=True,
            data=ClienteBase(**cliente)
        )
    except mysql.connector.Error as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database connection error: {err}"
        ) from err
    finally:
        cursor.close()
        db.close()

@router.post("/", summary="Create Cliente", tags=["Clientes"], response_model=APIResponse[ClienteBase])
def create_cliente_endpoint(cliente: ClienteCreate, db=Depends(get_db)):
    """
    Endpoint to create a new cliente.
    """
    try:
        cursor = db.cursor(dictionary=True)
        insert_query = """
            INSERT INTO clientes (nombre, correo, telefono, direccion)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(insert_query, (cliente.nombre, cliente.correo, cliente.telefono, cliente.direccion))
        db.commit()

        cliente_id = cursor.lastrowid
        cliente_data = {**cliente.dict(), "id": cliente_id}

        return APIResponse(
            success=True,
            data=ClienteBase(**cliente_data)
        )
    except mysql.connector.Error as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database connection error: {err}"
        ) from err
    finally:
        cursor.close()
        db.close()

@router.put("/{cliente_id}", summary="Update Cliente", tags=["Clientes"], response_model=APIResponse[ClienteBase])
def update_cliente_endpoint(cliente_id: int, cliente: ClienteCreate, db=Depends(get_db)):
    """
    Endpoint to update an existing cliente.
    """
    try:
        cursor = db.cursor(dictionary=True)
        update_query = """
            UPDATE clientes
            SET nombre = %s, correo = %s, telefono = %s, direccion = %s
            WHERE id = %s
        """
        cursor.execute(update_query, (cliente.nombre, cliente.correo, cliente.telefono, cliente.direccion, cliente_id))
        db.commit()

        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cliente not found"
            )

        return APIResponse(
            success=True,
            data=ClienteBase(**cliente.dict(), id=cliente_id)
        )
    except mysql.connector.Error as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database connection error: {err}"
        ) from err
    finally:
        cursor.close()
        db.close()

@router.delete("/{cliente_id}", summary="Delete Cliente", tags=["Clientes"], response_model=MessageResponse)
def delete_cliente_endpoint(cliente_id: int, db=Depends(get_db)):
    """
    Endpoint to delete a cliente by its ID.
    """
    try:
        cursor = db.cursor(dictionary=True)
        delete_query = "DELETE FROM clientes WHERE id = %s"
        cursor.execute(delete_query, (cliente_id,))
        db.commit()

        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cliente not found"
            )

        return MessageResponse(
            success=True,
            message="Cliente deleted successfully"
        )
    except mysql.connector.Error as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database connection error: {err}"
        ) from err
    finally:
        cursor.close()
        db.close()