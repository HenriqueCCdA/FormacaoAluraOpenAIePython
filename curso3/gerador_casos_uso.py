from openai import OpenAI
from dotenv import load_dotenv
import os
from tools import MODELO_GPT_4, STATUS_COMPLETED, STATUS_FAILED

load_dotenv()

cliente = OpenAI(api_key=os.getenv("OPANAI_API_KEY"))

def gerar_caso_uso(prompt, assistente, thread, modelo=MODELO_GPT_4):
    pergunta = f"""Gere um caso de uso para: {prompt}.
    Para isso, busque nos arquivos associados a você o conteúdo # Exemplos de Caso de Uso
    (no arquivo exemplos_casos_uso.txt)

    Adote o formato de saída abaixo.

    # Formato de Saída

    *Nome da Persona*, em *contexto do app*, precisa realizar *tarefa no app* no aplicativo.
    Logo, *Benefício Esperado*, para isso pela *descriação detalhada da tarefa realizada*.

    """

    cliente.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=pergunta,
    )

    run = cliente.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistente.id,
        tools=[{"type": "retrieval"}],
        model=modelo,
    )

    ran =cliente.beta.threads.runs.retrieve(
        thread_id=thread.id,
        run_id=run.id,
    )

    while run.status != STATUS_COMPLETED:
        ran =cliente.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id,
        )

        if ran.status == STATUS_FAILED:
            raise Exception("OpenAI Falhou!")

    mensagens = cliente.beta.threads.messages.list(
        thread_id=thread.id
    )

    return mensagens.data[0].content[0].text.value
