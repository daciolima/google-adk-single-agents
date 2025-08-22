import os
from google.adk.agents import Agent, LlmAgent
from dotenv import load_dotenv
# from google.adk.models.lite_llm import LiteLlm # Conversor para aceitar Openai
from langchain_community.tools.yahoo_finance_news import YahooFinanceNewsTool
import yfinance as yf
from google.adk.tools.crewai_tool import CrewaiTool
from langchain_community.tools import DuckDuckGoSearchResults
from google.adk.tools.langchain_tool import LangchainTool  
# from google.adk.tools import agent_tool
# from google.adk.tools import google_search
from crewai_tools import ScrapeWebsiteTool  # BraveSearchTool 


_ = load_dotenv()

LLM = os.environ.get("LLM", "gpt-4o-mini")

duck_search = DuckDuckGoSearchResults()
adk_duck_search = LangchainTool(tool=duck_search)

yfinance = YahooFinanceNewsTool()
adk_yfinance = LangchainTool(tool=yfinance)

# search_tool = CrewaiTool("web_search", "Search the web", BraveSearchTool())
# Brave requer configuracao BRAVE_API_KEY 


scrape_tool = CrewaiTool(ScrapeWebsiteTool(website_url="https://g1.globo.com/ultimas-noticias/"), name="scraper", description="Scrape a URL")


AgentDuckSearch = Agent(
    model="gemini-2.0-flash", #'gemini-2.0-flash-exp',
    name='AgentDuckSearch',
    instruction="""
        Pesquisar com a ferramenta adk_duck_search somente sobre conteúdo relacionado a inteligencia artificial, Agentic Development Kit - Google ADK, ações financeiras e mercado financeiro.
        Use a ferramenta adk_duck_search para pesquisar sobre o conteudo solicitado na internet.
    """,
    tools=[adk_duck_search]
)

# AgentGoogleSearch = Agent(
#     model="gemini-2.0-flash", #'gemini-2.0-flash-exp',
#     name='AgentGoogleSearch',
#     description="Você é um pesquisador de conteúdo na internet",
#     instruction="""
#         Use a ferramenta google_search para pesquisar sobre o conteudo solicitado na internet.
#     """,
#     tools=[google_search]
# )


# Create Scraper Agent
AgentScraper = Agent(
    name="AgentScraper",
    model="gemini-2.0-flash",
    description="Você extrai conteúdo de páginas da internet",
    instruction="Extrair texto de uma URL solicitada.",
    tools=[scrape_tool]
)


# tool single
def get_price(tkr: str):
    """Returns the latest close price for a stock ticker."""
    
    # Adiciona o sufixo .SA se o ticker não o tiver e for uma ação brasileira.
    # Esta é uma verificação simples; para uso em produção, considere uma lista de sufixos.
    if "." not in tkr and len(tkr) == 5: # Ex: BBAS3, PETR4
        tkr_sufixo = f"{tkr}.SA"
    else:
        tkr_sufixo = tkr

    print(f"Buscando dados para o ticker: {tkr_sufixo}")
    
    try:
        data = yf.Ticker(tkr_sufixo).history(period="1d")
        
        if not data.empty:
            latest_price = float(data['Close'].iloc[-1])
            print(f"Preço encontrado: {latest_price}")
            return latest_price
        else:
            print(f"Erro: Nenhum dado de preço encontrado para o ticker {tkr_sufixo}.")
            return None
            
    except Exception as e:
        print(f"Ocorreu um erro ao buscar dados para {tkr_sufixo}: {e}")
        return None



AgentGetPriceDay = Agent(
    name="AgentGetPriceDay",
    model="gemini-2.0-flash",
    description="Você retorna o preço da última cotação de um ticker de uma ação",
    instruction="Retornar um último preço de acão de um ticket.",
    tools=[get_price]
)


AgentYahooFinance = Agent(
    model="gemini-2.0-flash", #'gemini-2.0-flash-exp',
    name='AgentYahooFinance',
    description="Você é um especialista em mercado financeiro",
    instruction="""
        Return recent finance headlines from Yahoo Finance.
    """,
    tools=[adk_yfinance]
)


# Agente único(Raíz)
root_agent = LlmAgent(
    name="search_web", # nome do agente deve ser igual ao da pasta
    model="gemini-2.0-flash", # LiteLlm(model=LLM),
    description="Você é orquestrador. Gerencie encaminhando as consultas para o agente apropriado.",
    sub_agents=[AgentDuckSearch, AgentScraper, AgentYahooFinance],
    # tools=[
    #     agent_tool.AgentTool(agent=AgentYahooFinance),
    #     agent_tool.AgentTool(agent=AgentDuckSearch),
    #     agent_tool.AgentTool(agent=AgentGetPriceDay)
    # ],
    instruction="""
        Seja sempre educado e solicito.
        Use a ferramenta AgentDuckSearch para pesquisa de conteúdo na internet.
        Use a ferramenta AgentScraper para extrair conteudo de páginas na internet.
        User a ferramenta AgentGetPriceDay para obter cotação de um ticker de ação financeira de uma empresa.
        User a ferramenta AgentYahooFinance para obter headlines da Yahoo Finance.
    """
)
