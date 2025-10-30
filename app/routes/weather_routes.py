

from fastapi import APIRouter, HTTPException
from ..services import weather_services
from datetime import datetime, date, time # <-- 1. Importe o necessário

router = APIRouter(
    prefix="/weather",
    tags=["Weather"],
)

@router.get("/forecast", summary="Obtém a previsão do tempo para um evento específico")
def get_weather_forecast(
    destination: str, 
    event_date_str: str, # <-- 2. Peça a data como string (ex: "2025-10-30")
    event_time_str: str  # <-- 3. Peça a hora como string (ex: "14:30")
):
    """
    Obtém a previsão do tempo filtrada para a data e hora de um evento.
    
    - **destination**: O nome do local (ex: "Guaíba, RS")
    - **event_date_str**: A data do evento no formato AAAA-MM-DD
    - **event_time_str**: A hora do evento no formato HH:MM
    """
    
    # 4. Tente converter as strings em objetos date e time
    try:
        parsed_date = datetime.strptime(event_date_str, '%Y-%m-%d').date()
        parsed_time = datetime.strptime(event_time_str, '%H:%M').time()
    except ValueError:
        # Se o formato estiver errado, retorne um erro claro para o frontend
        raise HTTPException(
            status_code=400, 
            detail="Formato de data ou hora inválido. Use AAAA-MM-DD e HH:MM"
        )

    # 5. Chame o serviço com TODOS os argumentos necessários
    return weather_services.get_weather_forecast_for_event(
        destination=destination,
        event_date=parsed_date,
        event_time=parsed_time
    )