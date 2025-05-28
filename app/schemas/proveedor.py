from pydantic import BaseModel, Field, ConfigDict

class ProveedorBase(BaseModel):
    id: int = Field(..., description="ID único del proveedor.", ge=1)
    nombre: str = Field(..., max_length=255, example="Distribuidora Café Express")
    contacto: str | None = Field(None, max_length=255, example="info@cafexpress.com")

class ProveedorCreate(ProveedorBase):
    id: int | None = Field(None, description="ID único del proveedor. Se genera automáticamente al crear el proveedor.", ge=1)
    model_config = ConfigDict(exclude={'id'})

class ProveedorUpdate(ProveedorBase):
    nombre: str | None = Field(None, max_length=255, example="Distribuidora Café Express S.A.")
    contacto: str | None = Field(None, max_length=255, example="nuevo.contacto@cafexpress.com")

class ProveedorInDB(ProveedorBase):
    id: int = Field(..., description="ID único del proveedor.")

    class Config:
        from_attributes = True