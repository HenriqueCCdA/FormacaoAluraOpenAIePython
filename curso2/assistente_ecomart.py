from openai import OpenAI
from dotenv import load_dotenv
import os
import json
from helpers import carrega
from selecionar_persona import personas
from tools_ecomart import minha_tools

load_dotenv()


cliente = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
modelo = "gpt-4-1106-preview"
contexto = carrega("dados/ecomart.txt")


def criar_lista_ids():
    lista_ids_arquivos = []
    file_dados = cliente.files.create(
        file=open("dados/dados_ecomart.txt", "rb"),
        purpose="assistants"
    )
    lista_ids_arquivos.append(file_dados.id)

    file_politicas = cliente.files.create(
        file=open("dados/politicas_ecomart.txt", "rb"),
        purpose="assistants",
    )
    lista_ids_arquivos.append(file_politicas.id)

    file_produtos = cliente.files.create(
        file=open("dados/produtos_ecomart.txt", "rb"),
        purpose="assistants",
    )
    lista_ids_arquivos.append(file_produtos.id)

    return lista_ids_arquivos

def pegar_json():
    filename = "assistentes.json"

    if not os.path.exists(filename):
        vector_store = create_vector_store()
        thread_id = criar_thread(vector_store)
        assistant_id = criar_assistente(vector_store)
        data = {
            "assistant_id": assistant_id.id,
            "thread_id": thread_id.id,
            "vector_store_id": vector_store.id,
        }

        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        print("Arquivo 'aassistentes.json' criado com sucesso.")

    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print("Arquivo 'assistentes.json' não encontrado.")


def criar_thread(vector_store):
    return cliente.beta.threads.create(
        tool_resources={
            'file_search': {
                'vector_store_ids': [vector_store.id]
            }
        }
    )

def create_vector_store():
    vector_store = cliente.vector_stores.create(name='Ecomart Vector Store')

    file_paths = [
        'dados/ecomart.txt',
        'dados/politicas_ecomart.txt',
        'dados/produtos_ecomart.txt'
    ]
    file_streams = [open(path, 'rb') for path in file_paths]

    cliente.vector_stores.file_batches.upload_and_poll(
        vector_store_id=vector_store.id,
        files=file_streams
    )

    return vector_store


def criar_assistente(vector_store):
    assistente = cliente.beta.assistants.create(
        name="Atendente EcoMart",
        instructions=f"""
        Você é um chatbot de atendimento a clientes de um e-commerce.
        Você não deve responder perguntas que não sejam dados do ecommerce informado!
        Além disso, acesse os arquvos associados a você e a thrad para responder as perguntas.
        """,
        model=modelo,
        tools=minha_tools,
        tool_resources={
            'file_search': {
                'vector_store_ids': [vector_store.id]
            }
        }
    )

    return assistente
