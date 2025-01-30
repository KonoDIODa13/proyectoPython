from fastapi import APIRouter, Depends
from application.db.database import get_db
from sqlalchemy.orm import Session
from application.db import models

router= APIRouter(
    prefix="/usuario",
    tags=["Usuarios"]
)

@router.get("/all")
def getUsuarios(database:Session=Depends(get_db)):
    usuarios= database.query(models.Usuario).all()
    return usuarios