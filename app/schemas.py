
#BaseModel es una clase base proporcionada por la biblioteca Pydantic que te permite definir modelos de datos de forma sencilla y con validaciones incorporadas. Estos modelos te permiten describir la estructura y los tipos de datos que se esperan en tu aplicación.Aquí están algunos aspectos clave sobre BaseModel:
#Definición de modelos:Puedes crear modelos de datos utilizando BaseModel y definir los campos  que deseas para representar la estructura de datos de tu aplicación. Cada campo está definido como una variable de clase dentro del modelo y debe tener un tipo de dato asociado.

#Validación automática:Pydantic proporciona validaciones automáticas para los campos definidos en el modelo. Cuando creas una instancia del modelo, Pydantic verificará automáticamente que los valores proporcionados cumplan con los tipos de datos especificados y otras validaciones definidas, como la longitud máxima de una cadena, rangos numéricos, etc.

#Conversión de tipos:Pydantic también se encarga de la conversión de tipos. Por ejemplo, si defines un campo como tipo int, pero se proporciona un valor como "42" (cadena), Pydantic automáticamente convertirá ese valor a un entero.

#Valores predeterminados:Puedes proporcionar valores predeterminados para los campos del modelo. Si un campo no se proporciona al crear una instancia del modelo, tomará el valor predeterminado que hayas definido.

#Anotaciones de tipos:Pydantic utiliza las anotaciones de tipos de Python para inferir los tipos de datos de los campos del modelo. Por lo tanto, puedes aprovechar las anotaciones de tipos para mejorar la legibilidad y comprensión de tu código.

#Herencia:Los modelos de Pydantic admiten la herencia, lo que te permite definir un modelo base con campos comunes y luego crear subclases que hereden esos campos y agreguen campos adicionales.

"""EmailStr es un tipo específico de campo proporcionado por Pydantic para representar direcciones de correo electrónico. Al usar EmailStr, Pydantic se asegura de que el valor proporcionado para este campo sea una dirección de correo electrónico válida."""
from pydantic import BaseModel,EmailStr,conint
#from typing import Optional se utiliza en Python para importar el tipo Optional que proviene del módulo typing. Este tipo se utiliza para indicar que un valor puede ser opcional o nulo (None). Es especialmente útil cuando trabajas con funciones o atributos que pueden no tener un valor definido en ciertos casos.
from typing import Optional
#La importación from datetime import datetime te permite utilizar la clase datetime del módulo datetime en Python. La clase datetime es parte de la biblioteca estándar de Python y se utiliza para trabajar con fechas y horas en tus programas.Con datetime, puedes crear objetos que representen fechas y horas específicas, y también realizar operaciones como cálculos de diferencia entre fechas, formatear fechas para mostrarlas en diferentes formatos, entre otras funcionalidades.
from datetime import datetime
 
 
 
#------------------------------------------------------------------------------
#todos los atributos que se definen en las clases deben por obligacion ser los mismo que se mandan en la data en forma de JSON , es decir lo que enviamos por postman o en otro remoto caso en json , las claves deben ser iguales! a las que se definen en las clases de molelos pydantic. 
 
#{
#    "title":"He aprendido ",
#    "content":"las rutas estan protegidas gracias a! el poderoso auth",
#    "published":0,
#   "owner_id":12
#}


class UserCreate(BaseModel):
    email:EmailStr
    password:str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    create_at:datetime
    class Config:
        from_attributes= True



class UserLogin(BaseModel):
    email:EmailStr
    password:str


 
 
class PostBase (BaseModel):
    #This does not allow any of the fields to be sent as empty
    title:str
    content:str
    published:bool=True
    #rating: Optional[int]=None

class PostCreate(PostBase):
    #owner_id: Optional[int] # al parecer no puedo dejarlo asi, para decir que el owner_id no es totalmente necesario y que se calculara internamente y se asginara. por eso solo se pondra pass e internamente se asignara
    pass

class Post(PostBase):
    id:int
    create_at:datetime
    owner_id:int
    owner:UserOut
    #esto es necesario para hacer que un modelo alchemy pueda ser comprendido por un modelo pydantic
    class Config:
        from_attributes= True
        
class PostOut(BaseModel):
    Post:Post
    votes:int
    class Config:
        from_attributes= True
  

class Token(BaseModel):
    access_token:str
    token_type:str

class tokenData(BaseModel):
    id: Optional[int]=None # se coloca int, por que es el tipo de dato que va a regresar la query hecha con sqlalchemy, y esto lo podemos personalizar en los models, con sus tipos de datos de cadad column.
    
    
class Vote(BaseModel):
    post_id: int
    dir:conint(ge=0,le=1)