from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import schemas, crud, models
from starlette import status
from datetime import time
from app.database import get_db
from app.security import get_current_user
from app.services import maps_services, weather_services
from datetime import time
router = APIRouter(prefix="/eventos", tags=["Eventos"])

# Rota POST para CRIAR um novo evento
@router.post("/", response_model=schemas.Evento, status_code=201)
def criar_evento(
    # O schema 'evento' agora NÃO tem 'id_calendario'
    evento: schemas.EventoCreate, 
    db: Session = Depends(get_db),
    usuario_logado: models.Usuario = Depends(get_current_user) 
):
    """
    Cria um novo evento no calendário do usuário logado.
    O ID do calendário é obtido automaticamente através da autenticação.
    """
    
    # 1. Busca o calendário vinculado ao usuário logado
    calendario_usuario = db.query(models.Calendario).filter(
        models.Calendario.usuario_email == usuario_logado.email
    ).first()
    
    if not calendario_usuario:
        # Esta verificação AINDA É IMPORTANTE
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Nenhum calendário associado ao usuário."
        )

    # 2. REMOVEMOS A VERIFICAÇÃO DE AUTORIZAÇÃO ANTIGA
    #    if evento.id_calendario != calendario_usuario.id_calendario: ...
    #    (Isso não é mais necessário!)
         
    try:
        # 3. Chamamos o CRUD passando o ID do calendário do usuário
        db_evento = crud.create_event(
            db=db, 
            event=evento, 
            calendario_id=calendario_usuario.id_calendario
        )
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
    Busca os detalhes de um evento específico, garante a autorização, 
    chama APIs (se necessário) e salva os resultados no DB para a próxima vez.
    """
    db_evento = crud.get_event_by_id(db, event_id=id_evento)
    
    if db_evento is None:
        raise HTTPException(status_code=404, detail="Evento não encontrado.")
        
    # VERIFICAÇÃO DE AUTORIZAÇÃO (Mantida)
    calendario_usuario = db.query(models.Calendario).filter(
        models.Calendario.usuario_email == usuario_logado.email
    ).first()
    
    # Verifica se o evento pertence ao calendário do usuário logado
    if not calendario_usuario or db_evento.id_calendario != calendario_usuario.id_calendario:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Você não tem acesso a este evento."
        )
    
    needs_update = False  # Flag para saber se precisamos salvar no final
    route_data = None     # Variável para a resposta Maps
    weather_data = None   # Variável para a resposta Clima

    # 1. INTEGRAÇÃO DE MAPS: Chama a API apenas se DISTANCIA ou DURACAO estiverem vazios
    if not db_evento.distancia or not db_evento.duracao:
        if db_evento.local_de_saida and db_evento.local:
            try:
                mode = db_evento.transporte or 'driving' 
                route_data = maps_services.calculate_google_maps_route(
                    origin=db_evento.local_de_saida, 
                    destination=db_evento.local, 
                    mode=mode
                )
                
                if route_data:
                    # Salva os valores no OBJETO DB (ainda não salvo no banco)
                    db_evento.distancia = route_data.get('distance')
                    db_evento.duracao = route_data.get('duration')
                    needs_update = True # Marca para salvar no final
                    
            except Exception as e:
                print(f"Erro ao obter dados de rota: {e}")
                route_data = {"erro": "Não foi possível obter dados de rota."}

    # 2. INTEGRAÇÃO DE CLIMA: Chama a API apenas se CLIMA ou TEMPERATURA estiverem vazios
    if not db_evento.clima or db_evento.temperatura is None:
        event_date = db_evento.datas[0].data if db_evento.datas else None
        event_time = db_evento.hora_inicio or time(12, 0)

        if db_evento.local and event_date:
            try:
                weather_data_result = weather_services.get_weather_forecast_for_event(
                    destination=db_evento.local,
                    event_date=event_date,
                    event_time=event_time
                )
                
                # Se a API retornou dados válidos
                if weather_data_result and 'forecast' in weather_data_result:
                    forecast = weather_data_result['forecast']
                    # Salva os valores no OBJETO DB (ainda não salvo no banco)
                    db_evento.clima = forecast.get('condition')
                    db_evento.temperatura = float(forecast.get('temperature_celsius', 0))
                    weather_data = weather_data_result # Armazena para o objeto de resposta
                    needs_update = True # Marca para salvar no final

            #  Manejo de erros simples        
            except Exception as e:
                print(f"Erro ao obter dados de clima: {e}")
                weather_data = {"erro": "Não foi possível obter a previsão do tempo."}


    # 3. PERSISTÊNCIA: Se needs_update for True, salva as alterações no DB
    if needs_update:
        # Usa a função CRUD para comitar as alterações feitas no db_evento
        crud.update_event_api_data(
            db, 
            db_evento.id_evento, 
            db_evento.clima, 
            db_evento.temperatura, 
            db_evento.distancia, 
            db_evento.duracao
        )
        
    # 4. RESPOSTA: Converte o objeto do DB (agora atualizado) para o Schema de resposta
    evento_response = schemas.Evento.model_validate(db_evento)
    
    # Adiciona as informações de API ao SCHEMA DE RESPOSTA (se foram calculadas agora)
    # Se os dados já estavam no DB, maps_info/tempo_info serão None na resposta.
    if route_data:
        evento_response.maps_info = route_data 
    if weather_data:
        evento_response.tempo_info = weather_data

    return evento_response