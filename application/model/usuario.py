from datetime import datetime
# from typing import Optional
from pydantic import BaseModel

class Usuario (BaseModel):
    id: int
    nombre:str
    gmail:str
    contrasenna: str

class UsuarioDTO(BaseModel):
    nombre:str
    gmail:str
    contrasenna: str
    
