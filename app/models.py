
from sqlalchemy import Column, Integer, String, Text, Time, Date, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base  # Importa a Base do seu database.py

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
    eventos = relationship("Evento", back_populates="calendario")

# provavelmenete a parte mais importante
class Evento(Base):
    __tablename__ = "evento"

    id_evento = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    local = Column(String)
    duracao = Column(Time)
    hora_inicio = Column(Time)
    local_de_saida = Column(String)
    
    # Chave estrangeira
    id_calendario = Column(Integer, ForeignKey("calendario.id_calendario"), nullable=False)

    # Relacionamentos
    calendario = relationship("Calendario", back_populates="eventos") 
    tipos = relationship("TipoEvento", back_populates="evento")         
    datas = relationship("DataEvento", back_populates="evento")         
    transportes = relationship("TransporteEvento", back_populates="evento") 

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


class TransporteEvento(Base):
    __tablename__ = "transporte_evento"

    id_transporte = Column(Integer, primary_key=True, index=True)
    meio = Column(String)
    ida = Column(String)
    volta = Column(String)
    
    # Chave estrangeira
    evento_id = Column(Integer, ForeignKey("evento.id_evento"), nullable=False)
    
    # Relacionamento
    evento = relationship("Evento", back_populates="transportes") 



