from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas, security, crud
from app.database import get_db
# 1. Importe OAuth2PasswordRequestForm
from fastapi.security import OAuth2PasswordRequestForm

# Define o roteador para as rotas relacionadas a Usuários
router = APIRouter(prefix="/usuarios", tags=["Usuários"])

# Rota POST para CRIAR um novo usuário
@router.post("/", response_model=schemas.Usuario)
def criar_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    """
    Cria um novo usuário com senha criptografada.
    """
    # Verifica se o e-mail já existe
    usuario_existente = db.query(models.Usuario).filter(models.Usuario.email == usuario.email).first()
    if usuario_existente:
        raise HTTPException(status_code=400, detail="E-mail já cadastrado.")

    # Criptografa a senha antes de salvar
    senha_hash = security.gerar_hash(usuario.senha)
    novo_usuario = models.Usuario(
        email=usuario.email,
        nome=usuario.nome,
        senha_hash=senha_hash
    )
    db.add(novo_usuario)

# Cria um calendário vazio para o novo usuário
    novo_calendario = models.Calendario(usuario_email=novo_usuario.email)
    db.add(novo_calendario)

# Commit as mudanças no banco de dados    
    db.commit()
    db.refresh(novo_usuario)
    return novo_usuario

# Rota POST para LOGIN e obtenção de token OAuth2
@router.post("/login", response_model=schemas.Token) 
def login(
    # 2. Mude o parâmetro de entrada para usar OAuth2PasswordRequestForm
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
):
    """
    Faz login para obter um token de acesso OAuth2.
    Esta rota é usada pelo botão 'Authorize' no /docs.
    """

    # 3. Use 'form_data.username' para pegar o e-mail
    # O Swagger UI envia o campo 'username', que usaremos como e-mail.
    usuario = db.query(models.Usuario).filter(models.Usuario.email == form_data.username).first()

    # 3. Use 'form_data.password' para pegar a senha
    if not usuario or not security.verificar_senha(form_data.password, usuario.senha_hash):
        # Unifique as mensagens para evitar dar dicas
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail (username) ou senha incorretos.",
            # É uma boa prática adicionar este header na falha de login
            headers={"WWW-Authenticate": "Bearer"}, 
        )

    # 1. Cria o token de acesso
    access_token = security.create_access_token(
        data={"email": usuario.email}
    )

    # 4. Retorne APENAS o token, no formato que o Swagger espera
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

# Rota GET para obter os dados completos do usuário logado
@router.get("/me", response_model=schemas.UsuarioResponseCompleto)
def get_meus_dados_completos(
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(security.get_current_user)
):
    """
    Endpoint protegido para "recarregar" o perfil.
    
    Retorna todos os dados do usuário logado (perfil, calendários e
    todos os eventos aninhados com seus transportes, datas, etc.).
    """
    
    # Esta função não precisa de mudança, pois ela já usa
    # a dependência 'get_current_user' que funciona com o token.
    usuario_data = crud.get_user_full_data(db, email=current_user.email)
# Verifica se o usuário foi encontrado    
    if not usuario_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Usuário não encontrado."
        )
        
    return usuario_data