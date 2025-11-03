
# importação de bibliotecas necessarias
import os
import google.generativeai as genai
from fastapi import HTTPException
from datetime import datetime
from .. import crud
from ..database import SessionLocal 

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


# Função para gerar resposta do Gemini com contexto do sistema
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
    

# iremos criar um "pre-prompt" do dia a dia do usuario 
# busca eventos pela data no banco de dados -> fromata os dados -> pede ao gemini (chatbox)
def relatorio_diario(event_date_str: str):

    # 1. Validar e converter a data
    try:
        event_date = datetime.strptime(event_date_str, '%Y-%m-%d').date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato de data inválido. Por favor, use AAAA-MM-DD.")
    
    db = SessionLocal() # Cria uma sessão de banco de dados
    try:
        eventos_do_dia = crud.get_events_by_date(db, event_date=event_date)
        
        if not eventos_do_dia:
            # Resposta amigável se não houver eventos
            return f"Você não tem nenhum evento agendado para o dia {event_date.strftime('%d/%m/%Y')}."
        # formata dados para o prompt 
        ListInfos = []

        # 4. Formatar os dados dos eventos
        for evento in eventos_do_dia:
            info = f"- Compromisso: {evento.nome}\n"
            if evento.local:
                info += f"  Local: {evento.local}\n"
            if evento.hora_inicio:
                info += f"  Hora: {evento.hora_inicio.strftime('%H:%M')}\n"
            if evento.local_de_saida:
                info += f"  Local de Saída: {evento.local_de_saida}\n"
            ListInfos.append(info)
        # cria a string final
        info_string = "\n".join(ListInfos)
        
        # 5. Criar o pre-prompt para o Gemini
        prePrompt= (
            f"Meu assistente, AdasteIA. Por favor, escreva um relatório curto e amigável "
            f"sobre meus compromissos para o dia {event_date.strftime('%d/%m/%Y')}. "
            f"Organize o dia para mim com base nestas informações:\n\n"
            f"{info_string}\n\n"
            f"Seja prestativa e termine com uma nota positiva."
        )

        # 5. Chamar a API do Gemini
        response = model.generate_content(prePrompt) 
        return response.text
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar o relatório: {e}")
    
    finally:
        # finaliza a sessão do banco
        db.close()

    


