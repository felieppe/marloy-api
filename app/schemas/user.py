from pydantic import BaseModel, EmailStr, Field

class UserBase(BaseModel):
    correo: EmailStr = Field(..., example="usuario@empresa.com")
    es_administrador: bool = Field(False, description="Indica si el usuario es administrador.")

class UserCreate(UserBase):
    contraseña: str = Field(..., example="password", min_length=8, description="Contraseña del usuario, debe tener al menos 8 caracteres.")

class UserUpdate(BaseModel):
    es_administrador: bool = Field(..., description="Indica si el usuario es administrador.")
