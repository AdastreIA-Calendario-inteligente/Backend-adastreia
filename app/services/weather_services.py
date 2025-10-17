
import os
import requests
from fastapi import HTTPException
from dotenv import load_dotenv
import googlemaps

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Pega a chave do ambiente que foi carregada do arquivo .env
api_key = os.getenv("routes_maps_api_key")


# Inicializa o cliente do Google Maps
gmaps_client = googlemaps.Client(key=api_key)



# Pega a chave da OpenWeather 
OPENWEATHER_API_KEY = os.getenv("weather_key")

# URL base para a API de previsão de 5 dias / 3 horas
WEATHER_API_URL = "https://api.openweathermap.org/data/2.5/forecast"

def get_weather_forecast_for_destination(destination: str):
    """
    Função de serviço que obtém a previsão do tempo para um destino.
    1. Usa o Geocoding do Google para converter o nome do local em lat/lon.
    2. Usa as coordenadas para obter a previsão do tempo da OpenWeather.
    """
    # Geocodificação (pegar os destination e transformar em coordenadas)
    try:
        geocode_result = gmaps_client.geocode(destination)
        if not geocode_result:
            raise HTTPException(status_code=404, detail="Não foi possível encontrar as coordenadas para o destino fornecido.")
        
        location = geocode_result[0]['geometry']['location']
        lat, lon = location['lat'], location['lng']

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro durante a geocodificação: {e}")

    #Obter Previsão do Tempo (A partir das coordenadas, conseguir a previsão)
    try:
        params = {
            'lat': lat,         # latitude 
            'lon': lon,         # Longitude
            'appid': OPENWEATHER_API_KEY,
            'units': 'metric',  # Para obter temperatura em Celsius
            'lang': 'pt_br'     # Para obter descrições em Português
        }
        
        response = requests.get(WEATHER_API_URL, params=params)
        response.raise_for_status()  # Levanta um erro se a requisição falhou (ex: status 4xx ou 5xx)
        
        weather_data = response.json()

        # simplificar os dados e retornar ela para o usuario
        # A API retorna muitos dados. Vamos filtrar e retornar apenas o essencial para o objetivo do usuario
        previcao_simplificada = []
        for forecast in weather_data.get('list', [])[:8]: # Pega as próximas 24h (8 previsões de 3h)
            previcao_simplificada.append({
                "datetime": forecast['dt_txt'],
                "temperature_celsius": forecast['main']['temp'],
                "feels_like_celsius": forecast['main']['feels_like'],
                "condition": forecast['weather'][0]['description'],
                "icon_url": f"https://openweathermap.org/img/wn/{forecast['weather'][0]['icon']}@2x.png"
            })

        return {
            # Aqui seria os dados mais simplificados onde podemos retornar para o usuario
            "city": weather_data['city']['name'],
            "country": weather_data['city']['country'],
            "forecasts": previcao_simplificada
        }

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Erro ao contatar a API de previsão do tempo: {e}")