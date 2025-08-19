import os
from google.adk.agents import Agent
from dotenv import load_dotenv
from google.adk.models.lite_llm import LiteLlm # Conversor para aceitar Openai

_ = load_dotenv()

LLM = os.environ.get("LLM", "gpt-4o-mini")


# Agente único(Raíz)
root_agent = Agent(
    name="chef",
    model=LiteLlm(model=LLM),
    description="Você é uma chefe de cozinha nordestina",
    instruction="""
        Você é experiente chefe de cozinha nordestina. 
        É simpática e se chamada Lisa. 
        Responde somente sobre comida e receitas nordestinas.
        Responde sempre de forma educada e solicita.
    """
)
