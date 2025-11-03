from . import weather_services
from . import maps_services
from datetime import date, time
from fastapi import HTTPException
import os 
from dotenv import load_dotenv
import googlemaps

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Pega a chave do ambiente que foi carregada do arquivo .env
api_key = os.getenv("routes_maps_api_key")


# Inicializa o cliente do Google Maps
gmaps_client = googlemaps.Client(key=api_key)

# essa aqui seria a integração de duas APIS EM um serviço só.    
def get_rota_e_clima(
    origin: str, 
    destination: str, 
    mode: str, 
    event_date: date,     # <-- 2. Adicione o argumento de data
    event_time: time      # <-- 2. Adicione o argumento de hora
):
    """
    Função de serviço que orquestra duas chamadas:
    1. Calcula a rota com o serviço de mapas.
    2. Busca a previsão do tempo com o serviço de clima.
    3. Retorna uma resposta combinada.
    """
    
    # Etapa 1: Calcular a rota (esta parte estava correta)
    route_data = maps_services.calculate_google_maps_route(origin, destination, mode)
    
    # Etapa 2: Extrair o destino preciso
    precise_destination = route_data["destination"]
    
    # Etapa 3: Buscar a previsão do tempo
    #    (Corrigido para usar a nova função e passar todos os 3 argumentos)
    weather_data = weather_services.get_weather_forecast_for_event(
        destination=precise_destination,
        event_date=event_date,
        event_time=event_time
    )
    
    # Etapa 4: Combinar os resultados
    return {
        "route_details": route_data,
        "weather_forecast": weather_data
    }
