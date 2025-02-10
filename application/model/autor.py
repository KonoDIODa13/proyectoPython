from datetime import datetime
from typing import List
# from typing import Optional
from pydantic import BaseModel
from application.model.libro import Libro

class Autor(BaseModel):
    id:int
    nombre:str
    edad: int
    libros: List[Libro]=[]
    
    """class Config:
        orm_mode = True""" 

class AutorDTO (BaseModel):
    nombre:str
    edad: int