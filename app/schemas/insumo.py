from pydantic import BaseModel, Field, ConfigDict

class InsumoBase(BaseModel):
    id: int = Field(..., description="ID único del insumo.", ge=1, example=1)
    descripcion: str = Field(..., max_length=255, example="Café Tostado Grano")
    tipo: str | None = Field(None, max_length=100, example="Café")
    precio_unitario: float = Field(..., gt=0, example=0.15) # Mayor que cero
    id_proveedor: int = Field(..., gt=0, example=1)

class InsumoCreate(InsumoBase):
    id: int | None = Field(None, description="ID único del proveedor. Se genera automáticamente al crear el proveedor.", ge=1)
    model_config = ConfigDict(exclude={'id'})

class InsumoUpdate(InsumoBase):
    descripcion: str | None = Field(None, max_length=255, example="Café Molido Premium")
    tipo: str | None = Field(None, max_length=100, example="Café")
    precio_unitario: float | None = Field(None, gt=0, example=0.18)
    id_proveedor: int | None = Field(None, gt=0, example=2)

class InsumoInDB(InsumoBase):
    id: int = Field(..., description="ID único del insumo.")

    class Config:
        from_attributes = True