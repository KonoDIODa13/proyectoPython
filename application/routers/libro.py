from fastapi import APIRouter, Depends
from application.model.libro import Libro, LibroDTO, LibroUpdate

"""
from application.model.autor import Autor, AutorDTO
from application.model.genero import Genero, GeneroDTO
"""
from application.db.database import get_db
from sqlalchemy.orm import Session
from application.db import models
from typing import List

router = APIRouter(prefix="/libro", tags=["Libros"])


@router.get("/all", response_model=List[Libro])
def getLibro(database: Session = Depends(get_db)):
    libros = database.query(models.Libro).all()
    return libros


@router.get("/{id}")
def getLibroByID(id: int, database: Session = Depends(get_db)):
    libro = libroByID(id, database)
    if not libro:
        return {"Respuesta": "Error al buscar libro: No existe diche libro."}
    else:

        return {"Libro": showLibro(libro)}


@router.post("/add")
def addLibro(libroDTO: LibroDTO, database: Session = Depends(get_db)):
    libro = models.Libro(
        titulo=libroDTO.titulo,
        descripcion=libroDTO.descripcion,
        fecha_publicacion=libroDTO.fecha_publicacion,
        autor_id=libroDTO.autor_id,
        genero_id=libroDTO.genero_id,
    )
    if (
        existeLibro(libro.titulo, database)
        and existeGenero(libro.genero_id, database)
        and existeAutor(libro.autor_id, database)
    ):
        return {"Respuesta": "Error al insertar: libro ya existente en bd."}
    else:
        database.add(libro)
        database.commit()
        database.refresh(libro)
        return {"Respuesta": "libro creado.", "Libro": showLibro(libro)}


@router.patch("/{id}/update")
#def updateLibro(id: int, libroUpdate: LibroUpdate, database: Session = Depends(get_db)): en caso de que pete con el de libroDTO
def updateLibro(id: int, libroDTO: LibroDTO, database: Session = Depends(get_db)):
    libro = libroByID(id, database)
    if not libro:
        return {"Respuesta": "Error al borrar el libro: No existe diche libro."}
    else:
        if (
            existeGenero(libroDTO.genero_id, database)
            and existeAutor(libroDTO.autor_id, database)
        ):
            libro.titulo= libroDTO.titulo
            libro.autor_id= libroDTO.autor_id
            libro.genero_id= libroDTO.genero_id
            libro.descripcion= libroDTO.descripcion
            libro.fecha_publicacion= libroDTO.fecha_publicacion
            
            database.commit()
            return {
                "Respuesta": "libro modificado con éxito.",
                "Libro": showLibro(libro),
            }
        else:
            return {"Respuesta": "no se puede modificar el libro"}


@router.delete("/{id}/delete")
def deleteLibro(id: int, database: Session = Depends(get_db)):
    libro = libroByID(id, database)
    if not libro.first():
        return {"Respuesta": "Error al borrar el libro: No existe diche libro."}
    else:
        database.delete(libro.first())
        database.commit()
        return {"Respuesta": "libro eliminado con exito."}


def existeLibro(titulo: str, database: Session):
    data = database.query(models.Libro).all()
    existe = False
    for libroDB in data:
        if libroDB.titulo == titulo:
            existe = True
    return existe


def existeGenero(id_genero: int, database: Session):
    data = database.query(models.Genero).all()
    existe = False
    for generoDB in data:
        if generoDB.id == id_genero:
            existe = True
    return existe


def existeAutor(id_autor: int, database: Session):
    data = database.query(models.Autor).all()
    existe = False
    for autorDB in data:
        if autorDB.id == id_autor:
            existe = True
    return existe


def libroByID(id: int, database: Session = Depends(get_db)):
    return database.query(models.Libro).filter(models.Libro.id == id).first()


def showLibro(book: Libro):
    libro = models.Libro(
        titulo=book.titulo,
        descripcion=book.descripcion,
        fecha_publicacion=book.fecha_publicacion,
        genero_id=book.genero_id,
        autor_id=book.autor_id,
    )
    return libro
