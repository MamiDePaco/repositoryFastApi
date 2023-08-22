#Algo a tomar en cuenta, es la estrucuta de nuestras API, con respecto a nuestrs rutas, lo que quiero decir es que las rutas mas especificas tienen que ir poor encima de las mas genericas, para que el interprete de rutas, vea que si coincide con la especifica , sea usada y si no , se use la generica.


#importaciones
from fastapi import FastAPI, Response, status, HTTPException, Depends
from . import models #,schemas,utils
from .database import engine,get_db
from .routers import post,user,auth,vote
from .config import Settings
#from fastapi.params import Body

from fastapi.middleware.cors import CORSMiddleware

#La línea de código models.Base.metadata.create_all(bind=engine) en SQLAlchemy se utiliza para crear (o más precisamente, generar) las tablas en la base de datos basándose en la definición de los modelos (clases) que heredan de la clase Base.
#Asu vez, dicho codgio es el que le dice a sql alchemy que cree las tablas cuando se ejecute por primera vez , pero como al tener a alembic , esto ya no es necesario, pero se puede dejar sin romper nada.
models.Base.metadata.create_all(bind=engine)

#Cuando haces app = FastAPI(), estás creando una instancia de la clase FastAPI, que es el núcleo del framework. Esta instancia representa tu aplicación web y te permite agregar rutas, endpoints, middleware, manejar dependencias, entre otras cosas.Una vez que has creado la instancia de la aplicación app, puedes utilizar sus métodos y atributos para definir cómo se comportará tu API y cómo responderá a las solicitudes de los clientes.Por ejemplo, puedes agregar endpoints a la aplicación utilizando decoradores como @app.get, @app.post, @app.put, @app.delete, entre otros. Estos decoradores se utilizan para definir las rutas y métodos HTTP que tu API soportará.
app=FastAPI()


#son aquellos dominios de donde podre! ejecutar una peticion a mi api
#origins = ["http://localhost.tiangolo.com","https://localhost.tiangolo.com","http://localhost","http://localhost:8080",]


origins = [
    'https://www.youtube.com',
    #'https://youtube.com',
    'https://www.google.com'
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def main():
    return {"message":"Welcome to my API server"}

#Routes: En FastAPI, app.include_router es un método que se utiliza para agregar un conjunto de rutas definidas en un objeto APIRouter a la aplicación principal (app). Un APIRouter es una clase proporcionada por FastAPI que te permite definir un grupo de rutas y endpoints relacionados.
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)