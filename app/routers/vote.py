from fastapi import HTTPException, Response,status,APIRouter,Depends
from .. import schemas,database,models,oauth2
from sqlalchemy.orm import Session


router=APIRouter(
    prefix="/vote",
    tags=['Vote']
    
)
@router.post('',status_code=status.HTTP_201_CREATED)
async def vote(vote:schemas.Vote,db:Session=Depends(database.get_db),current_user:int=Depends(oauth2.get_current_user)):
    #logica para ver si se esta tratando de votar sobre una publicacion que no existe
    post=db.query(models.Post).filter(models.Post.id==vote.post_id).first()
    
    #La sentencia if not evalúa cualquier valor que pueda ser convertido a un valor booleano (True o False). En Python, se consideran valores falsos (que evaluarán como True en if not) los siguientes:
    #None: El valor nulo.
    #False: El valor booleano False.
    #Cualquier número igual a 0: Por ejemplo, 0, 0.0, 0j.
    #Secuencias y colecciones vacías: Por ejemplo, cadenas vacías (""), listas vacías ([]), tuplas vacías (()), diccionarios vacíos ({}), conjuntos vacíos (set()).
    #Objetos que implementan el método __bool__() o __len__() y retornan False o 0, respectivamente.
    #Cualquier otro valor que no sea None, False, 0 ni una secuencia o colección vacía se considera verdadero y evaluará como False en if not.
    if not post :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Vote with id: {vote.post_id}does not exist')
    
    #logica para insertar o eleminar un voto
    #consultamos a la bd si existe alguna fila que cumpla con la clave primaria (compuesta por 2 rows)
    vote_query=db.query(models.Vote).filter(models.Vote.post_id==vote.post_id,models.Vote.user_id==current_user.id)#se puede seguir agregnado condiciones en filter, lo que conlleva  a que sa fila cumpla para ambas condiciones
    #al ser una actualizancion,creacion o eliminacion, necesitamos dividir la consulta en 2, una es la consulta sql como tal(vote_query) y foun_vote que es el objeto en si, luego de aplicar first() o all()
    found_vote=vote_query.first()
    if(vote.dir==1): #DIR==1 cuando quiera insertar
        #En Python, los siguientes valores se consideran "truthy", lo que significa que se evaluarán como True en un contexto booleano (como una sentencia if), y los demás se consideran "falsy" y se evaluarán como False:
        #Valores truthy:

        #Cualquier objeto que no sea None
        #Números diferentes de cero (enteros y flotantes)
        #Cadenas no vacías
        #Listas, tuplas, conjuntos y diccionarios no vacíos
        #Funciones y clases definidas por el usuario
        #Objetos personalizados que implementen el método __bool__() o __len__() y devuelvan True
        
        #Valores falsy:

        #None
        #Cero en todas sus formas (0, 0.0, 0j)
        #Cadenas vacías ("" o '')
        #Listas, tuplas, conjuntos y diccionarios vacíos
        #Objetos personalizados que implementen el método __bool__() o __len__() y devuelvan False
        if found_vote: #si es 
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f'user {current_user.id}has alredy voted on post{vote.post_id}')
        new_vote=models.Vote(post_id=vote.post_id,user_id=current_user.id)# instanciamos un objeto para poder introducirlo en la bd
        db.add(new_vote)
        db.commit()
        return{'message':'succesfully added vote'}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Vote does not exist')
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"messagge":"Successfully deleted vote"}

