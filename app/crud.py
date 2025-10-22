
#from sqlalchemy.orm import Session
#from . import models, schemas

# tem que fazer a segurança dessa prte 
#from .security import get_password_hash 



#def create_user(db: Session, user: schemas.UsuarioCreate):
    # 1. Recebe o 'formulário' (schema) com a senha pura
    # 2. Faz o trabalho de segurança (gerar o hash)
   #hashed_password = get_password_hash(user.senha)
    
    # 3. Cria o objeto do 'cofre' (modelo) com o dado seguro
    #db_user = models.Usuario(
        #email=user.email,
        #nome=user.nome,
        #senha_hash=hashed_password # <--- Salva o hash, não a senha
    #)
    
    # 4. Guarda no cofre
    #db.add(db_user)
    #db.commit()
    #db.refresh(db_user)
    
    # 5. Devolve o objeto do cofre
    #return db_user