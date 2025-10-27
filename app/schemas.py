# é isso que o frontend precisa me enviar 
from datetime import datetime, date, time
from typing import Optional, List
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

# Formulário para LOGIN de usuário 
class UsuarioLogin(BaseModel):
    email: str
    senha: str

# Base para criar um Transporte
class TransporteBase(BaseModel):
    meio: str
    ida: Optional[str] = None
    volta: Optional[str] = None

# Base para o Tipo de Evento
class TipoEventoBase(BaseModel):
    tipo: str

# Schema de criação de Evento (o que o usuário envia)
class EventoCreate(BaseModel):
    id_calendario: int # Precisa deste ID para vincular o evento
    nome: str
    local: Optional[str] = None
    duracao: Optional[time] = None
    hora_inicio: Optional[time] = None
    local_de_saida: Optional[str] = None
    
    # Detalhes que são criados em tabelas separadas
    data_do_evento: date # A data em que o evento ocorre
    tipos_evento: List[TipoEventoBase]
    transporte: Optional[TransporteBase] = None
    
# Schema de Leitura de Evento (o que o backend devolve)
class Evento(BaseModel):
    id_evento: int
    nome: str
    local: Optional[str] = None
    duracao: Optional[time] = None
    hora_inicio: Optional[time] = None
    local_de_saida: Optional[str] = None

    class Config:
        from_attributes = True