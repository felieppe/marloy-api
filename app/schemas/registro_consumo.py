"""
    Schemas for RegistroConsumo (Consumption Record) in a manufacturing context.
"""

from datetime import datetime
from pydantic import BaseModel, Field

class RegistroConsumoBase(BaseModel):
    """
    Modelo base para el registro de consumo de insumos en máquinas.
    Este modelo define los campos comunes para los registros de consumo en el sistema.

    Args:
        BaseModel (pydantic.BaseModel): Clase base de Pydantic para la validación de datos.
        
    Attributes:
        id (int | None): ID único del registro de consumo, opcional para creación.
        id_maquina (int): ID de la máquina asociada al consumo, debe ser mayor que cero.
        id_insumo (int): ID del insumo consumido, debe ser mayor que cero.
        fecha (datetime): Fecha y hora del consumo, debe ser una fecha válida.
        cantidad_usada (float): Cantidad del insumo consumido, debe ser mayor que cero.
    """

    id: int | None = Field(None, description="ID único del registro de consumo.")
    id_maquina: int = Field(..., gt=0, example=1)
    id_insumo: int = Field(..., gt=0, example=1)
    fecha: datetime = Field(..., example="2025-05-23T10:00:00")
    cantidad_usada: float = Field(..., gt=0, example=100.0)

class RegistroConsumoCreate(BaseModel):
    """
    Modelo para crear un nuevo registro de consumo.
    Este modelo se utiliza para validar los datos al crear un nuevo registro de consumo.

    Args:
        BaseModel (pydantic.BaseModel): Clase base de Pydantic para la validación de datos.

    Attributes:
        id_maquina (int): ID de la máquina asociada al consumo, debe ser mayor que cero.
        id_insumo (int): ID del insumo consumido, debe ser mayor que cero.
        fecha (datetime): Fecha y hora del consumo, debe ser una fecha válida.
        cantidad_usada (float): Cantidad del insumo consumido, debe ser mayor que cero.
    """
    id_maquina: int = Field(..., gt=0, example=1)
    id_insumo: int = Field(..., gt=0, example=1)
    fecha: datetime = Field(..., example="2025-05-23T10:00:00")
    cantidad_usada: float = Field(..., gt=0, example=100.0)

class RegistroConsumoUpdate(BaseModel):
    """
    Modelo para actualizar un registro de consumo existente.
    Este modelo se utiliza para validar los datos al actualizar un registro de consumo.

    Args:
        BaseModel (pydantic.BaseModel): Clase base de Pydantic para la validación de datos.
        
    Attributes:
        id_maquina (int | None): ID de la máquina asociada al consumo, opcional.
        id_insumo (int | None): ID del insumo consumido, opcional.
        fecha (datetime | None): Fecha y hora del consumo, opcional.
        cantidad_usada (float | None): Cantidad del insumo consumido, debe ser mayor que cero.
    """

    cantidad_usada: float | None = Field(None, gt=0, example=120.0)
