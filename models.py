from sqlmodel import SQLModel, Field, Relationship

# Modelo de la tabla proveedor
class Proveedor(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nombre: str = Field(min_length=2, max_length=60)

    articulos: list["Articulo"] = Relationship(back_populates="proveedor")

# Modelo de la tabla articulo
class Articulo(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nombre: str = Field(min_length=2, max_length=60)
    precio: float = Field(gt=1000, lt=999999)
    activo: bool = Field(default=True)

    proveedor_id: int = Field(foreign_key="proveedor.id")
    proveedor: Proveedor | None = Relationship(back_populates="articulos")
