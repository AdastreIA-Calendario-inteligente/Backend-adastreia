from . import weather_services
from . import maps_services

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
def get_rota_e_clima(origin: str, destination: str, mode: str):
    """
    Função de serviço que orquestra duas chamadas:
    1. Calcula a rota com o serviço de mapas.
    2. Pega o destino formatado e busca a previsão do tempo com o serviço de clima.
    3. Retorna uma resposta combinada.
    """
    # A função original já lida com os erros.
    route_data = maps_services.calculate_google_maps_route(origin, destination, mode)
    
    # Extrair o destino preciso retornado pelo Google
    precise_destination = route_data["destination"]
    
    # A função de clima também já lida com seus próprios erros.
    weather_data = weather_services.get_weather_forecast_for_destination(precise_destination)
    
    # Combinar os dois resultados em um único objeto
    return {
        "route_details": route_data,
        "weather_forecast": weather_data
    }

