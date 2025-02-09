from fastapi import APIRouter, Depends
from application.model.libro import Libro, LibroDTO
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
    if not libro.first():
        return {"Respuesta": "Error al buscar libro: No existe diche libro."}
    else:

        return {"Libro": showLibro(libro.first())}


@router.post("/add")
def addLibro(libroDTO: LibroDTO, database: Session = Depends(get_db)):
    libro = models.Libro(
        titulo=libroDTO.titulo,
        descripcion=libroDTO.descripcion,
        fecha_publicacion=libroDTO.fecha_publicacion,
        autor_id=libroDTO.autor,
        genero_id=libroDTO.genero,
    )
    if existeLibro(libro.titulo, database):
        return {"Respuesta": "Error al insertar: libro ya existente en bd."}
    else:
        database.add(libro)
        database.commit()
        database.refresh(libro)
        return {"Respuesta": "libro creado.", "Libro": showLibro(libro)}


@router.patch("/{id}/update")
def updateLibro(id: int, libroDTO: LibroDTO, database: Session = Depends(get_db)):
    libro = libroByID(id, database)
    if not libro.first():
        return {"Respuesta": "Error al borrar el libro: No existe diche autor."}
    else:
        libro.update(libroDTO.model_dump(exclude_unset=True))
        database.commit()
        return {
            "Respuesta": "libro modificado con éxito.",
            "Libro": showLibro(libro.first()),
        }


@router.delete("/{id}/delete")
def deleteLibro(id: int, database: Session = Depends(get_db)):
    libro = libroByID(id, database)
    if not libro.first():
        return {"Respuesta": "Error al borrar el libro: No existe diche libro."}
    else:
        database.delete(libro)
        database.commit()
        return {"Respuesta": "libro eliminado con exito."}


def existeLibro(titulo, database: Session):
    data = database.query(models.Libro).all()
    existe = False
    for autorDB in data:
        if autorDB.nombre == titulo:
            existe = True
    return existe


def libroByID(id: int, database: Session = Depends(get_db)):
    return database.query(models.Libro).filter(models.Libro.id == id)


def showLibro(book: Libro):
    libro = models.Libro(
        titulo=book.titulo,
        descripcion=book.descripcion,
        fecha_publicacion=book.fecha_publicacion,
        genero=book.genero_id,
        autor=book.autor_id,
    )
    return libro
