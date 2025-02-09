from fastapi import APIRouter, Depends
from application.model.autor import Autor, AutorDTO
from application.db.database import get_db
from sqlalchemy.orm import Session
from application.db import models
from typing import List

router = APIRouter(prefix="/autor", tags=["Autores"])


@router.get("/all", response_model=List[Autor])
def getAutor(database: Session = Depends(get_db)):
    autores = database.query(models.Libro).all()
    return autores


@router.get("/{id}")
def getAutorByID(id: int, database: Session = Depends(get_db)):
    autor = generoByID(id, database)
    if not autor.first():
        return {"Respuesta": "Error al buscar genero: No existe diche genero."}
    else:

        return {"genero": showAutor(autor.first())}


@router.post("/add")
def addAutor(autorDTO: AutorDTO, database: Session = Depends(get_db)):
    autor = models.Libro(nombre=autorDTO.nombre, edad=autorDTO.edad)
    if existeGenero(autor.nombre, database):
        return {"Respuesta": "Error al insertar: autor ya existente en bd."}
    else:
        database.add(autor)
        database.commit()
        database.refresh(autor)
        return {"Respuesta": "autor creado.", "Autor": showAutor(autor)}


@router.patch("/{id}/update")
def updateAutor(id: int, autorDTO: AutorDTO, database: Session = Depends(get_db)):
    autor = generoByID(id, database)
    if not autor.first():
        return {"Respuesta": "Error al borrar el autor: No existe diche autor."}
    else:
        autor.update(autorDTO.model_dump(exclude_unset=True))
        database.commit()
        return {
            "Respuesta": "autor modificado con éxito.",
            "genero": showAutor(autor.first()),
        }


@router.delete("/{id}/delete")
def deleteAutor(id: int, database: Session = Depends(get_db)):
    autor = generoByID(id, database)
    if not autor.first():
        return {"Respuesta": "Error al borrar el autor: No existe diche autor."}
    else:
        database.delete(autor)
        database.commit()
        return {"Respuesta": "autor eliminado con exito."}


def existeGenero(nombre, database: Session):
    data = database.query(models.Libro).all()
    existe = False
    for autorDB in data:
        if autorDB.nombre == nombre:
            existe = True
    return existe


def generoByID(id: int, database: Session = Depends(get_db)):
    return database.query(models.Libro).filter(models.Libro.id == id)


def showAutor(author: Autor):
    autor = models.Libro(nombre=author.nombre, edad=author.edad)
    return autor
