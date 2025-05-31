from pydantic import BaseModel, Field
from datetime import datetime

class RegistroConsumoBase(BaseModel):
    id: int | None = Field(None, description="ID único del registro de consumo.")
    id_maquina: int = Field(..., gt=0, example=1)
    id_insumo: int = Field(..., gt=0, example=1)
    fecha: datetime = Field(..., example="2025-05-23T10:00:00")
    cantidad_usada: float = Field(..., gt=0, example=100.0)

class RegistroConsumoCreate(BaseModel):
    id_maquina: int = Field(..., gt=0, example=1)
    id_insumo: int = Field(..., gt=0, example=1)
    fecha: datetime = Field(..., example="2025-05-23T10:00:00")
    cantidad_usada: float = Field(..., gt=0, example=100.0)

class RegistroConsumoUpdate(BaseModel):
    cantidad_usada: float | None = Field(None, gt=0, example=120.0)

class RegistroConsumoInDB(RegistroConsumoBase):
    id: int = Field(..., description="ID único del registro de consumo.")

    class Config:
        from_attributes = True