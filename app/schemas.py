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

# schemas novos 
class Token(BaseModel):
    """Schema para a resposta do token de login."""
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """Schema para os dados dentro do token JWT."""
    email: Optional[str] = None

#  Schemas de Resposta Aninhados (Para o endpoint de recerregar dados dos usuarios)
# Estes são os schemas que "mostram tudo".

class TransporteEventoResponse(BaseModel):
    id_transporte: int
    meio: str
    ida: Optional[str] = None
    volta: Optional[str] = None
    class Config: from_attributes = True

class DataEventoResponse(BaseModel):
    id_data: int
    data: date
    class Config: from_attributes = True
    
class TipoEventoResponse(BaseModel):
    id_tipo: int
    tipo: str
    class Config: from_attributes = True

class EventoResponseCompleto(Evento):
    """
    Herda do seu schema 'Evento' e adiciona as listas de 
    dados aninhados (transportes, datas, tipos).
    """
    transportes: List[TransporteEventoResponse] = []
    datas: List[DataEventoResponse] = []
    tipos: List[TipoEventoResponse] = []
    
    class Config:
        from_attributes = True

class CalendarioResponse(BaseModel):
    """Schema para mostrar um Calendário com seus eventos."""
    id_calendario: int
    eventos: List[EventoResponseCompleto] = []
    
    class Config:
        from_attributes = True

class UsuarioResponseCompleto(Usuario):
    """
    Herda do seu schema 'Usuario' e adiciona a lista 
    de calendários aninhados.
    Este é o schema de resposta para o endpoint
    """
    calendarios: List[CalendarioResponse] = []
    
    class Config:
        from_attributes = True