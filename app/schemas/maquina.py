from pydantic import BaseModel, Field

class MaquinaBase(BaseModel):
    modelo: str = Field(..., max_length=100, example="CM-Pro 5000")
    id_cliente: int = Field(..., gt=0, example=1)
    ubicacion_cliente: str = Field(..., max_length=255, example="Hall Principal")
    costo_alquiler_mensual: float = Field(..., gt=0, example=150.00)

class MaquinaCreate(MaquinaBase):
    pass

class MaquinaUpdate(MaquinaBase):
    modelo: str | None = Field(None, max_length=100, example="CM-Pro 6000")
    id_cliente: int | None = Field(None, gt=0, example=2)
    ubicacion_cliente: str | None = Field(None, max_length=255, example="Comedor")
    costo_alquiler_mensual: float | None = Field(None, gt=0, example=175.00)

class MaquinaInDB(MaquinaBase):
    id: int = Field(..., description="ID único de la máquina.")

    class Config:
        from_attributes = True