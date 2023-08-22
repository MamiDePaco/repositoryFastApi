#create_engine es una función proporcionada por SQLAlchemy que se utiliza para crear una conexión o un motor de base de datos. Esta función es fundamental para interactuar con bases de datos en SQLAlchemy y es una parte clave de cómo se establece la comunicación entre tu aplicación Python y la base de datos.
from sqlalchemy import create_engine

#sessionmaker es una función proporcionada por SQLAlchemy que se utiliza para crear una fábrica de sesiones (session factory). Una sesión es una unidad de trabajo que representa una transacción con la base de datos. La sesión es utilizada para agrupar un conjunto de operaciones de base de datos en una transacción coherente.La función sessionmaker se utiliza para configurar cómo se deben crear y administrar las sesiones en la aplicación. Puedes proporcionar ciertos parámetros y opciones a sessionmaker para personalizar el comportamiento de las sesiones, como por ejemplo, si se debe habilitar el autoflush, autocommit, entre otros..
from sqlalchemy.orm import sessionmaker

#declarative_base es una función proporcionada por SQLAlchemy que se utiliza para crear una clase base de modelos declarativos. Los modelos declarativos son una forma conveniente y legible de definir estructuras de tablas de base de datos y relaciones entre tablas utilizando clases de Python.El uso de declarative_base permite definir tus modelos utilizando clases Python, en lugar de escribir código SQL directamente. Esto hace que el código sea más legible, más fácil de mantener y menos propenso a errores.
from sqlalchemy.ext.declarative import declarative_base 
from .config import Settings

#SQLACHEMY_DATABASE_URL='sqlserver://<username>:<password>@<ip-addres/hostname>/<database_name>'
SQLACHEMY_DATABASE_URL = f'mssql+pyodbc://{Settings.database_username}:{Settings.database_password}@{Settings.database_hostname}/{Settings.database_name}?driver=ODBC+Driver+17+for+SQL+Server'

#se esta creando el motor de la conexion
engine=create_engine(SQLACHEMY_DATABASE_URL)


"""
autocommit=False: Este parámetro controla el modo de autocommit de las transacciones en la sesión. Cuando autocommit está establecido en False, las transacciones no se confirman automáticamente después de cada operación. Esto significa que si realizas cambios en la base de datos (como insertar, actualizar o eliminar registros), deberás confirmar explícitamente la transacción mediante el método commit() para que los cambios se apliquen permanentemente a la base de datos. Si autocommit estuviera en True, cada operación individual se confirmaría automáticamente, lo que puede tener implicaciones en el rendimiento y la consistencia de los datos.

autoflush=False: Este parámetro controla el modo de autoflush de la sesión. Cuando autoflush está establecido en False, los cambios en los objetos de la sesión (por ejemplo, la modificación de propiedades de un modelo) no se sincronizan automáticamente con la base de datos hasta que realices una operación que requiera una consulta a la base de datos (por ejemplo, una consulta query(), commit() o flush()). Esto puede ser útil para evitar consultas innecesarias a la base de datos cuando estás realizando múltiples modificaciones en la sesión y deseas controlar cuándo se aplican esos cambios a la base de datos.

bind=engine: Este parámetro especifica el motor de base de datos al que se va a conectar la sesión. El objeto engine que proporcionas aquí es el que se creó previamente con create_engine y contiene la información necesaria para conectarse a la base de datos.
"""
sesionLocal=sessionmaker(autocommit=False, autoflush=False, bind=engine)


#Crea una clase base: declarative_base() crea una clase base que actúa como una fábrica para tus modelos de tablas. A partir de esta clase base, puedes definir tus propios modelos como subclases y cada modelo representará una tabla en tu base de datos.
Base=declarative_base() 


# Dependency
def get_db():
    db = sesionLocal()
    try:
        yield db
    finally:
        db.close()

 