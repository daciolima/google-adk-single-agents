import io
import os
import pandas as pd
from google.adk.runners import Runner
from google.adk.artifacts import InMemoryArtifactService # Or GcsArtifactService
from google.adk.agents import LlmAgent
from google.adk.sessions import InMemorySessionService
from google.genai import types
from google.adk.agents.callback_context import CallbackContext # Or ToolContext
from google.adk.sessions import InMemorySessionService, Session
from dotenv import load_dotenv

import uuid

session_id = uuid.uuid4()
user_id = uuid.uuid4()


_ = load_dotenv()

LLM = os.environ.get("LLM", "gpt-4o-mini")


artifact_service = InMemoryArtifactService()


session_id = uuid.uuid4()
user_id = uuid.uuid4()
print(session_id)
print(user_id)
session_instancia = InMemorySessionService()
session_instancia.create_session(
    app_name="analisadorCSV",
    user_id=user_id,
    session_id=session_id
)


root_agent = LlmAgent(
    name="search_csv", 
    model= "gemini-2.0-flash",
    description="Analisar somente arquivos com extensão .csv, lendo o conteúdo e resumindo as informações.",
    instruction="""
        Você deve realizar análise somente de arquivos csv enviado pelo solicitante.
        Descreva de que se trata o conteudo e pergunte o que quer saber sobre o conteudo.
        Seja sempre educado e solicito.Caso seja perguntado qualquer coisa fora do contexto do conteúdo do arquivo informe que não tem permissão para responder.
    """
)


runner = Runner(
    agent=root_agent,
    app_name="analisadorCSV",
    session_service=session_instancia,
    artifact_service=artifact_service.load_artifact(app_name="analisadorCSV", user_id=user_id, session_id=session_id, filename="livro_receitas_da_roca_caderno.pdf")
)

