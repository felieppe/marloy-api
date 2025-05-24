from pydantic import BaseModel, Field
from datetime import datetime

class MantenimientoBase(BaseModel):
    id: int | None = Field(None, gt=0, example=1, description="ID único del mantenimiento.")
    id_maquina: int = Field(..., gt=0, example=1)
    ci_tecnico: str = Field(..., max_length=20, example="1234567-8")
    tipo: str = Field(..., max_length=100, example="Preventivo")
    fecha: datetime = Field(..., example="2025-05-23T14:30:00")
    observaciones: str | None = Field(None, example="Se realizó limpieza y lubricación de componentes.")

class MantenimientoCreate(MantenimientoBase):
    pass

class MantenimientoUpdate(MantenimientoBase):
    id_maquina: int | None = Field(None, gt=0, example=2)
    ci_tecnico: str | None = Field(None, max_length=20, example="8765432-1")
    tipo: str | None = Field(None, max_length=100, example="Asistencia")
    fecha: datetime | None = Field(None, example="2025-05-24T09:00:00")
    observaciones: str | None = Field(None, example="Se ajustó la tolva de granos y se recalibró la máquina.")

class MantenimientoInDB(MantenimientoBase):
    id: int = Field(..., description="ID único del mantenimiento.")

    class Config:
        from_attributes = True