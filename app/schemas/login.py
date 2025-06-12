"""
    Schemas for user login and authentication.
    This module defines the Pydantic models used for user login operations,
"""

from pydantic import BaseModel, EmailStr, Field

class LoginBase(BaseModel):
    """
    Modelo base para el inicio de sesión de usuarios.
    Este modelo define los campos comunes para el inicio de sesión de usuarios en el sistema.

    Args:
        BaseModel (pydantic.BaseModel): Clase base de Pydantic para la validación de datos.
    
    Attributes:
        correo (EmailStr): Correo electrónico del usuario.
        contraseña (str): Contraseña del usuario.
    """

    correo: EmailStr = Field(..., example="usuario@empresa.com")
    contraseña: str = Field(..., example="password")    # pylint: disable=non-ascii-name

class LoginCreate(LoginBase):
    """
    Modelo para crear un nuevo inicio de sesión.
    Este modelo se utiliza para validar los datos al crear un nuevo inicio de sesión.

    Args:
        LoginBase (LoginBase): Modelo base para el inicio de sesión de usuarios.
        
    Attributes:
        es_administrador (bool): Indica si el usuario es administrador. Por defecto es False.
    """

    es_administrador: bool = Field(False, description="Indica si el usuario es administrador.")

class LoginRequest(BaseModel):
    """
    Modelo para la solicitud de inicio de sesión.
    Este modelo se utiliza para validar los datos al iniciar sesión.

    Args:
        BaseModel (pydantic.BaseModel): Clase base de Pydantic para la validación de datos.
        
    Attributes:
        correo (EmailStr): Correo electrónico del usuario.
        contraseña (str): Contraseña del usuario.
    """

    correo: EmailStr = Field(..., example="admin@marloy.com")
    contraseña: str = Field(..., example="adminpass")   # pylint: disable=non-ascii-name

class Token(BaseModel):
    """
    Modelo para el token de autenticación.
    Este modelo define el token que se devuelve al iniciar sesión exitosamente.

    Args:
        BaseModel (pydantic.BaseModel): Clase base de Pydantic para la validación de datos.
        
    Attributes:
        access_token (str): Token de acceso generado al iniciar sesión.
    """

    access_token: str = Field(..., example="eyJhbGciOiJIUzI1NiI...")

class LoginResponseData(Token):
    """
    Modelo para la respuesta de inicio de sesión.
    Este modelo se utiliza para devolver los datos del usuario al iniciar sesión exitosamente.

    Args:
        Token (Token): Modelo para el token de autenticación.
        
    Attributes:
        is_admin (bool): Indica si el usuario logueado es administrador.
    """

    is_admin: bool = Field(..., description="Indica si el usuario logueado es administrador.")
