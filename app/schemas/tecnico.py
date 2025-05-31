from pydantic import BaseModel, Field

class TecnicoBase(BaseModel):
    ci: str = Field(..., max_length=20, example="1234567-8")
    nombre: str = Field(..., max_length=100, example="Juan")
    apellido: str = Field(..., max_length=100, example="Pérez")
    telefono: str | None = Field(None, max_length=50, example="098765432")

class TecnicoCreate(TecnicoBase):
    pass

class TecnicoUpdate(BaseModel):
    nombre: str | None = Field(None, max_length=100, example="Juan Carlos")
    apellido: str | None = Field(None, max_length=100, example="Pérez Gómez")
    telefono: str | None = Field(None, max_length=50, example="099112233")

class TecnicoInDB(TecnicoBase):
    class Config:
        from_attributes = True