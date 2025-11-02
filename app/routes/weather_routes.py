from fastapi import APIRouter
from ..services import weather_services

router = APIRouter(
    prefix="/weather",
    tags=["Weather"],
)

@router.get("/forecast", summary="Obtém a previsão do tempo para um destino")
def get_weather_forecast(destination: str):
    """
    Obtém a previsão do tempo para as próximas 24 horas para um local de destino.
    
    - **destination**: O nome do local (ex: "Praia do Cassino, Rio Grande, RS").
    """
    return weather_services.get_weather_forecast_for_destination(destination)