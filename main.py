from fastapi import FastAPI

import uvicorn

from application.routers import usuario, genero, autor, libro

from application.db.database import Base, engine


def create_tables():
    Base.metadata.create_all(bind=engine)


create_tables()

app = FastAPI()
app.include_router(usuario.router)
app.include_router(genero.router)
app.include_router(autor.router)
app.include_router(libro.router)


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)
