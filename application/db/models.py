from application.db.database import Base
from sqlalchemy import Column,Integer,String,Boolean,DateTime
from datetime import datetime
from sqlalchemy.schema import ForeignKey
from sqlalchemy.orm import relationship


class Usuario(Base):
    __tablename__ = "usuario"
    id = Column(Integer,primary_key=True,autoincrement=True)
    nombre=Column(String)
    gmail=Column(String)
    contrasenna= Column(String)

class Genero(Base):
    __tablename__= "genero"
    id = Column(Integer,primary_key=True,autoincrement=True)
    genero = Column(String)
    libro_id = relationship("Libro", backref="genero", cascade="delete, merge")

class Autor(Base):
    __tablename__= "autor"
    id = Column(Integer,primary_key=True,autoincrement=True)
    nombre = Column(String)
    edad = Column(Integer)
    libro_id = relationship("Libro", backref="autor", cascade="delete, merge")

class Libro(Base):
    __tablename__= "libro"
    id = Column(Integer,primary_key=True,autoincrement=True)
    titulo= Column(String)
    genero_id = Column(Integer, ForeignKey("genero.id", ondelete = "CASCADE"))
    autor_id = Column(Integer, ForeignKey("autor.id", ondelete = "CASCADE"))
    descripcion= Column(String)
    fecha_publicacion= Column(DateTime, default=datetime.now, onupdate=datetime.now)
