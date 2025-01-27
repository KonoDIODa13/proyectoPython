from datetime import datetime
# from typing import Optional
from pydantic import BaseModel

class Usuario (BaseModel):
    nombre:str
    gmail:str
    contrasenna: str
    
