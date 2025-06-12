"""
    Schemas for report responses in the application.
"""

from pydantic import BaseModel, Field

class ReporteBase(BaseModel):
    """
    Modelo base para los reportes.
    Este modelo define los campos comunes para los reportes en el sistema.

    Args:
        BaseModel (pydantic.BaseModel): Clase base de Pydantic para la validación de datos.
    """

class FacturacionMensualResponse(ReporteBase):
    """
    Modelo para la respuesta del reporte de facturación mensual.
    Este modelo se utiliza para representar la facturación mensual
    de un cliente, incluyendo el total de alquiler y el total de insumos consumidos.

    Args:
        ReporteBase (ReporteBase): Modelo base para los reportes.
        
    Attributes:
        cliente_id (int): ID del cliente.
        nombre_cliente (str): Nombre del cliente.
        total_alquiler (float): Total a cobrar por alquiler
        de máquinas para el mes/año especificado.
        total_insumos (float): Total a cobrar por insumos consumidos para el mes/año especificado.
        total_a_cobrar (float): Suma del total de alquiler y el total de insumos.
    """

    cliente_id: int = Field(..., description="ID del cliente.")
    nombre_cliente: str = Field(..., description="Nombre del cliente.")
    total_alquiler: float = Field(
        ...,
        description="Total a cobrar por alquiler de máquinas para el mes/año especificado."
    )
    total_insumos: float = Field(
        ...,
        description="Total a cobrar por insumos consumidos para el mes/año especificado."
    )
    total_a_cobrar: float = Field(
        ...,
        description="Suma del total de alquiler y el total de insumos."
    )

class InsumosMasConsumidosResponse(ReporteBase):
    """
    Modelo para la respuesta del reporte de insumos más consumidos.
    Este modelo se utiliza para representar los insumos más consumidos
    en un periodo específico, incluyendo la descripción del insumo,
    la cantidad total consumida y el costo total.

    Args:
        ReporteBase (ReporteBase): Modelo base para los reportes.

    Attributes:
        insumo_descripcion (str): Descripción del insumo.
        total_cantidad (float): Cantidad total consumida del insumo en el periodo especificado.
        total_costo (float): Costo total de los insumos consumidos en el periodo especificado.
    """

    insumo_descripcion: str = Field(..., description="Descripción del insumo.")
    total_cantidad: float = Field(
        ...,
        description="Cantidad total consumida del insumo en el periodo especificado."
    )
    total_costo: float = Field(
        ...,
        description="Costo total de los insumos consumidos en el periodo especificado."
    )

class TecnicosMasMantenimientosResponse(ReporteBase):
    """
    Modelo para la respuesta del reporte de técnicos con más mantenimientos.
    Este modelo se utiliza para representar los técnicos que han realizado más mantenimientos

    Args:
        ReporteBase (ReporteBase): Modelo base para los reportes.
        
    Attributes:
        tecnico_nombre (str): Nombre del técnico.
        mantenimientos_realizados (int): Cantidad de mantenimientos realizados
        por el técnico en el periodo especificado.
    """

    tecnico_nombre: str = Field(..., description="Nombre del técnico.")
    mantenimientos_realizados: int = Field(
        ...,
        description="""
        Cantidad de mantenimientos realizados por el técnico en el periodo especificado.
        """
    )

class ClientesMasMaquinasResponse(ReporteBase):
    """
    Modelo para la respuesta del reporte de clientes con más máquinas alquiladas.
    Este modelo se utiliza para representar los clientes que han alquilado más máquinas

    Args:
        ReporteBase (ReporteBase): Modelo base para los reportes.
        
    Attributes:
        cliente_nombre (str): Nombre del cliente.
        total_maquinas (int): Cantidad total de máquinas alquiladas
        por el cliente en el periodo especificado.
    """

    cliente_nombre: str = Field(..., description="Nombre del cliente.")
    total_maquinas: int = Field(
        ...,
        description="""
        Cantidad total de máquinas alquiladas por el cliente en el periodo especificado.
        """
    )
