from datetime import date, time, datetime,timedelta
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

# Função de serviço que obtém a previsão do tempo para um evento específico
def get_weather_forecast_for_event(
    destination: str, 
    event_date: date, 
    event_time: time
):
    """
    Função de serviço que obtém a previsão do tempo para um destino
    e filtra os dados para a data e hora do evento.
    """
    # Geocodificação (pegar os destination e transformar em coordenadas)
    try:
        geocode_result = gmaps_client.geocode(destination)
        if not geocode_result:
            raise HTTPException(status_code=404, detail="Não foi possível encontrar as coordenadas para o destino fornecido.")
        
        location = geocode_result[0]['geometry']['location']
        lat, lon = location['lat'], location['lng']
    # Manejo de erros simples
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro durante a geocodificação: {e}")

    # Obter Previsão do Tempo
    try:
        params = {
            'lat': lat, # latitude 
            'lon': lon, # Longitude
            'appid': OPENWEATHER_API_KEY,
            'units': 'metric',# Para obter temperatura em Celsius
            'lang': 'pt_br' # Para obter descrições em Português
        }

        response = requests.get(WEATHER_API_URL, params=params)
        response.raise_for_status()
        weather_data = response.json()

        #  Combina data e hora para o momento exato do evento
        target_datetime_local = datetime.combine(event_date, event_time)

        # converte a hora local para UTC 
        target_datetime_utc = target_datetime_local + timedelta(hours=3)
        
        melhor_previsao = None

        menor_diferenca = timedelta(days=5) # Inicializa com um valor alto para comparação

        #Itera sobre todas as previsões disponíveis (até 5 dias)
        for forecast in weather_data.get('list', []):
            # Converte a string de data/hora da API para objeto datetime
            forecast_dt_utc = datetime.strptime(forecast['dt_txt'], '%Y-%m-%d %H:%M:%S')
            
                
            # Calcula a diferença absoluta de tempo entre a previsão e a hora do evento
            diferenca = abs(forecast_dt_utc - target_datetime_utc)
            
            # Encontra a previsão mais próxima da hora de início
            if diferenca < menor_diferenca:
                menor_diferenca = diferenca
                melhor_previsao = forecast
        # Se nenhuma previsão foi encontrada
        if not melhor_previsao:
             return {"city": weather_data['city']['name'], "forecast": "Nenhuma previsão disponível para a data do evento."}


        #  Retorna apenas a previsão mais relevante
        return {
            "city": weather_data['city']['name'],
            "country": weather_data['city']['country'],
            "forecast": {
                "datetime": melhor_previsao['dt_txt'],
                "temperature_celsius": melhor_previsao['main']['temp'],
                "feels_like_celsius": melhor_previsao['main']['feels_like'],
                "condition": melhor_previsao['weather'][0]['description'],
                "icon_url": f"https://openweathermap.org/img/wn/{melhor_previsao['weather'][0]['icon']}@2x.png"
            }
        }

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Erro ao contatar a API de previsão do tempo: {e}")