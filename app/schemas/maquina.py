"""
    Schemas for Maquina (Machine) management in a rental system.
"""

from pydantic import BaseModel, Field

class MaquinaBase(BaseModel):
    """
    Modelo base para la máquina.
    Este modelo define los campos comunes para las máquinas en el sistema de alquiler.

    Args:
        BaseModel (pydantic.BaseModel): Clase base de Pydantic para la validación de datos.

    Attributes:
        id (int): ID único de la máquina.
        modelo (str): Modelo de la máquina, debe tener una longitud máxima.
        id_cliente (int): ID del cliente al que se alquila la máquina, debe ser mayor que cero.
        ubicacion_cliente (str):
        Ubicación del cliente donde se encuentra la máquina, debe tener una longitud máxima.
        costo_alquiler_mensual (float):
        Costo mensual del alquiler de la máquina, debe ser mayor que cero.
    """

    id: int = Field(..., description="ID único de la máquina.", ge=1, example=1)
    modelo: str = Field(..., max_length=100, example="CM-Pro 5000")
    id_cliente: int = Field(..., gt=0, example=1)
    ubicacion_cliente: str = Field(..., max_length=255, example="Hall Principal")
    costo_alquiler_mensual: float = Field(..., gt=0, example=150.00)

class MaquinaCreate(BaseModel):
    """
    Modelo para crear una nueva máquina.
    Este modelo se utiliza para validar los datos al crear una nueva máquina.

    Args:
        BaseModel (pydantic.BaseModel): Clase base de Pydantic para la validación de datos.

    Attributes:
        modelo (str | None): Modelo de la máquina, opcional.
        id_cliente (int | None): 
        ID del cliente al que se alquila la máquina, debe ser mayor que cero.
        ubicacion_cliente (str | None): 
        Ubicación del cliente donde se encuentra la máquina, opcional.
        costo_alquiler_mensual (float | None): 
        Costo mensual del alquiler de la máquina, debe ser mayor que cero.
    """

    modelo: str | None = Field(None, max_length=100, example="CM-Pro 6000")
    id_cliente: int | None = Field(None, gt=0, example=2)
    ubicacion_cliente: str | None = Field(None, max_length=255, example="Comedor")
    costo_alquiler_mensual: float | None = Field(None, gt=0, example=175.00)

class MaquinaUpdate(MaquinaCreate):
    """
    Modelo para actualizar una máquina existente.
    Este modelo se utiliza para validar los datos al actualizar una máquina.

    Args:
        MaquinaCreate (MaquinaCreate): Modelo para crear una nueva máquina.
        
    Attributes:
        modelo (str | None): Modelo de la máquina, opcional.
        id_cliente (int | None): 
        ID del cliente al que se alquila la máquina, debe ser mayor que cero.
        ubicacion_cliente (str | None): 
        Ubicación del cliente donde se encuentra la máquina, opcional.
        costo_alquiler_mensual (float | None): 
        Costo mensual del alquiler de la máquina, debe ser mayor que cero.
    """
