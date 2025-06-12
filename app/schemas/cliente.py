"""
    Esquema de datos para clientes en el sistema.
"""

from pydantic import BaseModel, Field, EmailStr

class ClienteBase(BaseModel):
    """
    Modelo base para los clientes.
    Este modelo define los campos comunes para los clientes en el sistema.

    Args:
        BaseModel (pydantic.BaseModel): Clase base de Pydantic para la validación de datos.

    Attributes:
        id (int): ID único del cliente.
        nombre (str): Nombre del cliente.
        direccion (str): Dirección del cliente.
        telefono (str | None): Número de teléfono del cliente, opcional.
        correo (EmailStr | None): Correo electrónico del cliente, opcional.
    """

    id: int = Field(..., description="ID único del cliente.", ge=1)
    nombre: str = Field(..., max_length=255, example="Oficinas Centrales XYZ")
    direccion: str = Field(..., max_length=255, example="Av. Libertador 2000")
    telefono: str | None = Field(None, max_length=50, example="099123456")
    correo: EmailStr | None = Field(None, example="contacto@xyz.com")

class ClienteCreate(BaseModel):
    """
    Modelo para crear un nuevo cliente.
    Este modelo se utiliza para validar los datos al crear un nuevo cliente.

    Args:
        BaseModel (pydantic.BaseModel): Clase base de Pydantic para la validación de datos.
        
    Attributes:
        nombre (str): Nombre del cliente.
        direccion (str): Dirección del cliente.
        telefono (str | None): Número de teléfono del cliente, opcional.
        correo (EmailStr | None): Correo electrónico del cliente, opcional.
    """

    nombre: str = Field(..., max_length=255, example="Oficinas Centrales XYZ")
    direccion: str = Field(..., max_length=255, example="Av. Libertador 2000")
    telefono: str | None = Field(None, max_length=50, example="099123456")
    correo: EmailStr | None = Field(None, example="contacto@xyz.com")

class ClienteUpdate(ClienteCreate):
    """
    Modelo para actualizar un cliente existente.
    Este modelo se utiliza para validar los datos al actualizar un cliente.

    Args:
        ClienteCreate (ClienteCreate): Modelo base para crear un cliente.
    
    Attributes:
        nombre (str): Nombre del cliente.
        direccion (str): Dirección del cliente.
        telefono (str | None): Número de teléfono del cliente, opcional.
        correo (EmailStr | None): Correo electrónico del cliente, opcional.
    """
