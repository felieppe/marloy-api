"""Endpoint to retrieve the most consumed supplies.

    Raises:
        HTTPException: If there is a database connection error or if no consumption data is found.

    Returns:
        APIResponse: A response containing a list
        of the most consumed supplies with their total quantities and costs.
"""

import mysql.connector
from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.schemas.common import APIResponse
from app.schemas.reporte import InsumosMasConsumidosResponse
from app.dependencies import get_db, get_current_admin_user

router = APIRouter()

@router.get(
    "/",
    summary="Get Most Consumed Supplies",
    tags=["Reportes"],
    response_model=APIResponse[list[InsumosMasConsumidosResponse]],
    dependencies=[Depends(get_current_admin_user)]
)
def get_most_consumed_supplies(
    limit: int = Query(10, ge=1, description="Max return of insumos"),
    db=Depends(get_db)
):
    """
    Endpoint to retrieve the most consumed supplies for a specific month and year.
    """
    try:
        cursor = db.cursor(dictionary=True)

        query = """
            SELECT
                i.descripcion AS insumo_descripcion,
                SUM(rc.cantidad_usada) AS total_cantidad,
                SUM(rc.cantidad_usada * i.precio_unitario) AS total_costo
            FROM registro_consumo rc
            JOIN insumos i ON rc.id_insumo = i.id
            GROUP BY i.id, i.descripcion
            ORDER BY total_cantidad DESC, total_costo DESC
            LIMIT %s;
        """
        cursor.execute(query, (limit,))
        result = cursor.fetchall()

        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No consumption data found."
            )

        response_data = [InsumosMasConsumidosResponse(**item) for item in result]

        return APIResponse(success=True, data=response_data)

    except mysql.connector.Error as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database connection error: {err}"
        ) from err
    finally:
        cursor.close()
        db.close()
