#Fue necesario para poder trabjar con formularios
#pip install python-multipart

#APIRouter es una clase proporcionada por FastAPI que se utiliza para crear subconjuntos de rutas en una aplicación web. FastAPI utiliza enrutadores (APIRouter) para organizar las rutas y las funciones asociadas en módulos separados, lo que ayuda a mantener el código ordenado y fácil de mantener, especialmente en aplicaciones más grandes.
from fastapi import APIRouter, Depends,status,HTTPException,Response


#La importación from fastapi.security.oauth2 import OAuth2PasswordRequestForm en FastAPI te permite utilizar la clase OAuth2PasswordRequestForm. Esta clase es un formulario especializado que se utiliza para recibir y validar las solicitudes de inicio de sesión (login) mediante el flujo de autenticación "OAuth 2.0 Resource Owner Password Credentials".El flujo "OAuth 2.0 Resource Owner Password Credentials" permite a los usuarios autenticarse mediante un nombre de usuario y una contraseña, obteniendo luego un token de acceso que se utiliza para autorizar el acceso a recursos protegidos en una API.El formulario OAuth2PasswordRequestForm te permite recibir las credenciales de inicio de sesión desde una solicitud POST y valida automáticamente los campos enviados en la solicitud. Los campos que espera recibir este formulario son:

#username: El nombre de usuario o identificador del usuario que se está autenticando.
#password: La contraseña del usuario que se está autenticando.
#scope (opcional): El alcance o los permisos requeridos para el token de acceso. Esto es específico para ciertos escenarios de OAuth 2.0 y puede no estar presente en todas las solicitudes.
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

#La importación from sqlalchemy.orm import Session es para utilizar la clase Session proporcionada por SQLAlchemy. La clase Session es parte de la funcionalidad de ORM (Mapeo Objeto-Relacional) de SQLAlchemy y se utiliza para administrar las interacciones con la base de datos.Una sesión en SQLAlchemy es una unidad de trabajo que representa una transacción con la base de datos. Se utiliza para agrupar un conjunto de operaciones y cambios en la base de datos en una transacción coherente. Las sesiones facilitan la comunicación con la base de datos, permitiendo realizar operaciones de lectura, escritura y actualización de datos. En pocas palabras,

#sessionmaker: Es un fabricante de sesiones (session factory) que se utiliza para crear instancias de sesiones. Controla cómo se establecen las conexiones y las transacciones a la base de datos. Cuando utilizas sessionmaker, estás configurando cómo las sesiones deben comportarse y cómo se crean.

#Session: Es una instancia de sesión real que se crea a partir del sessionmaker. Representa una transacción individual con la base de datos. Proporciona un contexto para realizar operaciones de lectura y escritura, así como para agrupar estas operaciones en una transacción coherente. La sesión mantiene una conexión activa a la base de datos durante su vida útil y te permite interactuar con la base de datos de manera segura y 
from sqlalchemy.orm import Session

from .. import database,schemas,models,utils,oauth2

#APIRouter es una clase proporcionada por FastAPI que se utiliza para crear un enrutador (router) dentro de una aplicación FastAPI. Un enrutador es una forma de organizar y agrupar rutas (endpoints) relacionadas en secciones o módulos específicos de una API. Asi mismo, evita la necesidad de importar fastapi en el documento necesariamente y usando APIRouter() y app.include_router() obtendriamos un codigo mas modular.
router=APIRouter(tags=["Authentication"],)


#antes estabamos usando el schemas.userLogin, pero esto no sirve del todo, ya que no podemos trabajar con datos de formulario , por eso se reemplaza por OAuthPasswordAuthent
@router.post('/login', response_model=schemas.Token)#para serealizar la respuesta a lo que se tiene que devolver con response_model, debe pasarse los mismo parametros o en caso de pasar un diccionacionario este debe tener el mimso nombre que los atributos del modelo.
def login(user_credentials:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(database.get_db)):
    #reemplazamos a user_credentials.email por user_credentials.username, por que al usar Oauth2PasswordRequestForm solo devolvera 2 campos, y el primero almacenara el correo,id o lo que sea dentro del nombre username y el segundo sera el password
    user=db.query(models.User).filter(models.User.email==user_credentials.username).first()#los tipos de cada atributo de objeto dependen de los tipos de datos definidos en los models.
    #print(type(user.create_at))
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Invalid Credentials")
    if not utils.verify(user_credentials.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Invalid Credentials")
    
    #create token aplicando la funcion de utils y return token
    #sera los campos que pasaremos para la cargautil Y sera importante para recuperarlos cuando estemos verificando
    acces_token=oauth2.create_access_token(data={"user_id":user.id})
    return {"access_token":acces_token,
    "token_type":"bearer"}#respuesta a seralizar al modelo de schemas.token, aun asi le pasemos mas campos se cambiara a lo  que le mande el modelo