"""
    Schemas for Tecnico (Technician) entity in the application.
"""

from pydantic import BaseModel, Field

class TecnicoBase(BaseModel):
    """
    Modelo base para el técnico.
    Este modelo define los campos comunes para los técnicos en el sistema.

    Args:
        BaseModel (pydantic.BaseModel): Clase base de Pydantic para la validación de datos.
        
    Attributes:
        ci (str): Cédula de identidad del técnico, debe tener un formato específico.
        nombre (str): Nombre del técnico, debe tener una longitud máxima.
        apellido (str): Apellido del técnico, debe tener una longitud máxima.
        telefono (str | None): Número de teléfono del técnico, opcional y con longitud máxima.
    """

    ci: str = Field(..., max_length=20, example="1234567-8")
    nombre: str = Field(..., max_length=100, example="Juan")
    apellido: str = Field(..., max_length=100, example="Pérez")
    telefono: str | None = Field(None, max_length=50, example="098765432")

class TecnicoCreate(TecnicoBase):
    """
    Modelo para crear un nuevo técnico.
    Este modelo se utiliza para validar los datos al crear un nuevo técnico.

    Args:
        TecnicoBase (TecnicoBase): Modelo base para el técnico.

    Attributes:
        ci (str | None): Cédula de identidad del técnico, opcional.
        nombre (str | None): Nombre del técnico, opcional.
        apellido (str | None): Apellido del técnico, opcional.
        telefono (str | None): Número de teléfono del técnico, opcional.
    """

class TecnicoUpdate(BaseModel):
    """
    Modelo para actualizar un técnico existente.
    Este modelo se utiliza para validar los datos al actualizar un técnico.

    Args:
        BaseModel (pydantic.BaseModel): Clase base de Pydantic para la validación de datos.

    Attributes:
        nombre (str | None): Nombre del técnico, opcional.
        apellido (str | None): Apellido del técnico, opcional.
        telefono (str | None): Número de teléfono del técnico, opcional.
    """

    nombre: str | None = Field(None, max_length=100, example="Juan Carlos")
    apellido: str | None = Field(None, max_length=100, example="Pérez Gómez")
    telefono: str | None = Field(None, max_length=50, example="099112233")
