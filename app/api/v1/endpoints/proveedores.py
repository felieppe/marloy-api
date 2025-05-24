from fastapi import APIRouter, Depends, HTTPException, status
import mysql.connector

from app.schemas.common import APIResponse, MessageResponse
from app.schemas.proveedor import ProveedorBase, ProveedorCreate
from app.dependencies import get_db

router = APIRouter()

@router.get("/", summary="Get Proveedores", tags=["Proveedores"], response_model=APIResponse[list[ProveedorBase]])
def get_proveedores_endpoint(db=Depends(get_db)):
    """
    Endpoint to retrieve all proveedores.
    """
    try:
        cursor = db.cursor(dictionary=True)
        query = "SELECT * FROM proveedores"
        cursor.execute(query)

        proveedores = cursor.fetchall()
        if not proveedores:
            return APIResponse(success=True, data=[])

        return APIResponse(
            success=True,
            data=[ProveedorBase(**proveedor) for proveedor in proveedores]
        )
    except mysql.connector.Error as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database connection error: {err}"
        ) from err
    finally:
        cursor.close()
        db.close()
        
@router.get("/{proveedor_id}", summary="Get Proveedor by ID", tags=["Proveedores"], response_model=APIResponse[ProveedorBase])
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
        
@router.post("/", summary="Create Proveedor", tags=["Proveedores"], response_model=APIResponse[ProveedorBase])
def create_proveedor_endpoint(proveedor: ProveedorCreate, db=Depends(get_db)):
    """
    Endpoint to create a new proveedor.
    """
    try:
        cursor = db.cursor(dictionary=True)
        query = "INSERT INTO proveedores (nombre, contacto) VALUES (%s, %s)"
        cursor.execute(query, (proveedor.nombre, proveedor.contacto))
        db.commit()

        proveedor.id = cursor.lastrowid
        return APIResponse(
            success=True,
            data=ProveedorBase(**proveedor.dict())
        )
    except mysql.connector.Error as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database connection error: {err}"
        ) from err
    finally:
        cursor.close()
        db.close()
        
@router.put("/{proveedor_id}", summary="Update Proveedor", tags=["Proveedores"], response_model=APIResponse[ProveedorBase])
def update_proveedor_endpoint(proveedor_id: int, proveedor: ProveedorBase, db=Depends(get_db)):
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
            data=ProveedorBase(**proveedor.dict())
        )
    except mysql.connector.Error as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database connection error: {err}"
        ) from err
    finally:
        cursor.close()
        db.close()
        
@router.delete("/{proveedor_id}", summary="Delete Proveedor", tags=["Proveedores"], response_model=APIResponse[MessageResponse])
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