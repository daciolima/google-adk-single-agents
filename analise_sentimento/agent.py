import os
from datetime import datetime
from google.adk.agents import Agent
from dotenv import load_dotenv
from google.adk.models.lite_llm import LiteLlm # Conversor para aceitar Openai

from .tools import get_sentimento

_ = load_dotenv()

LLM = os.environ.get("LLM", "gpt-4o-mini")



# Agente único(Raíz)
root_agent = Agent(
    name="analise_sentimento", # nome do agente deve ser igual ao da pasta
    model=LiteLlm(model=LLM),
    description="Você é uma agente que retorna o sentimento de um texto",
    instruction=f"""
        Data e Hora atual {datetime.now()}
        Você é uma analista de sentimento de textos. 
        Seja educado e solicito e, em caso de ser cumprimentado, responda com educação ao cumprimento.
        Você deve analisar apenas sentimentos onde será usada a ferramenta get_sentimento.
        Caso for perguntado com outro assunto que não seja sobre análise de texto informe que não tem permissão para responder.
        
        Use a ferramenta get_sentimento passando o conteudo para o parâmetro topic para analizar o sentimento do(s) texto(s).
        Após obter a análise do sentimento retorno para o solicitante usando o português brasileiro.
    """,
    tools=[get_sentimento]
)
