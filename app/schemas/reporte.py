from pydantic import BaseModel, Field

class ReporteBase(BaseModel):
    pass

class FacturacionMensualResponse(ReporteBase):
    cliente_id: int = Field(..., description="ID del cliente.")
    nombre_cliente: str = Field(..., description="Nombre del cliente.")
    total_alquiler: float = Field(..., description="Total a cobrar por alquiler de máquinas para el mes/año especificado.")
    total_insumos: float = Field(..., description="Total a cobrar por insumos consumidos para el mes/año especificado.")
    total_a_cobrar: float = Field(..., description="Suma del total de alquiler y el total de insumos.")

class InsumosMasConsumidosResponse(ReporteBase):
    insumo_descripcion: str = Field(..., description="Descripción del insumo.")
    total_cantidad: float = Field(..., description="Cantidad total consumida del insumo en el periodo especificado.")
    total_costo: float = Field(..., description="Costo total de los insumos consumidos en el periodo especificado.")

class TecnicosMasMantenimientosResponse(ReporteBase):
    tecnico_nombre: str = Field(..., description="Nombre del técnico.")
    mantenimientos_realizados: int = Field(..., description="Cantidad de mantenimientos realizados por el técnico en el periodo especificado.")

class ClientesMasMaquinasResponse(ReporteBase):
    cliente_nombre: str = Field(..., description="Nombre del cliente.")
    total_maquinas: int = Field(..., description="Cantidad total de máquinas alquiladas por el cliente en el periodo especificado.")