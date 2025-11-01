
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import SQLAlchemyError
from datetime import date
from . import models, schemas, security
from typing import Optional

# função que pega todos os eventos de um usuario em uma data especifica

def get_events_by_date(db: Session, event_date: date) -> list[models.Evento]:
    """
    Busca no banco todos os Eventos associados a uma data específica.
    
    Esta função consulta a tabela 'DataEvento' e carrega
    os detalhes do 'Evento' principal relacionado a cada entrada.
    """

    try:
        # 2. Consulta a tabela DataEvento filtrando pela data fornecida
        data_eventos_encontrados = db.query(models.DataEvento) \
                .filter(models.DataEvento.data == event_date) \
                .options(joinedload(models.DataEvento.evento)) \
                .all()
        
        # 3. Extrai apenas os objetos 'Evento' da lista
        eventos_do_dia = [data_evento.evento for data_evento in data_eventos_encontrados if data_evento.evento]
        
        return eventos_do_dia
    
    except SQLAlchemyError as e:
        print(f"Erro ao buscar eventos no banco: {e}")
        return []
    
def get_event_by_id(db: Session, event_id: int):
    """
    Busca um evento específico pelo seu ID (id_evento)
    """
    # Usa .options(joinedload(...)) para carregar os relacionamentos em uma só consulta
    return db.query(models.Evento)\
        .filter(models.Evento.id_evento == event_id)\
        .options(
            joinedload(models.Evento.datas),
            joinedload(models.Evento.tipos),
            joinedload(models.Evento.transportes)
        )\
        .first()

def create_event(db: Session, event: schemas.EventoCreate) -> models.Evento:
    """
    Cria um novo Evento e todas as suas entidades relacionadas.
    """
    try:
        # 1. Cria o objeto principal Evento
        db_evento = models.Evento(
            id_calendario=event.id_calendario,
            nome=event.nome,
            local=event.local,
            duracao=event.duracao,
            hora_inicio=event.hora_inicio,
            local_de_saida=event.local_de_saida
        )
        
        db.add(db_evento)
        db.flush() # Flushes para obter o db_evento.id_evento antes do commit

        # 2. Cria a DataEvento
        db_data_evento = models.DataEvento(
            evento_id=db_evento.id_evento,
            data=event.data_do_evento
        )
        db.add(db_data_evento)

        # 3. Cria os Tipos de Evento
        for tipo_in in event.tipos_evento:
            db_tipo = models.TipoEvento(
                evento_id=db_evento.id_evento,
                tipo=tipo_in.tipo
            )
            db.add(db_tipo)

        # 4. Cria o Transporte (se existir)
        if event.transporte:
            db_transporte = models.TransporteEvento(
                evento_id=db_evento.id_evento,
                meio=event.transporte.meio,
                ida=event.transporte.ida,
                volta=event.transporte.volta
            )
            db.add(db_transporte)

        db.commit()
        db.refresh(db_evento)
        return db_evento
    
    except SQLAlchemyError as e:
        db.rollback()
        # É fundamental lidar com a exceção e relançá-la ou retornar um erro
        print(f"Erro ao criar evento: {e}")
        raise

def get_user_full_data(db: Session, email: str) -> Optional[models.Usuario]:
    """
    Busca um usuário e carrega TODOS os seus dados relacionados
    (calendários, eventos, transportes, etc.) de forma eficiente
    usando 'joinedload'.
    """
    return db.query(models.Usuario).filter(models.Usuario.email == email).options(
        joinedload(models.Usuario.calendarios)  # Carrega os calendários
            .joinedload(models.Calendario.eventos)  # Carrega os eventos
                .joinedload(models.Evento.transportes), # Carrega os transportes
        joinedload(models.Usuario.calendarios)
            .joinedload(models.Calendario.eventos)
                .joinedload(models.Evento.datas), # Carrega as datas
        joinedload(models.Usuario.calendarios)
            .joinedload(models.Calendario.eventos)
                .joinedload(models.Evento.tipos) # Carrega os tipos
    ).first()

