
from fastapi import FastAPI

from .routes import maps_routes

# Cria a instância da aplicação FastAPI
app = FastAPI(title="AdasteIA", version="0.1.0")
app.include_router(maps_routes.router)

# Define um endpoint (ou "rota") para a raiz da URL
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

