from fastapi import APIRouter, Depends
from application.model.usuario import Usuario, UsuarioDTO
from application.db.database import get_db
from sqlalchemy.orm import Session
from application.db import models
from typing import List

router = APIRouter(prefix="/usuario", tags=["Usuarios"])


@router.get("/all", response_model=List[Usuario])
def getUsuarios(database: Session = Depends(get_db)):
    usuarios = database.query(models.Usuario).all()
    return usuarios


@router.get("/{id}")
def getUsuarioByID(id: int, database: Session = Depends(get_db)):
    usuario = usuarioByID(id, database)
    if not usuario:
        return {"Respuesta": "Error al buscar usuario: No existe diche Usuario."}
    else:

        return {"Usuario": usuario}


@router.post("/add")
def addUsuarios(usuarioDTO: UsuarioDTO, database: Session = Depends(get_db)):
    usuario = models.Usuario(
        nombre=usuarioDTO.nombre,
        gmail=usuarioDTO.gmail,
        contrasenna=usuarioDTO.contrasenna,
    )
    if existeUsuario(usuario.nombre, usuario.contrasenna, database):
        return {"Respuesta": "Error al insertar: Usuario ya existente en bd."}
    else:
        database.add(usuario)
        database.commit()
        database.refresh(usuario)
        return {"Respuesta": "Usuario creado.", "Usuario": usuario}


@router.patch("/{id}/update")
def updateUsuario(id: int, usuarioDTO: UsuarioDTO, database: Session = Depends(get_db)):
    usuario = usuarioByID(id, database)
    if not usuario:
        return {"Respuesta": "Error al borrar el usuario: No existe diche Usuario."}
    else:
        usuario.nombre = usuarioDTO.nombre
        usuario.gmail = usuarioDTO.gmail
        usuario.contrasenna = usuarioDTO.contrasenna
        database.commit()
        return {
            "Respuesta": "Usuario modificado con éxito.",
            "Usuario": usuario,
        }


@router.delete("/{id}/delete")
def deleteUsuario(id: int, database: Session = Depends(get_db)):
    usuario = usuarioByID(id, database)
    if not usuario:
        return {"Respuesta": "Error al borrar el usuario: No existe diche Usuario."}
    else:
        database.delete(usuario)
        database.commit()
        return {"Respuesta": "Usuario eliminado con exito."}


def existeUsuario(nombre: str, contrasenna: str, database: Session):
    data = database.query(models.Usuario).all()
    existe = False
    for usuarioDB in data:
        if usuarioDB.nombre == nombre and usuarioDB.contrasenna == contrasenna:
            existe = True
    return existe


def usuarioByID(id: int, database: Session = Depends(get_db)):
    return database.query(models.Usuario).filter(models.Usuario.id == id).first()

