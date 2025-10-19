# app/routes/gemini_routes.py

from fastapi import APIRouter
from pydantic import BaseModel
from ..services import gemini_services

router = APIRouter(
    prefix="/ai",
    tags=["AI - Gemini"], # Nova tag para a documentação
)

# Schema Pydantic para validar a requisição de entrada
class GeminiRequest(BaseModel):
    prompt: str

@router.post("/chat", summary="Envia um prompt para a IA Gemini")
def chat_with_gemini(request: GeminiRequest):
    """
    Endpoint de chat para interagir com o AdasteIA.
    
    Envie um JSON com um campo "prompt" e receba a resposta da IA.
    """
    # Chama o serviço com o prompt do usuário
    response_text = gemini_services.generate_gemini_response(request.prompt)
    
    # Retorna a resposta da IA em um JSON
    return {"response": response_text}