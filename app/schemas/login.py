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

class LoginRequest(BaseModel):
    correo: EmailStr = Field(..., example="admin@marloy.com")
    contraseña: str = Field(..., example="adminpass")

class Token(BaseModel):
    access_token: str = Field(..., example="eyJhbGciOiJIUzI1NiI...")

class LoginResponseData(Token):
    is_admin: bool = Field(..., description="Indica si el usuario logueado es administrador.")
