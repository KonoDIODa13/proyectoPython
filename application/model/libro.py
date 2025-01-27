from datetime import datetime
# from typing import Optional
from pydantic import BaseModel
from autor import Autor
from genero import Genero

class libro(BaseModel):
    titulo:str
    autor: Autor
    genero: Genero
    descripcion: str
    fecha_publicacion: datetime
