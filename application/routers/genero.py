from fastapi import APIRouter, Depends
from application.model.genero import Genero, GeneroDTO
from application.db.database import get_db
from sqlalchemy.orm import Session
from application.db import models
from typing import List

router = APIRouter(prefix="/genero", tags=["Generos"])


@router.get("/all", response_model=List[Genero])
def getGeneros(database: Session = Depends(get_db)):
    generos = database.query(models.Genero).all()
    return generos


@router.get("/{id}")
def getGeneroByID(id: int, database: Session = Depends(get_db)):
    genero = generoByID(id, database)
    if not genero.first():
        return {"Respuesta": "Error al buscar genero: No existe diche genero."}
    else:

        return {"genero": showGenero(genero.first())}


@router.post("/add")
def addGeneros(generoDTO: GeneroDTO, database: Session = Depends(get_db)):
    genero = models.Genero(genero=generoDTO.genero)
    if existeGenero(genero.genero, database):
        return {"Respuesta": "Error al insertar: genero ya existente en bd."}
    else:
        database.add(genero)
        database.commit()
        database.refresh(genero)
        return {"Respuesta": "genero creado.", "genero": showGenero(genero)}


@router.patch("/{id}/update")
def updateGenero(id: int, generoDTO: GeneroDTO, database: Session = Depends(get_db)):
    genero = generoByID(id, database)
    if not genero.first():
        return {"Respuesta": "Error al borrar el género: No existe diche género."}
    else:
        genero.update(generoDTO.model_dump(exclude_unset=True))
        database.commit()
        return {
            "Respuesta": "género modificado con éxito.",
            "genero": showGenero(genero.first()),
        }


@router.delete("/{id}/delete")
def deleteGenero(id: int, database: Session = Depends(get_db)):
    genero = generoByID(id, database)
    if not genero.first():
        return {"Respuesta": "Error al borrar el género: No existe diche genero."}
    else:
        database.delete(genero)
        database.commit()
        return {"Respuesta": "genero eliminado con exito."}


def existeGenero(genre: str, database: Session):
    data = database.query(models.Genero).all()
    existe = False
    for generoDB in data:
        if generoDB.genero == genre:
            existe = True
    return existe


def generoByID(id: int, database: Session = Depends(get_db)):
    return database.query(models.Genero).filter(models.Genero.id == id)


def showGenero(genre: Genero):
    genero = models.Genero(genero=genre.genero)
    return genero
