from datetime import datetime, date, time
from typing import Optional, List
from pydantic import BaseModel

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

# Base para o Tipo de Evento
class TipoEventoBase(BaseModel):
    tipo: str
    class Config:
        from_attributes = True

# Schema de criação de Evento (o que o usuário envia)
class EventoCreate(BaseModel):
    id_calendario: int 
    nome: str
    local: Optional[str] = None
    duracao: Optional[str] = None
    hora_inicio: Optional[str] = None
    hora_fim: Optional[str] = None
    temperatura: Optional[float] = None
    clima: Optional[str] = None
    local_de_saida: Optional[str] = None
    transporte: Optional[str] = None
    distancia: Optional[str] = None
    
    # Detalhes que são criados em tabelas separadas
    data_do_evento: date # A data em que o evento ocorre
    tipos_evento: List[TipoEventoBase]
    
# Schema de Leitura de Evento (o que o backend devolve)
class DataEvento(BaseModel):
    id_data: int
    data: date
    class Config:
        from_attributes = True
class Evento(BaseModel):
    id_evento: int
    nome: str
    local: Optional[str] = None
    duracao: Optional[str] = None
    hora_inicio: Optional[str] = None
    local_de_saida: Optional[str] = None
    hora_fim: Optional[str] = None
    temperatura: Optional[float] = None
    clima: Optional[str] = None
    transporte: Optional[str] = None
    distancia: Optional[str] = None
    data_do_evento: date = None

    maps_info: Optional[dict] = None  # Para armazenar informações de mapas/clima
    tempo_info: Optional[dict] = None  # Para armazenar informações de clima/tempo
    
    #Relacionamentos
    tipos: List[TipoEventoBase] = None
    datas: List[DataEvento]
    class Config:
        from_attributes = True

#Atualiza a referência para o novo Schema DataEvento
Evento.model_rebuild()