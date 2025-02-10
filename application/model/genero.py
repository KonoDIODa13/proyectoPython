from datetime import datetime
from typing import List

# from typing import Optional
from pydantic import BaseModel
from application.model.libro import Libro


class Genero(BaseModel):
    id: int
    genero: str
    libros: List[Libro] = []

    """class Config:
        orm_mode = True"""


class GeneroDTO(BaseModel):
    genero: str
