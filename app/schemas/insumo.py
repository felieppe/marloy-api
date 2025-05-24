from pydantic import BaseModel, Field

class InsumoBase(BaseModel):
    descripcion: str = Field(..., max_length=255, example="Café Tostado Grano")
    tipo: str | None = Field(None, max_length=100, example="Café")
    precio_unitario: float = Field(..., gt=0, example=0.15) # Mayor que cero
    id_proveedor: int = Field(..., gt=0, example=1)

class InsumoCreate(InsumoBase):
    pass

class InsumoUpdate(InsumoBase):
    descripcion: str | None = Field(None, max_length=255, example="Café Molido Premium")
    tipo: str | None = Field(None, max_length=100, example="Café")
    precio_unitario: float | None = Field(None, gt=0, example=0.18)
    id_proveedor: int | None = Field(None, gt=0, example=2)

class InsumoInDB(InsumoBase):
    id: int = Field(..., description="ID único del insumo.")

    class Config:
        from_attributes = True