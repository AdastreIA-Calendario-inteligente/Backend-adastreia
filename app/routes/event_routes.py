from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas 
from app import crud 
from app.database import get_db
from app.security import get_current_user
from app import models
from app.services import maps_services, weather_services

router = APIRouter(prefix="/eventos", tags=["Eventos"])

# Rota POST para CRIAR um novo evento
@router.post("/", response_model=schemas.Evento, status_code=201)
def criar_evento(
    evento: schemas.EventoCreate, 
    db: Session = Depends(get_db),
    # Adiciona a dependência JWT
    usuario_logado: models.Usuario = Depends(get_current_user) 
):
    """
    Cria um novo evento no calendário, verificando a autorização do usuário logado.
    """
    # 1. Busca o calendário vinculado ao usuário logado
    calendario_usuario = db.query(models.Calendario).filter(
        models.Calendario.usuario_email == usuario_logado.email
    ).first()
    
    if not calendario_usuario:
        # Se o usuário logado não tiver um calendário (algo que deve ser criado no cadastro)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Nenhum calendário associado ao usuário."
        )

    # 2. VERIFICAÇÃO DE AUTORIZAÇÃO: Confirma se o id_calendario do payload corresponde ao id do usuário
    if evento.id_calendario != calendario_usuario.id_calendario:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Você só pode criar eventos no seu próprio calendário."
        )
         
    try:
        db_evento = crud.create_event(db=db, event=evento)
        return db_evento
    except Exception as e:
        print(f"Erro ao criar evento na rota: {e}")
        raise HTTPException(status_code=500, detail="Erro interno ao criar o evento.")

# Rota GET para BUSCAR um evento pelo ID (Também Protegida)
@router.get("/{id_evento}", response_model=schemas.Evento)
def buscar_evento(
    id_evento: int, 
    db: Session = Depends(get_db),
    usuario_logado: models.Usuario = Depends(get_current_user) # Adiciona proteção
):
    """
    Busca os detalhes de um evento específico, garantindo que pertença ao usuário logado.
    """
    db_evento = crud.get_event_by_id(db, event_id=id_evento)
    
    if db_evento is None:
        raise HTTPException(status_code=404, detail="Evento não encontrado.")
        
    # VERIFICAÇÃO DE AUTORIZAÇÃO: Confirma se o evento pertence ao calendário do usuário
    # Busca o calendário do usuário
    calendario_usuario = db.query(models.Calendario).filter(
        models.Calendario.usuario_email == usuario_logado.email
    ).first()
    
    # Checa se o evento buscado está no calendário do usuário logado
    if not calendario_usuario or db_evento.id_calendario != calendario_usuario.id_calendario:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Você não tem acesso a este evento."
        )
        
    evento_response = schemas.Evento.model_validate(db_evento)
    
    # 1. Integração de Maps (Chamada corrigida e adicionando a variável 'mode')
    if db_evento.local_de_saida and db_evento.local:
        try:

            transporte_evento = db_evento.transportes[0] if db_evento.transportes else None
            
            mode = 'driving' 
            
            route_data = maps_services.calculate_google_maps_route(
                origin=db_evento.local_de_saida, 
                destination=db_evento.local, 
                mode=mode # Novo parâmetro exigido pelo seu serviço
            )
            evento_response.maps_info = route_data
        except Exception as e:
            print(f"Erro ao obter dados de rota: {e}")
            evento_response.maps_info = {"erro": "Não foi possível obter dados de rota."}

    # 2. Integração de Tempo/Clima (Chamada corrigida)
    # A função de clima precisa de 'destination' (local) e 'date' (data do evento).
    event_date = db_evento.datas[0].data if db_evento.datas else None
    event_time = db_evento.hora_inicio or time(12, 0) # Usa a hora de início ou 12:00 como padrão

    if db_evento.local and event_date:
        try:
            # Chamada corrigida para a nova função de serviço
            weather_data = weather_services.get_weather_forecast_for_event(
                destination=db_evento.local,
                event_date=event_date,
                event_time=event_time
            )
            
            evento_response.tempo_info = weather_data
        except Exception as e:
            print(f"Erro ao obter dados de clima: {e}")
            evento_response.tempo_info = {"erro": "Não foi possível obter a previsão do tempo."}

    return evento_response