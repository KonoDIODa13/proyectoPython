from datetime import datetime
# from typing import Optional
from pydantic import BaseModel

class Autor(BaseModel):
    nombre:str
    edad: int