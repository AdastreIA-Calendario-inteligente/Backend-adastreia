# é isso que o frontend precisa me enviar 


from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Formulário para CRIAR um usuário 
class UsuarioCreate(BaseModel):
    email: str
    nome: str
    senha: str  

# Formulário para LER um usuário (o que o backend devolve)
class Usuario(BaseModel):
    email: str
    nome: str
    
    class Config:
        from_attributes = True 
