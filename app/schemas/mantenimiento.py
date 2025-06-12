"""
    Schemas for Mantenimiento (Maintenance) operations.
"""

from datetime import datetime
from pydantic import BaseModel, Field

class MantenimientoBase(BaseModel):
    """
    Modelo base para el mantenimiento de máquinas.
    Este modelo define los campos comunes para el mantenimiento de máquinas en el sistema.

    Args:
        BaseModel (pydantic.BaseModel): Clase base de Pydantic para la validación de datos.
        
    Attributes:
        id (int | None): ID único del mantenimiento, opcional para creación.
        id_maquina (int): ID de la máquina asociada al mantenimiento, debe ser mayor que cero.
        ci_tecnico (str): Cédula de identidad del técnico que realiza el mantenimiento.
        tipo (str): Tipo de mantenimiento (e.g., Preventivo, Correctivo),
        debe tener una longitud máxima.
        fecha (datetime): Fecha y hora del mantenimiento, debe ser una fecha válida.
        observaciones (str | None): Observaciones del mantenimiento, opcional.
    """

    id: int | None = Field(None, gt=0, example=1, description="ID único del mantenimiento.")
    id_maquina: int = Field(..., gt=0, example=1)
    ci_tecnico: str = Field(..., max_length=20, example="1234567-8")
    tipo: str = Field(..., max_length=100, example="Preventivo")
    fecha: datetime = Field(..., example="2025-05-23T14:30:00")
    observaciones: str | None = Field(
        None,
        example="Se realizó limpieza y lubricación de componentes."
    )

class MantenimientoCreate(BaseModel):
    """
    Modelo para crear un nuevo mantenimiento.
    Este modelo se utiliza para validar los datos al crear un nuevo mantenimiento.

    Args:
        BaseModel (pydantic.BaseModel): Clase base de Pydantic para la validación de datos.

    Attributes:
        id_maquina (int): ID de la máquina asociada al mantenimiento, debe ser mayor que cero.
        ci_tecnico (str): Cédula de identidad del técnico que realiza el mantenimiento.
        tipo (str): Tipo de mantenimiento (e.g., Preventivo, Correctivo), 
        debe tener una longitud máxima.
        fecha (datetime): Fecha y hora del mantenimiento, debe ser una fecha válida.
        observaciones (str | None): Observaciones del mantenimiento, opcional.
    """

    id_maquina: int = Field(..., gt=0, example=1)
    ci_tecnico: str = Field(..., max_length=20, example="1234567-8")
    tipo: str = Field(..., max_length=100, example="Preventivo")
    fecha: datetime = Field(..., example="2025-05-23T14:30:00")
    observaciones: str | None = Field(
        None,
        example="Se realizó limpieza y lubricación de componentes."
    )

class MantenimientoUpdate(MantenimientoCreate):
    """
    Modelo para actualizar un mantenimiento existente.
    Este modelo se utiliza para validar los datos al actualizar un mantenimiento.

    Args:
        MantenimientoCreate (MantenimientoCreate): Modelo para crear un nuevo mantenimiento.
        
    Attributes:
        id (int): ID único del mantenimiento, debe ser mayor que cero.
        id_maquina (int): ID de la máquina asociada al mantenimiento, debe ser mayor que cero.
        ci_tecnico (str): Cédula de identidad del técnico que realiza el mantenimiento.
        tipo (str): Tipo de mantenimiento (e.g., Preventivo, Correctivo), 
        debe tener una longitud máxima.
        fecha (datetime): Fecha y hora del mantenimiento, debe ser una fecha válida.
        observaciones (str | None): Observaciones del mantenimiento, opcional.
    """
