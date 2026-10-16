from sqlmodel import SQLModel, Field


# Schema para crear proveedores
class ProveedorCreate(SQLModel):
    nombre: str = Field(min_length=2, max_length=60)


# Schema para mostrar proveedores
class ProveedorRead(ProveedorCreate):
    id: int


# Schema para crear articulos
class ArticuloCreate(SQLModel):
    nombre: str = Field(min_length=2, max_length=60)
    precio: float = Field(gt=1000, lt=999999)
    activo: bool = True
    proveedor_id: int = Field(gt=0)


# Schema para mostrar articulos con su proveedor
class ArticuloRead(ArticuloCreate):
    id: int
    proveedor: ProveedorRead | None = None
