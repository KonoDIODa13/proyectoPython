from fastapi import APIRouter, Depends
from application.model.autor import Autor, AutorDTO
from application.model.libro import Libro
from application.db.database import get_db
from sqlalchemy.orm import Session
from application.db import models
from typing import List

router = APIRouter(prefix="/autor", tags=["Autores"])


@router.get("/all", response_model=List[Autor])
def getAutor(database: Session = Depends(get_db)):
    autores = database.query(models.Autor).all()
    return autores


@router.get("/{id}")
def getAutorByID(id: int, database: Session = Depends(get_db)):
    autor = autorByID(id, database)
    if not autor:
        return {"Respuesta": "Error al buscar genero: No existe diche genero."}
    else:
        return {"autor": autor}


@router.post("/add")
def addAutor(autorDTO: AutorDTO, database: Session = Depends(get_db)):
    autor = models.Autor(nombre=autorDTO.nombre, edad=autorDTO.edad)
    if existeAutor(autor.nombre, database):
        return {"Respuesta": "Error al insertar: autor ya existente en bd."}
    else:
        database.add(autor)
        database.commit()
        database.refresh(autor)
        return {"Respuesta": "autor creado.", "Autor": autor}


@router.patch("/{id}/update")
def updateAutor(id: int, autorDTO: AutorDTO, database: Session = Depends(get_db)):
    autor = autorByID(id, database)
    if not autor:
        return {"Respuesta": "Error al borrar el autor: No existe diche autor."}
    else:
        autor.nombre = autorDTO.nombre
        autor.edad = autor.edad
        database.commit()
        return {
            "Respuesta": "autor modificado con éxito.",
            "genero": autor,
        }


@router.delete("/{id}/delete")
def deleteAutor(id: int, database: Session = Depends(get_db)):
    autor = autorByID(id, database)
    if not autor.first():
        return {"Respuesta": "Error al borrar el autor: No existe diche autor."}
    else:
        database.delete(autor)
        database.commit()
        return {"Respuesta": "autor eliminado con exito."}


def existeAutor(nombre, database: Session):
    data = database.query(models.Autor).all()
    existe = False
    for autorDB in data:
        if autorDB.nombre == nombre:
            existe = True
    return existe


def autorByID(id: int, database: Session):
    autorBD = database.query(models.Autor).filter(models.Autor.id == id).first()

    if autorBD:
        autor = Autor(
            id=autorBD.id,
            nombre=autorBD.nombre,
            edad=autorBD.edad,
            libros=[
                Libro(
                    id=libro.id,
                    titulo=libro.titulo,
                    autor_id=libro.autor_id,
                    genero_id=libro.genero_id,
                    descripcion=libro.descripcion,
                    fecha_publicacion=libro.fecha_publicacion,
                )
                for libro in autorBD.libros
            ],
        )
        return autor
    else:
        return None
