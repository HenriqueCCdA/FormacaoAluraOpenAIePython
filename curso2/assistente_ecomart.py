from openai import OpenAI
from dotenv import load_dotenv
import os
from helpers import carrega
from selecionar_persona import personas

load_dotenv()


cliente = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
modelo = "gpt-4"
contexto = carrega("dados/ecomart.txt")


assistente = cliente.beta.assistants.create(
    name="Atendente EcoMart",
    instructions=f"""
    Você é um chatbot de atendimento a clientes de um e-commerce.
    Você não deve responder perguntas que nãao sejam dados do ecommerce informado!
    Além disso, adote a persona abiaxo para responder ao cliente.

    ## Contexto
    {contexto}

    ## Persona
    {personas["neutro"]}
    """,
    model=modelo,
)

print(assistente.id)
