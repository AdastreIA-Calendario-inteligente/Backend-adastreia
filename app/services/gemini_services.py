
# importação de bibliotecas necessarias
import os
import google.generativeai as genai
from fastapi import HTTPException

#pegando a cheve da API 
GEMINI_API_KEY = os.getenv("gemini_key")

# configuramos a API
genai.configure(api_key=GEMINI_API_KEY)

  # Escolhe o modelo. 'gemini-2.5-flash-lite' 
model = genai.GenerativeModel('gemini-2.5-flash-lite')

#precisamos Fazer um NLU workflow do gemini pra nossa aplicação se quisermos 
# que ela faça algo mais complexo do que só falar com os usuarios, mesmo assim, 
# se não conseguirmos, ela é bastabte util só como chatbox. 

# aqui só irei fazer um exemplo 
SYSTEM_INSTRUCTION = (
    "Você é AdasteIA, uma assistente de gerenciamento de rotina e calendário. "
    "Seu nome é uma homenagem a Ada Lovelace e à deusa grega Adrasteia. "
    "Seja sempre prestativa, inteligente e concisa em suas respostas."
)


def generate_gemini_response(user_prompt: str):
    """
    Gera uma resposta do Gemini, já com o contexto do sistema AdasteIA.
    """
    try:
        # Cria o prompt completo, combinando a instrução do sistema com a pergunta do usuário
        full_prompt = f"{SYSTEM_INSTRUCTION}\n\nPergunta do Usuário: {user_prompt}"

        # Gera o conteúdo
        response = model.generate_content(full_prompt)
        
        # Retorna apenas o texto da resposta
        return response.text
    
    except Exception as e:
        # Captura qualquer erro que a API do Gemini possa retornar
        print(f"Erro ao chamar a API do Gemini: {e}")
        raise HTTPException(status_code=500, detail="Ocorreu um erro ao processar sua solicitação com a IA.")