from pydantic import BaseModel, EmailStr, Field

class LoginBase(BaseModel):
    correo: EmailStr = Field(..., example="usuario@empresa.com")
    contraseña: str = Field(..., example="password")

class LoginCreate(LoginBase):
    es_administrador: bool = Field(False, description="Indica si el usuario es administrador.")

class LoginInDB(LoginBase):
    es_administrador: bool

    class Config:
        from_attributes = True