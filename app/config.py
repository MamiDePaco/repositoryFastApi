#BaseSettings es una clase base proporcionada por Pydantic que se utiliza para definir modelos de configuración en aplicaciones. Los modelos de configuración se utilizan para validar, cargar y acceder a las variables de entorno y configuración de una aplicación.Un modelo de configuración basado en BaseSettings suele contener campos que representan las variables de configuración que tu aplicación necesita. Pueden ser cadenas, enteros, booleanos y otros tipos de datos. Pydantic se encargará de validar que los valores 
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    #los atributos declarados tienen que ser estrictamente los mismos que en el .env, minusculas o mayuculas al parecer tambien
    database_hostname:str
    database_port:str
    database_password:str
    database_name:str
    database_username:str
    secret_key:str
    algorithm:str
    acces_token_expire_minutes:int
    class Config:
        env_file=".env" #esta linea indica! de que archivo va  traer los datos.
    
    
#instanciamos
Settings=Settings()