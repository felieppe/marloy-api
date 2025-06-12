"""Endpoint to retrieve technicians with the most maintenance records.
    This endpoint returns a list of technicians along 
    with the count of maintenance records they have handled,

    Raises:
        HTTPException: If there is a database connection error or if no maintenance data is found.

    Returns:
        APIResponse: A response containing a list of technicians with their maintenance counts.
"""

import mysql.connector
from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.schemas.common import APIResponse
from app.schemas.reporte import TecnicosMasMantenimientosResponse
from app.dependencies import get_db, get_current_admin_user

router = APIRouter()

@router.get(
    "/",
    summary="Get Technicians with Most Maintenances",
    tags=["Reportes"],
    response_model=APIResponse[list[TecnicosMasMantenimientosResponse]],
    dependencies=[Depends(get_current_admin_user)]
)
def get_technicians_with_most_maintenances(
    limit: int = Query(10, ge=1, description="Max return of technicians"),
    db=Depends(get_db)
):
    """
    Endpoint to retrieve the technicians with the most maintenance records.
    """
    try:
        cursor = db.cursor(dictionary=True)

        query = """
            SELECT
                CONCAT(t.nombre, ' ', t.apellido) AS tecnico_nombre,
                COUNT(m.id) AS mantenimientos_realizados
            FROM tecnicos t
            JOIN mantenimientos m ON t.ci = m.ci_tecnico
            GROUP BY t.ci, t.nombre, t.apellido
            ORDER BY mantenimientos_realizados DESC
            LIMIT %s;
        """
        cursor.execute(query, (limit,))
        result = cursor.fetchall()

        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No maintenance data found."
            )

        response_data = [TecnicosMasMantenimientosResponse(**item) for item in result]
        return APIResponse(success=True, data=response_data)

    except mysql.connector.Error as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database connection error: {err}"
        ) from err
    finally:
        cursor.close()
        db.close()
