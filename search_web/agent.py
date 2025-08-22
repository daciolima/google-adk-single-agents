import os
from google.adk.agents import Agent
from dotenv import load_dotenv
from google.adk.models.lite_llm import LiteLlm # Conversor para aceitar Openai
from langchain_community.tools import DuckDuckGoSearchResults
from google.adk.tools.langchain_tool import LangchainTool  
from google.adk.tools import google_search

_ = load_dotenv()

LLM = os.environ.get("LLM", "gpt-4o-mini")

duck_search = DuckDuckGoSearchResults()
adk_duck_search = LangchainTool(tool=duck_search)

# Agente único(Raíz)
root_agent = Agent(
    name="search_web", # nome do agente deve ser igual ao da pasta
    model=LiteLlm(model=LLM),
    description="Você é um pesquisador de conteúdo na internet",
    tools=[adk_duck_search, google_search],
    instruction="""
        Você é experiente pesquisador de conteúdo na internet
        Pesquisar somente sobre conteúdo relacionado a inteligência artificial. 
        Seja sempre educado e solicito.
        Caso a pergunta esteja relacionada a outro assunto que não dentro do contexto do universo da inteligencia artificial, informar que não tem permissão. 
    """
)
