from pydantic import BaseModel, Field, EmailStr

class ClienteBase(BaseModel):
    nombre: str = Field(..., max_length=255, example="Oficinas Centrales XYZ")
    direccion: str = Field(..., max_length=255, example="Av. Libertador 2000")
    telefono: str | None = Field(None, max_length=50, example="099123456")
    correo: EmailStr | None = Field(None, example="contacto@xyz.com")

class ClienteCreate(ClienteBase):
    pass

class ClienteUpdate(ClienteBase):
    nombre: str | None = Field(None, max_length=255, example="Oficinas Centrales XYZ S.A.")
    direccion: str | None = Field(None, max_length=255, example="Av. Libertador 2050")
    telefono: str | None = Field(None, max_length=50, example="099987654")
    correo: EmailStr | None = Field(None, example="nuevo.contacto@xyz.com")

class ClienteInDB(ClienteBase):
    id: int = Field(..., description="ID único del cliente.")

    class Config:
        from_attributes = True