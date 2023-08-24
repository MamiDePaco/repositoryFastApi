from fastapi import FastAPI, Response, status, HTTPException,Depends,APIRouter
from ..import models,schemas,oauth2
from sqlalchemy import desc,asc,func# importado para poder usar un order by en una clausula que use limit o offset, para evitar el error :sqlalchemy.exc.CompileError: MSSQL requires an order_by when using an OFFSET or a non-simple LIMIT clause
from sqlalchemy.orm import Session,joinedload,aliased # joinedload es para poder abujtar 
from ..database import get_db
from typing import List,Optional,Any

router=APIRouter(
    prefix="/posts",
    tags=["posts"]
)



#method GET
@router.get("",response_model=List[schemas.PostOut]) 
async def get_post(db:Session=Depends(get_db),current_user:schemas.tokenData=Depends(oauth2.get_current_user),limit:int=10,skip:int=0,search:Optional[str]=""):
    # si quisieramos solo ver las publicaciones de un mismo usuario ,seria la siguiente logica.
    #posts=db.query(models.Post).filter(models.Post.owner_id==current_user.id).all()
    
    
    
        #aclaracion------------------------------------
        #existe la carga peresoza, que es una funcionalidad de fastApi y pydantic .
        #La carga perezosa (lazy loading) es una estrategia de carga de datos utilizada en ORM (Mapeo Objeto-Relacional) como SQLAlchemy. En lugar de cargar todos los datos relacionados de inmediato al recuperar un objeto principal de la base de datos, la carga perezosa retrasa la carga de los datos relacionados hasta que se accede explícitamente a ellos.En el contexto de SQLAlchemy (y otros sistemas ORM similares), la carga perezosa significa que las propiedades que representan relaciones con otras tablas o entidades no se cargan automáticamente al recuperar un objeto principal. En su lugar, se realiza una consulta adicional a la base de datos solo cuando se accede a la propiedad relacionada.
        
        
        #Carga Perezoza (Lazy Loading):

        #Ventajas:

        #Las consultas iniciales pueden ser más rápidas y ligeras, ya que solo recuperan la información necesaria en ese momento.No se realizan consultas adicionales hasta que se accede a la relación, lo que puede ser más eficiente en algunos casos.Puede ser útil para evitar traer información innecesaria si no se planea utilizarla en ese momento.
        
        #Desventajas:

        #Si accedes a múltiples propiedades relacionadas en diferentes puntos de tu código, podrías incurrir en múltiples consultas a la base de datos, lo que podría afectar el rendimiento.Si no tienes cuidado, podrías tener un problema conocido como N+1 queries, donde se realizan muchas consultas individuales en lugar de una consulta eficiente para recuperar múltiples registros.

        #joinedload (o Técnicas Similares):

        #Ventajas:
        #Permite recuperar todas las relaciones necesarias en una sola consulta, lo que puede ser más eficiente para consultas que requieren información relacionada.
        #Evita el problema de N+1 queries al cargar todas las relaciones de una vez.
        
        #Desventajas:
        #Puede generar consultas más complejas y pesadas en términos de rendimiento si las relaciones son demasiado extensas o innecesarias para la consulta actual.
        #Puede traer más datos de los necesarios si no se planifica adecuadamente.


        #Consideraciones:
        #La elección depende del uso específico del sistema y los requisitos de rendimiento.Si sabes de antemano que siempre necesitarás ciertas relaciones, es más eficiente cargarlas con joinedload desde el principio.Si la información relacionada no se utilizará en todas las consultas, la carga perezosa podría ser una opción más eficiente para evitar traer datos innecesarios.
        #----------------------------------------------
        #explicacion de options
        #-------------------------------------------------
        #options en SQLAlchemy te permite aplicar varias opciones o modificadores a una consulta para personalizar su comportamiento. Aquí hay algunas opciones comunes que puedes utilizar junto con options:

        #joinedload: Como ya mencionamos, esta opción te permite cargar anticipadamente datos de relaciones específicas al realizar la consulta.

        #defer: Esta opción te permite diferir la carga de columnas específicas hasta que sean accedidas por primera vez. Esto puede ser útil si tienes columnas con datos grandes o costosos de recuperar, y no necesitas acceder a ellos en todas las consultas.

        #undefer: Es el complemento de defer. Si has diferido ciertas columnas, undefer te permite cargarlas explícitamente en una consulta posterior.

        #selectinload: Similar a joinedload, pero en lugar de realizar un join en la consulta, utiliza una subconsulta para cargar los datos relacionados.

        #subqueryload: Carga los datos relacionados utilizando una subconsulta independiente en lugar de un join.

        #eagerload: Carga datos relacionados de manera anticipada, pero no siempre de la forma más eficiente. Puede generar más consultas de las necesarias en algunas situaciones.

        #contains_eager: Una versión avanzada de joinedload que te permite cargar relaciones de forma anticipada y también acceder a las propiedades de esas relaciones en la misma consulta.

        #defaultload: Carga datos de relaciones en función de cómo estén configuradas por defecto en el modelo.

        #lazyload: Utiliza la carga perezosa para cargar datos relacionados.

        #noload: Evita cargar datos relacionados.
        #-------------------------------------------------
    #----------------------------------------------------------------------------------------
    #postprueba=db.query(models.Post).filter(models.Post.title.contains(search)).options(joinedload(models.Post.owner)).order_by(asc(models.Post.id)).limit(limit).offset(skip).all()
    
    #esta consulta no puede ser realizada por sql server, solo por postgresql por que implica traer en el select campos que no estan introducidos en el group by 
    #postprueba=db.query(models.Post.id,func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id==models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).order_by(asc(models.Post.id)).limit(limit).offset(skip).all()
    
    #sub query
    v = aliased(
    db.query(models.Vote.post_id, func.count().label('total_likes'))
    .group_by(models.Vote.post_id)
    .subquery()
    )

    # Consulta principal
    query = (
    db.query(
        models.Post,
        func.coalesce(v.c.total_likes, 0).label('votes')
    ).outerjoin(v, models.Post.id == v.c.post_id)
    )
    postprueba = query.filter(models.Post.title.contains(search)).order_by(asc(models.Post.id)).limit(limit).offset(skip).all()
    

    #filter, damos uso de la funcion contains(), para pasarle la variable  a ser buscada, pero ! asi mismo !, los espacio en la data que se pase por la url debe ser reemplazados por  %20 
    #joinedload es una de las opciones disponibles en SQLAlchemy y se utiliza para indicar que deseas cargar una relación específica de manera explícita y anticipada al realizar la consulta. Es decir, con joinedload, SQLAlchemy realizará una consulta que incluirá la información de la relación en la misma consulta que se utiliza para recuperar los objetos principales. Esto ayuda a evitar consultas adicionales para cargar datos relacionados más adelante.
    #order by especifica como se ordenara los registros para luego pasar a ser devueltos
    #limit es la cantidad de registros
    #offset es la cantidad de registros que son obviados
    #------------------------------------------------------------------------------------------
    #posts=db.query(models.Post).all()
    print("solo soy algo que se creo para cambiar el codigo para subir a git")
    return postprueba

@router.post("/{id}",response_model=schemas.PostOut)
async def get_only_post(id:int,db:Session=Depends(get_db),current_user:schemas.tokenData=Depends(oauth2.get_current_user)):
    # we need that id to be a integer, because normally the data send of a Api is a string.
    #print(type(id))
    v = aliased(
    db.query(models.Vote.post_id, func.count().label('total_likes'))
    .group_by(models.Vote.post_id)
    .subquery()
    )

    # Consulta principal
    query = (
    db.query(
        models.Post,
        func.coalesce(v.c.total_likes, 0).label('votes')
    ).outerjoin(v, models.Post.id == v.c.post_id)
    )
    post_found=query.filter(models.Post.id==id).first()
    if not post_found: 
        #response.status_code= status.HTTP_404_NOT_FOUND
        #return {"message":f"Post with id {id} not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id {id} not found")
    #SI Quisieramos que nuestra aplicacion no pueda llamar a post que no sean suyos, es decir debe pertenecerla a una sola persona
    #if post_found.owner_id != current_user.id:
        #raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f'Not authorized to perform requested action')
    return post_found


#method POST
@router.post("", status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
#en get_curent_user es int , segun chatgpt me dice que no deberia ser un int , mas bien deberia ser un schemas.tokenData. (DEJARE LA EXPLICACION DEBAJO COMENTADO )
async def create_post(new_post:schemas.PostCreate,db:Session=Depends(get_db),current_user:models.User=Depends(oauth2.get_current_user)):#El "current_user" sera la dependencia que establcera que se inicie sesion antes, asi como tambien contendra informacion del usuario llamado. "NO ES SEGURO AUN POR QUE NO HEMOS PERSONALIZADO QUE NOS DARA CON UN REPONSE.MODEL"
    
    #instanciando una objeto de la clase models.Post y se le esta pasando parametros, los cuales puede ser pasados de esta forma , desenpaquetando un diccionario o asignar por nombre.
    post=models.Post(owner_id=current_user.id,**new_post.dict())

    db.add(post)
    db.commit()
    db.refresh(post)
    #debido a que estamosrecuperando y retornado un modelo alchemys, este debera ser interpretado por un modelo pydantic con la clase config
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id:int,db:Session=Depends(get_db),current_user:schemas.tokenData=Depends(oauth2.get_current_user)):
    
    post_found=db.query(models.Post).filter(models.Post.id==id)#No se coloca .first(), por que  debajo se tendra que usar .delete()
    #aunque tambien podemos crear otra variable = post=post_found.first() y sobre esta usar
    
        #print(post_found) # cuando se devuelve sin un first ni un all, se devuleve una sentencia sql como tal
        #print(post_found.first())# cuando se emplea los metodos first o all , este devuelve un fabuloso objeto!!!
    if post_found.first()==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'post with id {id} not found')
    #logica para impedir que un usuario autenticado entre a borrar publicaciones de otras personas
    if post_found.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f'Not authorized to perform requested action')
    #se necesita realizar la accion delete sobre la misma query, sin aplicar all() ni first(),ya que en teoria
    post_found.delete(synchronize_session=False)
    db.commit()

    return 
    {
        Response(status_code=status.HTTP_204_NO_CONTENT)
    }



@router.put("/{id}",response_model=schemas.Post)
async def update_post(id:int , update_post:schemas.PostCreate, db:Session=Depends(get_db),current_user:schemas.tokenData=Depends(oauth2.get_current_user)):
    post_query=db.query(models.Post).filter(models.Post.id == id)
    post=post_query.first()
    if post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'post with id {id} not found')
    #logica para impedir que un usuario autenticado entre a actualizar publicaciones de otras personas
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f'Not authorized to perform requested action')
    
    #necesitamos pasar como un parametro un diccionario, que sera la info a actualizar
    # el famoso dict() solo funciona en pydantic models, no en alchemys models
    post_query.update(update_post.dict(),synchronize_session=False)
    db.commit()
    # por lo que pude ver, es que no puedo llamar a solo  post, por que por mas que tenga .first() no lo aplica, por eso debemos usar post_query.first(), tal vez una explicacion es que una vez actualizado ya no exista el post como tal, por eso otra vez tendriamos que llamar a la query como tal 
    return post_query.first()











#EXPLICACIONES 
"""Mis disculpas por la confusión en mi respuesta anterior. Tienes toda la razón.En el código proporcionado, get_current_user es una dependencia que devuelve un objeto de clase tokenData, que tiene un atributo id de tipo Optional[str]. Sin embargo, en la declaración de la función create_post, se está utilizando get_current_user:int=Depends(oauth2.get_current_user).Esto no es correcto, ya que estás especificando que el parámetro get_current_user debe ser de tipo int, pero la dependencia en realidad devuelve un objeto de tipo tokenData.Para corregirlo, simplemente cambia la declaración de la función create_post para que refleje el tipo correcto que devuelve la dependencia get_current_user. Por ejemplo:


from fastapi import Depends

# ... código anterior ...

async def create_post(new_post: schemas.PostBase, db: Session = Depends(get_db), get_current_user: schemas.tokenData = Depends(oauth2.get_current_user)):
    # Resto del código de la función create_post


    
Aquí, estamos especificando que el parámetro get_current_user debe ser de tipo schemas.tokenData, que es el tipo que devuelve la dependencia oauth2.get_current_user. Al hacer esto, la dependencia se inyectará correctamente en la función y podrás acceder a los atributos del objeto tokenData sin problemas. , en esta rspuesta que me distes que errores puede haber si lo dejo como int
Si dejas el parámetro get_current_user como int en la función create_post, podrías enfrentar algunos problemas cuando intentes acceder a los atributos del objeto tokenData en el cuerpo de la función. Aquí hay algunos problemas potenciales:

Errores de tipo: Si intentas acceder a los atributos de get_current_user, como get_current_user.id, Python arrojará un error de tipo porque un objeto int no tiene un atributo llamado id.

Pérdida de información: Al declarar get_current_user:int=Depends(oauth2.get_current_user), Python tratará de convertir el objeto tokenData devuelto por la dependencia en un entero, lo cual resultará en la pérdida de información. No podrás acceder a los atributos del objeto tokenData.

Respuestas inesperadas: Si el tipo de get_current_user es forzado a ser int, esto podría llevar a comportamientos inesperados en tu código más adelante, ya que se está cambiando el tipo real del objeto que se pasa a la función.

Para evitar estos problemas, es importante definir el tipo del parámetro get_current_user de acuerdo con el tipo que devuelve la dependencia oauth2.get_current_user, que en este caso es schemas.tokenData. Así, el objeto tokenData estará disponible en el cuerpo de la función y podrás acceder a sus atributos correctamente."""