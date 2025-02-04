from datetime import datetime
# from typing import Optional
from pydantic import BaseModel

class Genero(BaseModel):
    id:int
    genero:str

class GeneroDTO (BaseModel):
    genero:str