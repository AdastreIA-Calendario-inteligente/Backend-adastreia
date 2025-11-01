from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..services import maw_services
from datetime import date, time,datetime


router = APIRouter(
    prefix="/mapas e clima",
    tags=["funções de local e clima juntos"],
)

# O Schema Pydantic para contat
class RouteRequest(BaseModel):
    origin: str
    destination: str
    mode: str = "driving" # é um exemplo, mas ainda não sei como podemos identificar do usuario o meio de transporte


@router.post("/rota_com_clima", summary="Calcula rota e obtém previsão do tempo para o destino")
def get_route_and_weather_info(
    origin: str,
    destination: str, 
    mode: str,
    event_date_str: str, # <-- Peça a data
    event_time_str: str  # <-- Peça a hora
):
    """
    Calcula a rota E obtém a previsão do tempo filtrada para
    o local de destino, na data e hora do evento.
    
    - **destination**: O nome do local (ex: "Guaíba, RS")
    - **event_date_str**: A data do evento no formato AAAA-MM-DD
    - **event_time_str**: A hora do evento no formato HH:MM
    """
    
    # Converta as strings em objetos date e time
    try:
        parsed_date = datetime.strptime(event_date_str, '%Y-%m-%d').date()
        parsed_time = datetime.strptime(event_time_str, '%H:%M').time()
    except ValueError:
        raise HTTPException(
            status_code=400, 
            detail="Formato de data ou hora inválido. Use AAAA-MM-DD e HH:MM"
        )

    # Chame o serviço de orquestração com TODOS os 5 argumentos
    return maw_services.get_rota_e_clima(
        origin=origin,
        destination=destination,
        mode=mode,
        event_date=parsed_date,
        event_time=parsed_time
    )