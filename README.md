# AdasteIA - Gerenciador de Rotina Inteligente

## Descrição do Projeto

AdasteIA é um projeto de sistema distribuído que funciona como um calendário inteligente. A aplicação web permite que usuários gerenciem seus eventos e tarefas diárias, recebendo sugestões otimizadas com base em dados de APIs externas, como previsão do tempo, condições de trânsito e recomendações de uma inteligência artificial.

Este projeto foi desenvolvido para a disciplina de Sistemas Distribuídos da FURG.

### Equipe
* João gabriel freitas acosta 
* Lara Letittja
* Karoline Vieira


---

## Como Executar o Backend

Siga os passos abaixo para configurar e rodar o ambiente de desenvolvimento do backend.

### Pré-requisitos
* [Python 3.9+](https://www.python.org/downloads/)
* [Git](https://git-scm.com/)

### 1. Clonar o Repositório

```bash
git clone https://github.com/AdastreIA-Calendario-inteligente/Backend-adastreia
cd adasteia_backend
```

### 2. Criar e Ativar o Ambiente Virtual

```bash
# Criar o ambiente
python -m venv venv

# Ativar no macOS/Linux
source venv/bin/activate

# Ativar no Windows
.\venv\Scripts\activate
```

### 3. Instalar as Dependências

```bash
pip install -r requirements.txt
```


### 4. Executar o Servidor

Após a configuração, inicie o servidor de desenvolvimento:
```bash
uvicorn app.main:app --reload
```

O servidor estará rodando em `http://127.0.0.1:8000`.

### 5. Acessando a Documentação da API

Com o servidor no ar, a documentação interativa da API (gerada automaticamente pelo FastAPI) está disponível em:
* **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* **ReDoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)