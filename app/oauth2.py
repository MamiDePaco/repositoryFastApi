#La biblioteca jose es una biblioteca de Python que proporciona funciones y herramientas para trabajar con JSON Web Tokens (JWT). Los JSON Web Tokens son un estándar abierto (RFC 7519) que se utiliza para transmitir información de forma segura entre dos partes en forma de objetos JSON. Los JWT son ampliamente utilizados para la autenticación y autorización en aplicaciones web y servicios RESTful.jose ofrece una serie de funciones para codificar y decodificar JWT, así como para validar la integridad de los tokens y verificar la firma digital.

    #algunas funcionaliades :Codificación y Decodificación,Verificación y Validación,Expiración y Tiempo de Vida,Algoritmos de Firma,Gestión de Errores.
    
#pip install python-jose[cryptography]
from jose import JWTError,jwt

from datetime import datetime,timedelta
from . import schemas,models,database

#from fastapi.security import OAuth2PasswordBearer: OAuth2PasswordBearer es una clase proporcionada por FastAPI que se utiliza para manejar la autenticación basada en el flujo de autenticación OAuth 2.0 con el método de concesión de credenciales de contraseña (Resource Owner Password Credentials Grant).OAuth 2.0 es un protocolo de autorización que permite que aplicaciones y servicios accedan a recursos protegidos en nombre del usuario. El flujo de concesión de credenciales de contraseña es uno de los métodos de autenticación proporcionados por OAuth 2.0 y se utiliza cuando un cliente confía al servidor sus credenciales de usuario directamente (nombre de usuario y contraseña) para obtener un token de acceso.Cuando utilizas OAuth2PasswordBearer, puedes agregarlo como una dependencia en una ruta o función de FastAPI para requerir autenticación. El token de acceso se pasará como un encabezado HTTP en la solicitud y será validado automáticamente por FastAPI para verificar si el usuario tiene permiso para acceder a la ruta o función.
from fastapi.security import OAuth2PasswordBearer


from fastapi import Depends,HTTPException,Response,status

#Este modulo como ya sabemos nos permite tener un unidad de interaccion con la bd, pero en este caso servira dentro de get_current_user para devolver informacion importante del usuario que vayamos a necesitar.
from sqlalchemy.orm import Session 
from .config import Settings
#-----------------------------------------------------------------------------------


#oauth2_schema=OAuth2PasswordBearer(tokenUrl="login"): La línea de código oauth2_schema = OAuth2PasswordBearer(tokenUrl="login") crea una instancia de la clase OAuth2PasswordBearer proporcionada por FastAPI para manejar la autenticación basada en el flujo de autenticación OAuth 2.0 con el método de concesión de credenciales de contraseña (Resource Owner Password Credentials Grant).La instancia creada (oauth2_schema) se utilizará como una dependencia en las rutas o funciones de FastAPI para requerir autenticación. Cuando se utiliza esta dependencia, FastAPI buscará el token de acceso en el encabezado HTTP "Authorization" y lo validará automáticamente para determinar si el usuario está autenticado y autorizado para acceder a la ruta o función.El argumento tokenUrl especifica la URL a la que los clientes deben enviar las solicitudes de autenticación para obtener un token de acceso. En este caso, se ha establecido la URL como "login", pero en una implementación real, debería ser la URL real donde se encuentra el endpoint para la autenticación OAuth2.
oauth2_schema=OAuth2PasswordBearer(tokenUrl="login")



#SECRET_KEY
#ALGORITHM
#TIME_EXPIRED
SECRET_KEY = Settings.secret_key
ALGORITHM=Settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES=Settings.acces_token_expire_minutes




#data sera la carga util del token
def create_access_token(data:dict):  # lo que se recibe es una beta del payload que queremos mandar.
    
    #al estar cambiando algunas cosas, no queremos cambiar la data original, por ende copiaremos dicha data y la almanecaremos en una nueva data
    to_encode= data.copy()
    
    expire=datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp":expire})
    #campos a pasar :jwt.encode(payload,secret_key,algorithm)
    encode_jwt=jwt.encode(to_encode,SECRET_KEY,ALGORITHM)
    return encode_jwt



def verify_token(token:str,credentials_exception):
    try:
        #descodificamos el jwt obteniendo un diccionario clave:valor
        payload=jwt.decode(token,SECRET_KEY,[ALGORITHM])
        #se usa método get() : valor = diccionario.get(clave) para acceder el valor de un clave en especfica
        id:str=payload.get('user_id') # se le coloca str por que si fuera int, que es el valor por defecto de ese dato, no podriamos aplicar NONE, ya que esto es predilecto de los str y no de los int.
       
        #comprobamos que exista, y si no es asi lanzamos un excepcion
        if id is None:
            raise credentials_exception
        # creamos una instancia de la clase tokenData pasandole como argumento el id
        token_data=schemas.tokenData(id=id) 
    except JWTError: 
        raise credentials_exception 
    #retornamos la istancia debido a ""
    return token_data








""" tenemos una forma distinta  de implementar la funcion get_current_user, donde antes solo se regresaba el id, que era lo unico que se devolvia despues de instanciar schemas.tokenData(id=id),pero esto no resulta tan bien, por que nos limita.

        def verify_token(token:str,credentials_exception):
        try:
            payload=jwt.decode(token,SECRET_KEY,[ALGORITHM])
        
            id:str=payload.get('user_id') # se le coloca str por que si fuera int, que es el valor por defecto de ese dato, no podriamos aplicar NONE, ya que esto es predilecto de los str y no de los int.
            #comprobamos que exista, y si no es asi lanzamos un excepcion
            if id is None:
            raise credentials_exception
            # creamos una instancia de la clase tokenData pasandole como argumento el id
            token_data=schemas.tokenData(id=id) 
        except JWTError: 
                raise credentials_exception 
        return token_data
"""
def get_current_user(token:str=Depends(oauth2_schema),db:Session=Depends(database.get_db)):
    #asignamos la respuesta de httpexception a una variable
    credentials_exception= HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f"could not validate credentials",headers={"WWW-Authenticate":"Bearer"})
    #pasamos parametros  a la funcion que creamos y la retornamos 
    token=verify_token(token,credentials_exception)
    user=db.query(models.User).filter(models.User.id==token.id).first()
    #print(type(user))
    return user