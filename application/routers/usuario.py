from fastapi import APIRouter, Depends
from application.model.usuario import Usuario
from application.db.database import get_db
from sqlalchemy.orm import Session
from application.db import models
from typing import List

router= APIRouter(
    prefix="/usuario",
    tags=["Usuarios"]
)

@router.get("/all", response_model=List[Usuario])
def getUsuarios(database:Session=Depends(get_db)):
    usuarios = database.query(models.Usuario).all()
    return usuarios

@router.post("/add")
def addUsuarios(usuarioBody: Usuario, database:Session=Depends(get_db)):
    dick_usuario= usuarioBody.model_dump()
    usuario= models.Usuario(
        nombre = dick_usuario["nombre"],
        gmail = dick_usuario['gmail'],
        contrasenna = dick_usuario['contrasenna']
    )
    if(existeUsuario(usuario, database)):
        return {"Respuesta": "Error al insertar: Usuario ya existente en bd."}
    else:
        database.add(usuario)
        database.commit()
        database.refresh(usuario)
        return {
            "Respuesta": "Usuario creado.",
            "Usuario": usuario
                } 


def existeUsuario(usuario: Usuario,database: Session):
    data = database.query(models.Usuario).all()
    existe= False
    for usuarioDB in data:
        if usuarioDB.nombre == usuario.nombre and usuarioDB.contrasenna == usuario.contrasenna:
            existe=True
    return existe