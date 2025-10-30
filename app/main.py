from .routes import maps_routes, weather_routes, maw_routes, gemini_routes, user_routes, event_routes
from fastapi import FastAPI

#para integrar com o frontend 
from fastapi.middleware.cors import CORSMiddleware

# importando rotas
from .routes import maps_routes, weather_routes, maw_routes, gemini_routes, event_routes

# Cria a instância da aplicação FastAPI
app = FastAPI(title="AdasteIA", version="0.1.0")
app.include_router(maps_routes.router)
app.include_router(weather_routes.router)
app.include_router(maw_routes.router)
app.include_router(gemini_routes.router)
app.include_router(user_routes.router)
app.include_router(event_routes.router)
#app.include_router(event_routes.router)

# Define um endpoint (ou "rota") para a raiz da **URL
@app.get("/")
def read_root():
    """
    Endpoint raiz que retorna uma mensagem de boas-vindas.
    """
    return {"message": "Bem-vindo à API do AdasteIA!"}

# Endpoint para ver se a API está no ar 
@app.get("/health")
def health_check():
    """
    Endpoint simples para verificar se a API está no ar.
    """
    return {"status": "ok"}

#Lista de origend permitidas 
origins = [
    # Também é preciso colocar a url do frontend de dev local
    "https://adastreia.onrender.com/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials = True,
    allow_methods=["*"],
    allow_headers=["*"],

)