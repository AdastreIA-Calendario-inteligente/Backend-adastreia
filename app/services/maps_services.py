
import googlemaps
import os
from dotenv import load_dotenv
from datetime import datetime
from fastapi import HTTPException # Usamos para passar erros para a camada de rota
from . import weather_services

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Pega a chave do ambiente que foi carregada do arquivo .env
api_key = os.getenv("routes_maps_api_key")


# Inicializa o cliente do Google Maps
gmaps_client = googlemaps.Client(key=api_key)

def calculate_google_maps_route(origin: str, destination: str, mode: str):
    """
    Função de serviço que calcula uma rota usando a API do Google Maps.
    Recebe strings simples e retorna um dicionário com os dados da rota.
    """
    try:
        now = datetime.now()
        
        # Faz a chamada para a API do Google Directions
        directions_result = gmaps_client.directions(
            origin,
            destination,
            mode=mode,
            departure_time=now,
            language="pt-BR"
        )

        if not directions_result:
            # Se a API do Google não retornar resultados, levanta um erro HTTP
            raise HTTPException(status_code=404, detail="Não foi possível encontrar uma rota.")

        leg = directions_result[0]['legs'][0]
        
        # Monta e retorna o dicionário com os dados limpos
        return {
            "origin": leg['start_address'],
            "destination": leg['end_address'],
            "distance": leg['distance']['text'],
            "duration": leg['duration']['text'],
            "duration_in_traffic": leg.get('duration_in_traffic', {}).get('text'),
            "summary_route": directions_result[0]['summary'],
        }

    except googlemaps.exceptions.ApiError as e:
        # Erro específico da API do Google
        raise HTTPException(status_code=500, detail=f"Erro na API do Google Maps: {e}")
    except Exception as e:
        # Outros erros inesperados
        raise HTTPException(status_code=500, detail=f"Ocorreu um erro inesperado no serviço de mapas: {e}")
    
