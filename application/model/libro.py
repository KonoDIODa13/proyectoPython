from datetime import datetime
from pydantic import BaseModel


class Libro(BaseModel):
    id: int
    titulo: str
    autor_id: int
    genero_id: int
    descripcion: str
    fecha_publicacion: datetime

    """class Config:
        orm_mode = True"""


class LibroDTO(BaseModel):
    titulo: str
    autor_id: int
    genero_id: int
    descripcion: str
    fecha_publicacion: datetime
    
