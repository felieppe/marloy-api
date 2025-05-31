from pydantic import BaseModel, Field, EmailStr

class ClienteBase(BaseModel):
    id: int = Field(..., description="ID único del cliente.", ge=1)
    nombre: str = Field(..., max_length=255, example="Oficinas Centrales XYZ")
    direccion: str = Field(..., max_length=255, example="Av. Libertador 2000")
    telefono: str | None = Field(None, max_length=50, example="099123456")
    correo: EmailStr | None = Field(None, example="contacto@xyz.com")

class ClienteCreate(BaseModel):
    nombre: str = Field(..., max_length=255, example="Oficinas Centrales XYZ")
    direccion: str = Field(..., max_length=255, example="Av. Libertador 2000")
    telefono: str | None = Field(None, max_length=50, example="099123456")
    correo: EmailStr | None = Field(None, example="contacto@xyz.com")

class ClienteUpdate(ClienteCreate):
    pass

class ClienteInDB(ClienteBase):
    id: int = Field(..., description="ID único del cliente.")

    class Config:
        from_attributes = True