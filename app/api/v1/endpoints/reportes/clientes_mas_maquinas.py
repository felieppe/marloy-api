""" Get clients with the most machines.
    Endpoint to retrieve the clients with the most machines.

    Raises:
        HTTPException: If there is a database connection error or if no client data is found.

    Returns:
        APIResponse: A response containing a list of clients with their machine counts.
"""

import mysql.connector
from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.schemas.common import APIResponse
from app.schemas.reporte import ClientesMasMaquinasResponse
from app.dependencies import get_db, get_current_admin_user

router = APIRouter()

@router.get(
    "/",
    summary="Get Clients with Most Machines",
    tags=["Reportes"],
    response_model=APIResponse[list[ClientesMasMaquinasResponse]],
    dependencies=[Depends(get_current_admin_user)]
)
def get_clients_with_most_machines(
    limit: int = Query(10, ge=1, description="Max return of clients"),
    db=Depends(get_db)
):
    """
    Endpoint to retrieve the clients with the most machines.
    """
    try:
        cursor = db.cursor(dictionary=True)

        query = """
            SELECT
                c.nombre AS cliente_nombre,
                COUNT(m.id) AS total_maquinas
            FROM clientes c
            JOIN maquinas m ON c.id = m.id_cliente
            GROUP BY c.id, c.nombre
            ORDER BY total_maquinas DESC
            LIMIT %s;
        """
        cursor.execute(query, (limit,))
        result = cursor.fetchall()

        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No client data found."
            )

        response_data = [ClientesMasMaquinasResponse(**item) for item in result]
        return APIResponse(success=True, data=response_data)

    except mysql.connector.Error as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database connection error: {err}"
        ) from err
    finally:
        cursor.close()
        db.close()
