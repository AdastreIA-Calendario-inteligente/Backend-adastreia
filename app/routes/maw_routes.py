from fastapi import APIRouter
from pydantic import BaseModel
from ..services import maw_services

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
def get_rota_com_clima_info(request: RouteRequest):
    """
    Obtém informações detalhadas da rota e, ao mesmo tempo, busca
    a previsão do tempo para o local de destino.
    
    Esta é uma rota de orquestração que combina múltiplos serviços do backend.
    """
    # A rota simplesmente chama a nova função de orquestração do serviço
    return maw_services.get_rota_e_clima(
        origin=request.origin,
        destination=request.destination,
        mode=request.mode
    )