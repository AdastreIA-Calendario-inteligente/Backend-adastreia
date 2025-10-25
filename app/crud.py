
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import SQLAlchemyError
from datetime import date
from . import models, schemas


# função que pega todos os eventos de um usuario em uma data especifica

def get_events_by_date(db: Session, event_date: date) -> list[models.Evento]:
    """
    Busca no banco todos os Eventos associados a uma data específica.
    
    Esta função consulta a tabela 'DataEvento' e carrega
    os detalhes do 'Evento' principal relacionado a cada entrada.
    """

    try:
        # 1. Encontra as entradas em DataEvento que correspondem à data
        # 2. Usa 'options(joinedload(models.DataEvento.evento))' para
        #    automaticamente carregar o objeto Evento relacionado.
        #    Isso é muito eficiente e evita novas consultas ao banco.
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
    
