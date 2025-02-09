from datetime import datetime
# from typing import Optional
from pydantic import BaseModel
from application.model.autor import AutorDTO
from application.model.genero import GeneroDTO

class Libro(BaseModel):
    id: int
    titulo:str
    autor: AutorDTO
    genero: GeneroDTO
    descripcion: str
    fecha_publicacion: datetime
    
class LibroDTO (BaseModel):
    titulo:str
    autor: Autor
    genero: Genero
    descripcion: str
    fecha_publicacion: datetime
