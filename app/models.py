#SQLAlchemy es una biblioteca de mapeo objeto-relacional (ORM) en Python que proporciona una interfaz de alto nivel para interactuar con bases de datos relacionales. Su objetivo es simplificar la manipulación de datos almacenados en bases de datos y permitir el uso de conceptos orientados a objetos al trabajar con bases de datos.
"""
    Algunos de los tipos de datos comunes disponibles en SQLAlchemy son:
        Integer: Representa un campo de tipo entero en la base de datos.
        SmallInteger: Representa un campo de tipo entero pequeño.
        BigInteger: Representa un campo de tipo entero grande.
        Float: Representa un campo de tipo número de punto flotante.
        Numeric: Representa un campo de tipo número decimal.
        String: Representa un campo de tipo cadena de caracteres o texto.
        Text: Representa un campo de tipo texto largo.
        Boolean: Representa un campo de tipo booleano, que puede ser verdadero o falso.
        Date: Representa un campo de tipo fecha.
        Time: Representa un campo de tipo hora.
        DateTime: Representa un campo de tipo fecha y hora.
        Enum: Representa un campo de tipo enumerado, que contiene un conjunto de opciones predefinidas.
        JSON: Representa un campo de tipo JSON, que puede almacenar datos en formato JSON. 
"""
from sqlalchemy import Column, Integer,String, Boolean,DATETIME,ForeignKey
#from sqlalchemy.sql.sqltypes import TIMESTAMP


from sqlalchemy.orm import relationship


#La importación from sqlalchemy.sql.expression import text te permite acceder a la clase text proporcionada por SQLAlchemy. La clase text es utilizada para crear expresiones SQL directas o literales en tus consultas, lo que te permite ejecutar consultas SQL complejas y personalizadas que no se pueden expresar fácilmente con el mapeo ORM tradicional.La clase text se utiliza principalmente para ejecutar consultas SQL crudas o específicas que no necesariamente se ajustan al modelo de datos definido en tus clases y tablas de SQLAlchemy.
from sqlalchemy.sql.expression import text


from .database import Base


#la diferencia entre aplicar default y server_default es donde se evalua en resumen, la diferencia entre default y server_default radica en dónde se evalúa y aplica el valor predeterminado. default se evalúa en el lado del cliente antes de insertar el registro, mientras que server_default se evalúa y aplica por el servidor de la base de datos durante la operación de inserción. 
class User(Base):
    __tablename__ = 'users'
    id=Column(Integer, primary_key=True, nullable=False)
    email=Column(String(100),nullable=False, unique=True)
    password=Column(String, nullable=False)
    create_at=Column(DATETIME(timezone=True),nullable=False, server_default=text('GETDATE()'))

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer,primary_key=True, nullable=False)
    title=Column(String,nullable=False)
    content=Column(String,nullable=False)
    published=Column(Boolean, server_default='TRUE', nullable=False)
    create_at=Column(DATETIME(timezone=True),nullable=False, server_default=text('GETDATE()'))
    owner_id=Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False)
    #No busca el nombre de la tabla, si no el nombre de la clase para crear un objeto a partir de esto
    owner=relationship('User')


class Vote(Base):
    __tablename__='votes'
   
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey('posts.id', ondelete="NO ACTION"), primary_key=True)
    #TRUCO PIRUCO!, en caso de tener el error de que no se puede insertar 2 cascade en la misma tabla, es necesario cambiar un cascade por ! un NO ACTION! POR QUE EN SQL SERVER, ESTO ES CONOCIDO COMO CICLO O MULTIPLES RUTAS DE CASCADA ! LO QUE OCASIONARA DICHO ERRORR, PERO POSGRLSQL NO SUCEDE 