"""" Este es un modulo de funciones utiles para el funcionamiento"""


#La clase CryptContext de la biblioteca Passlib se utiliza para manejar el almacenamiento seguro y la verificación de contraseñas en una aplicación. Passlib es una biblioteca de Python que proporciona funciones seguras para trabajar con contraseñas, incluyendo el almacenamiento seguro (hashing) y la verificación de contraseñas para autenticación.Aquí te explico cómo funciona CryptContext y cómo se combina con la biblioteca jose para trabajar juntos en la seguridad de contraseñas:

#CryptContext:
#CryptContext es un objeto que actúa como un contexto para administrar y configurar diferentes esquemas de hash y opciones de almacenamiento seguro de contraseñas. Con CryptContext, puedes especificar una lista de esquemas de hash para almacenar contraseñas, y luego usar métodos como hash() para crear hashes seguros y verify() para verificar contraseñas almacenadas con los hashes generados.

"""en una aplicación web que utiliza JWT para autenticación, es común utilizar una biblioteca de almacenamiento seguro de contraseñas como Passlib con CryptContext para almacenar contraseñas de usuarios de forma segura en la base de datos. Luego, cuando un usuario intenta iniciar sesión, la contraseña proporcionada se verifica utilizando CryptContext y, si es válida, se puede generar un token JWT para permitir al usuario acceder a recursos protegidos."""

#pip install passlib[bcrypt]
from passlib.context import CryptContext

"""
 En esta línea de código, estás creando un objeto CryptContext llamado pwd_context con la siguiente configuración:

schemes=["bcrypt"]:
Este parámetro especifica una lista de esquemas de hash que se utilizarán para almacenar las contraseñas. En este caso, se está utilizando únicamente el esquema "bcrypt". bcrypt es un algoritmo de hash de contraseña seguro y ampliamente utilizado en aplicaciones web debido a su resistencia a los ataques de fuerza bruta y su capacidad para hacer que el proceso de hash sea computacionalmente costoso.

Puedes proporcionar varios esquemas en una lista, y Passlib seleccionará automáticamente el esquema adecuado cuando almacenes o verifiques contraseñas. Sin embargo, en este caso, solo se está utilizando bcrypt.

deprecated="auto":
Este parámetro determina el comportamiento de Passlib cuando un esquema de hash se considera obsoleto o inseguro. En este caso, se ha establecido en "auto", lo que significa que Passlib decidirá automáticamente si un esquema de hash específico está obsoleto o no, basándose en sus propias políticas internas de degradación.

Si un esquema de hash se marca como obsoleto, Passlib seguirá admitiendo la verificación de contraseñas almacenadas con ese esquema, pero generará un nuevo hash utilizando el esquema más seguro al almacenar nuevas contraseñas. Esto ayuda a garantizar que las contraseñas nuevas se almacenen de forma segura y que los usuarios actuales puedan seguir autenticándose sin problemas.

Si lo prefieres, también puedes configurar deprecated a True o False de manera explícita para permitir o evitar el uso de esquemas de hash obsoletos respectivamente.
"""
pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")

#Funcion para hashear las contraseñas
def hash(password:str):
    return pwd_context.hash(password)


#Funcion para verificar las contrasenias
def verify(plain_password,hashed_password):
    #retorna true or false
    return pwd_context.verify(plain_password,hashed_password)
