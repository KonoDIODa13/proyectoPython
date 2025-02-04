from datetime import datetime
# from typing import Optional
from pydantic import BaseModel

class Autor(BaseModel):
    id:int
    nombre:str
    edad: int

class AutorDTO (BaseModel):
    nombre:str
    edad: int