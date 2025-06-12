"""
    Proveedor schemas for FastAPI application.
    This module defines the Pydantic models for creating, updating, and retrieving
"""

from pydantic import BaseModel, Field, ConfigDict

class ProveedorBase(BaseModel):
    """
    Modelo base para los proveedores.
    Este modelo define los campos comunes para los proveedores en el sistema.

    Args:
        BaseModel (pydantic.BaseModel): Clase base de Pydantic para la validación de datos.

    Attributes:
        id (int): ID único del proveedor.
        nombre (str): Nombre del proveedor, debe tener una longitud máxima.
        contacto (str | None): Información de contacto del proveedor, opcional.
    """

    id: int = Field(..., description="ID único del proveedor.", ge=1)
    nombre: str = Field(..., max_length=255, example="Distribuidora Café Express")
    contacto: str | None = Field(None, max_length=255, example="info@cafexpress.com")

class ProveedorCreate(ProveedorBase):
    """
    Modelo para crear un nuevo proveedor.
    Este modelo se utiliza para validar los datos al crear un nuevo proveedor.

    Args:
        ProveedorBase (ProveedorBase): Modelo base para los proveedores.

    Attributes:
        id (int | None): ID único del proveedor, opcional.
        Se genera automáticamente al crear el proveedor.
        model_config (ConfigDict): Configuración para excluir el campo 'id' en la creación.
    """

    id: int | None = Field(
        None,
        description="ID único del proveedor. Se genera automáticamente al crear el proveedor.",
        ge=1
    )
    model_config = ConfigDict(exclude={'id'})

class ProveedorUpdate(ProveedorBase):
    """
    Modelo para actualizar un proveedor existente.
    Este modelo se utiliza para validar los datos al actualizar un proveedor.

    Args:
        ProveedorBase (ProveedorBase): Modelo base para los proveedores.

    Attributes:
        nombre (str | None): Nombre del proveedor, opcional.
        contacto (str | None): Información de contacto del proveedor, opcional.
    """

    nombre: str | None = Field(None, max_length=255, example="Distribuidora Café Express S.A.")
    contacto: str | None = Field(None, max_length=255, example="nuevo.contacto@cafexpress.com")
