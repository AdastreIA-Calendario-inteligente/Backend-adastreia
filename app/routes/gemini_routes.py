

from fastapi import APIRouter, HTTPException
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

@router.post("/chat-interno/{data}", summary="Gera um resumo do dia com base nos eventos")
def get_chat_interno_resumo_diario(data: str):
    try:
        summary = gemini_services.relatorio_diario(event_date_str=data)
        return {"response": summary}
    except HTTPException as e:
        # Repassa exceções HTTP (como o 400 de data inválida)
        raise e
    except Exception as e:
        # Captura qualquer outro erro inesperado
        print(f"Erro inesperado na rota /chat-interno: {e}")
        raise HTTPException(status_code=500, detail="Ocorreu um erro interno.")
    
    