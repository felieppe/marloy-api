"""
    Esquemas para el modelo de datos Insumo.
"""

from pydantic import BaseModel, Field, ConfigDict

class InsumoBase(BaseModel):
    """
    Modelo base para los insumos.
    Este modelo define los campos comunes para los insumos en el sistema.
    
    Args:
        BaseModel (pydantic.BaseModel): Clase base de Pydantic para la validación de datos.
    
    Attributes:
        id (int): ID único del insumo.
        descripcion (str): Descripción del insumo.
        tipo (str | None): Tipo del insumo, opcional.
        precio_unitario (float): Precio unitario del insumo, debe ser mayor que cero.
        id_proveedor (int): ID del proveedor del insumo, debe ser mayor que cero.
    """

    id: int = Field(..., description="ID único del insumo.", ge=1, example=1)
    descripcion: str = Field(..., max_length=255, example="Café Tostado Grano")
    tipo: str | None = Field(None, max_length=100, example="Café")
    precio_unitario: float = Field(..., gt=0, example=0.15) # Mayor que cero
    id_proveedor: int = Field(..., gt=0, example=1)

class InsumoCreate(InsumoBase):
    """
    Modelo para crear un nuevo insumo.
    Este modelo se utiliza para validar los datos al crear un nuevo insumo.

    Args:
        InsumoBase (InsumoBase): Modelo base para los insumos.

    Attributes:
        descripcion (str): Descripción del insumo.
        tipo (str | None): Tipo del insumo, opcional.
        precio_unitario (float): Precio unitario del insumo, debe ser mayor que cero.
        id_proveedor (int): ID del proveedor del insumo, debe ser mayor que cero.
    """

    id: int | None = Field(
        None,
        description="ID único del proveedor. Se genera automáticamente al crear el proveedor.",
        ge=1
    )
    model_config = ConfigDict(exclude={'id'})

class InsumoUpdate(BaseModel):
    """
    Modelo para actualizar un insumo existente.
    Este modelo se utiliza para validar los datos al actualizar un insumo.

    Args:
        BaseModel (pydantic.BaseModel): Clase base de Pydantic para la validación de datos.

    Attributes:
        descripcion (str | None): Descripción del insumo, opcional.
        tipo (str | None): Tipo del insumo, opcional.
        precio_unitario (float | None): Precio unitario del insumo, debe ser mayor que cero.
        id_proveedor (int | None): ID del proveedor del insumo, debe ser mayor que cero.
    """

    descripcion: str | None = Field(None, max_length=255, example="Café Molido Premium")
    tipo: str | None = Field(None, max_length=100, example="Café")
    precio_unitario: float | None = Field(None, gt=0, example=0.18)
    id_proveedor: int | None = Field(None, gt=0, example=2)
