from fastapi import APIRouter, Depends, HTTPException, Query, status
import mysql.connector, math

from app.schemas.common import APIResponse, MessageResponse
from app.schemas.reporte import FacturacionMensualResponse
from app.dependencies import get_db

router = APIRouter()

@router.get("/{cliente_id}", summary="Get Monthly Billing Report", tags=["Reportes"], response_model=APIResponse[FacturacionMensualResponse])
def get_monthly_billing_report(cliente_id: int, month: int = Query(..., ge=1, le=12, description="Mes para el reporte (1-12)"), year: int = Query(..., ge=2000, description="Año para el reporte (ej. 2025)"), db=Depends(get_db) ):
    """
    Endpoint to retrieve the monthly billing report for a specific client.
    """
    try:
        cursor = db.cursor(dictionary=True)

        query = """
            SELECT 
                c.id AS cliente_id,
                c.nombre AS nombre_cliente,
                SUM(m.costo_alquiler_mensual) AS total_alquiler,
                SUM(i.precio_unitario * rc.cantidad_usada) AS total_insumos,
                SUM(m.costo_alquiler_mensual + (i.precio_unitario * rc.cantidad_usada)) AS total_a_cobrar
            FROM clientes c
            LEFT JOIN maquinas m ON c.id = m.id_cliente
            LEFT JOIN registro_consumo rc ON m.id = rc.id_maquina
            LEFT JOIN insumos i ON rc.id_insumo = i.id
            WHERE c.id = %s AND MONTH(rc.fecha) = %s AND YEAR(rc.fecha) = %s
            GROUP BY c.id;
        """
        cursor.execute(query, (cliente_id, month, year))
        result = cursor.fetchone()

        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No billing data found for the specified client and date."
            )

        response_data = FacturacionMensualResponse(**result)
        return APIResponse(success=True, data=response_data)

    except mysql.connector.Error as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database connection error: {err}"
        ) from err
    finally:
        cursor.close()
        db.close()