"""
    Schemas for user management in the application.
"""

from pydantic import BaseModel, EmailStr, Field

class UserBase(BaseModel):
    """
    Modelo base para el usuario.
    Este modelo define los campos comunes para los usuarios en el sistema.

    Args:
        BaseModel (pydantic.BaseModel): Clase base de Pydantic para la validación de datos.
        
    Attributes:
        correo (EmailStr): Correo electrónico del usuario, debe tener un formato válido.
        es_administrador (bool): Indica si el usuario es administrador. Por defecto es False.
    """

    correo: EmailStr = Field(..., example="usuario@empresa.com")
    es_administrador: bool = Field(False, description="Indica si el usuario es administrador.")

class UserCreate(UserBase):
    """
    Modelo para crear un nuevo usuario.
    Este modelo se utiliza para validar los datos al crear un nuevo usuario.

    Args:
        UserBase (UserBase): Modelo base para el usuario.

    Attributes:
        contraseña (str): Contraseña del usuario, debe tener al menos 8 caracteres.
    """

    contraseña: str = Field(        # pylint: disable=non-ascii-name
        ...,
        example="password",
        min_length=8,
        description="Contraseña del usuario, debe tener al menos 8 caracteres."
    )

class UserUpdate(BaseModel):
    """
    Modelo para actualizar un usuario existente.
    Este modelo se utiliza para validar los datos al actualizar un usuario.

    Args:
        BaseModel (_type_): _description_
        
    Attributes:
        es_administrador (bool): Indica si el usuario es administrador. Por defecto es False.
    """

    es_administrador: bool = Field(..., description="Indica si el usuario es administrador.")
