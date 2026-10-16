from typing import Annotated
from fastapi import FastAPI, HTTPException, Depends, Path, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select

from database import get_db
import models
import schemas

app = FastAPI()

app.title = "App comercio"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Respuesta de error
NOT_FOUND_RESPONSE = {
    404: {
        "description": "Articulo no encontrado",
        "content": {
            "application/json": {
                "example": {"detail": "Articulo no encontrado"}
            }
        },
    },
}


# GET - Obtener todos los proveedores
@app.get("/proveedores", response_model=list[schemas.ProveedorRead])
def get_proveedores(db: Session = Depends(get_db)):
    proveedores = db.exec(select(models.Proveedor)).all()
    return proveedores


# POST - Agregar proveedor
@app.post("/proveedores", response_model=schemas.ProveedorRead)
def agregar_proveedor(
    proveedor_nuevo: schemas.ProveedorCreate,
    db: Session = Depends(get_db)
):
    nuevo_proveedor = models.Proveedor(
        nombre=proveedor_nuevo.nombre
    )

    db.add(nuevo_proveedor)
    db.commit()
    db.refresh(nuevo_proveedor)

    return nuevo_proveedor


# GET - Obtener todos los articulos
@app.get("/articulos", response_model=list[schemas.ArticuloRead])
def get_articulos(db: Session = Depends(get_db)):
    articulos = db.exec(select(models.Articulo)).all()
    return articulos


# GET - Buscar articulo por ID
@app.get(
    "/articulos/{id}",
    responses=NOT_FOUND_RESPONSE,
    response_model=schemas.ArticuloRead
)
def get_articulos_by_id(
    id: Annotated[int, Path(gt=0)],
    db: Session = Depends(get_db)
):
    articulo = db.get(models.Articulo, id)

    if articulo is None:
        raise HTTPException(
            status_code=404,
            detail="Articulo no encontrado"
        )

    return articulo


# POST - Agregar articulo
@app.post("/articulos", response_model=schemas.ArticuloRead)
def agregar_articulo(
    articulo_nuevo: schemas.ArticuloCreate,
    db: Session = Depends(get_db)
):
    proveedor = db.get(
        models.Proveedor,
        articulo_nuevo.proveedor_id
    )

    if proveedor is None:
        raise HTTPException(
            status_code=404,
            detail="Proveedor no encontrado"
        )

    nuevo_articulo = models.Articulo(
        nombre=articulo_nuevo.nombre,
        precio=articulo_nuevo.precio,
        activo=articulo_nuevo.activo,
        proveedor_id=articulo_nuevo.proveedor_id
    )

    db.add(nuevo_articulo)
    db.commit()
    db.refresh(nuevo_articulo)

    return nuevo_articulo


# DELETE - Borrar articulo
@app.delete(
    "/articulos/{id}",
    responses=NOT_FOUND_RESPONSE,
    response_model=schemas.ArticuloRead
)
def borrar_articulos(
    id: Annotated[int, Path(gt=0)],
    logico: Annotated[bool, Query(description="Mantener registro")] = False,
    db: Session = Depends(get_db)
):
    articulo = db.get(models.Articulo, id)

    if articulo is None:
        raise HTTPException(
            status_code=404,
            detail="Articulo no encontrado"
        )

    respuesta = schemas.ArticuloRead.model_validate(articulo)

    if logico:
        articulo.activo = False
        db.add(articulo)
    else:
        db.delete(articulo)

    db.commit()

    if logico:
        db.refresh(articulo)
        return articulo

    return respuesta


# PUT - Editar articulo
@app.put(
    "/articulos/{id}",
    responses=NOT_FOUND_RESPONSE,
    response_model=schemas.ArticuloRead
)
def editar_articulo(
    id: Annotated[int, Path(gt=0)],
    articulo_editar: schemas.ArticuloCreate,
    db: Session = Depends(get_db)
):
    articulo = db.get(models.Articulo, id)

    if articulo is None:
        raise HTTPException(
            status_code=404,
            detail="Articulo no encontrado"
        )

    proveedor = db.get(
        models.Proveedor,
        articulo_editar.proveedor_id
    )

    if proveedor is None:
        raise HTTPException(
            status_code=404,
            detail="Proveedor no encontrado"
        )

    articulo.nombre = articulo_editar.nombre
    articulo.precio = articulo_editar.precio
    articulo.activo = articulo_editar.activo
    articulo.proveedor_id = articulo_editar.proveedor_id

    db.add(articulo)
    db.commit()
    db.refresh(articulo)

    return articulo