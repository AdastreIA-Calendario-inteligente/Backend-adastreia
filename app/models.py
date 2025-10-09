
from sqlalchemy import Column, Integer, String, DateTime
from .database import Base
import datetime

# Exemplo de uma tabela para "Eventos" do calendário
# fiz o mais generico possível e ainda não sei como a lara vai 
# fazer, só deixei aqui como exemplo.
class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, nullable=True)
    start_time = Column(DateTime, default=datetime.datetime.utcnow)
    end_time = Column(DateTime)