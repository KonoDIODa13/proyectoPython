from fastapi import APIRouter, Depends
# from model import usuario, Autor, Genero, Libro
from application.model.usuario import Usuario;
# from app.db.database import get_db
# from sqlalchemy.orm import Session
#from application.database import models
from typing import List

router= APIRouter(
    prefix="/usuario",
    tags=["Usuarios"]
)

"""@router.get("/all")
def getUsuarios(database:Session=Depends(get_db)):
    usuarios= database.query(models.Usuario).all()
    return usuarios"""