from fastapi import APIRouter
from pydantic import BaseModel
from ..services import maps_services

# Define o roteador para as rotas relacionadas a Maps e rotas de destino
router = APIRouter(
    prefix="/maps",
    tags=["Maps e rotas de destino"],
)

# O Schema Pydantic para contat
class RouteRequest(BaseModel):
    origin: str
    destination: str
    mode: str = "driving" # é um exemplo, mas ainda não sei como podemos identificar do usuario o meio de transporte

# Rota POST para calcular rota e tempo de viagem
@router.post("/calculate-route", summary="Calcula rota e tempo de viagem")
def get_route_info(request: RouteRequest):
    """
    Recebe uma origem, destino e modo de transporte, e retorna
    informações detalhadas da rota.
    
    Esta rota agora age como um intermediário, validando a requisição e
    chamando a camada de serviço para fazer o trabalho pesado.
    """
    # Chama a função do serviço, passando os dados validados
    route_data = maps_services.calculate_google_maps_route(
        origin=request.origin,
        destination=request.destination,
        mode=request.mode
    )
    
    # Simplesmente retorna o resultado que o serviço preparou
    return route_data

