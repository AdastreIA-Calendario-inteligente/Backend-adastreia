from sqlalchemy import Column, Integer, String, Text, Time, Date, ForeignKey, Float
from sqlalchemy.orm import relationship
from .database import Base

# Tabelas Presentes no database 
class Usuario(Base):
    __tablename__ = "usuario"

    email = Column(String, primary_key=True, index=True)
    nome = Column(String)
    senha_hash = Column(Text)

    # Relacionamentos 
    chats = relationship("ChatIA", back_populates="usuario")
    calendarios = relationship("Calendario", back_populates="usuario")

class ChatIA(Base):
    __tablename__ = "chatia"

    id_chat = Column(Integer, primary_key=True, index=True)
    pergunta = Column(String)
    resposta = Column(String)
    
    # Chave estrangeira 
    usuario_email = Column(String, ForeignKey("usuario.email"), nullable=False)

    # Relacionamento 
    usuario = relationship("Usuario", back_populates="chats")

class Calendario(Base):
    __tablename__ = "calendario"

    id_calendario = Column(Integer, primary_key=True, index=True)
    
    # Chave estrangeira
    usuario_email = Column(String, ForeignKey("usuario.email"), nullable=False) # não pode ficar vazio

    # Relacionamentos
    usuario = relationship("Usuario", back_populates="calendarios") 
    
    # Um calendário tem muitos 'eventos'
    # O back_populates aponta para a propriedade 'calendario' no modelo Evento
    eventos = relationship("Evento", back_populates="calendario")

class Evento(Base):
    __tablename__ = "evento"

    id_evento = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    local = Column(String) #local do evento
    duracao = Column(String)
    hora_inicio = Column(String)
    local_de_saida = Column(String) #local de onde o usuario vai sair
    temperatura = Column(Float)
    clima = Column(String)
    hora_fim = Column(String)
    distancia = Column(String)
    transporte = Column(String)
    
    # Chave estrangeira
    id_calendario = Column(Integer, ForeignKey("calendario.id_calendario"), nullable=False)

    # Relacionamentos
    
    # CORRIGIDO:
    # Um evento pertence a um 'calendario' (singular)
    # O back_populates aponta para a propriedade 'eventos' (plural) no modelo Calendario
    calendario = relationship("Calendario", back_populates="eventos") 
    
    tipos = relationship("TipoEvento", back_populates="evento") 
    datas = relationship("DataEvento", back_populates="evento") 

class TipoEvento(Base):
    __tablename__ = "tipo_evento"

    id_tipo = Column(Integer, primary_key=True, index=True)
    tipo = Column(String)
    
    # Chave estrangeira
    evento_id = Column(Integer, ForeignKey("evento.id_evento"), nullable=False)
    
    # Relacionamento
    evento = relationship("Evento", back_populates="tipos")

class DataEvento(Base):
    __tablename__ = "data_evento"

    id_data = Column(Integer, primary_key=True, index=True)
    data = Column(Date)
    
    # Chave estrangeira
    evento_id = Column(Integer, ForeignKey("evento.id_evento"), nullable=False)
    
    # Relacionamento
    evento = relationship("Evento", back_populates="datas")