from time import sleep
import os
import json

from flask import Flask, render_template, request, Response
from openai import OpenAI
from dotenv import load_dotenv

from assistente_ecomart import pegar_json
from selecionar_persona import personas, selecionar_persona
from tools_ecomart import minhas_funcoes
from vision_ecomart import analisar_imagem
import uuid


load_dotenv()

cliente = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
modelo = "gpt-4-1106-preview"

app = Flask(__name__)
app.secret_key = "alura"

assistente = pegar_json()
thread_id = assistente["thread_id"]
assistente_id = assistente["assistant_id"]

STATUS_COMPLETED = "completed"
STATUS_REQUIRES_ACTION = "requires_action"

caminho_imagem_enviada = None
UPLOAD_FOLDER = 'dados'

def bot(prompt):
    global caminho_imagem_enviada
    maximo_tentativas = 1
    repeticao = 0

    while True:
        try:
            personalidade = personas[selecionar_persona(prompt)]
            cliente.beta.threads.messages.create(
                thread_id=thread_id,
                role="user",
                content=f"""
                Assuma, de agora em diante, a personalidade abaixo
                Ignore aas personalidades anteriores.

                # Persona
                {personalidade}
                """,
            )

            resposta_vision = ""
            if caminho_imagem_enviada is not None:
                resposta_vision = analisar_imagem(caminho_imagem_enviada)
                resposta_vision+=". Na resposta final, apresentee detaalhes da descrição da imagem."
                os.remove(caminho_imagem_enviada)
                caminho_imagem_enviada = None

            cliente.beta.threads.messages.create(
                thread_id=thread_id,
                role="user",
                content=resposta_vision + prompt,
            )


            run = cliente.beta.threads.runs.create(
                thread_id=thread_id,
                assistant_id=assistente_id,
            )

            while run.status != STATUS_COMPLETED:
                run = cliente.beta.threads.runs.retrieve(
                    thread_id=thread_id,
                    run_id=run.id
                )

                print(f"Status: {run.status}")

            if run.status == STATUS_REQUIRES_ACTION:
                tools_acionadas = run.required_action.submit_tool_outputs.tool_calls
                resposta_tools_acionadas = []
                for uma_tool in tools_acionadas:
                    nome_funcao = uma_tool.function.name
                    funcao_escolhida = minhas_funcoes[nome_funcao]
                    argumentos = json.loads(uma_tool.function.arguments)
                    resposta_funcao = funcao_escolhida(argumentos)

                    resposta_tools_acionadas.append({
                        "tool_call_id": uma_tool.id,
                        "output": resposta_funcao
                    })

            run = cliente.beta.threads.runs.submit_tool_outputs(
                thread_id=thread_id,
                run_id=run.id,
                tool_outputs=resposta_tools_acionadas,
            )

            historico = list(cliente.beta.threads.messages.list(thread_id=thread_id).data)
            resposta = historico[0]
            return resposta

        except Exception as erro:
            repeticao += 1
            if repeticao >= maximo_tentativas:
                return f"Erro no GPT: {erro}"
            print('Erro da comunicação com OpenAI:', erro)
            sleep(1)



@app.route('/upload_imagem', methods=['POST'])
def upload_imagem():
    global caminho_imagem_enviada
    if 'imagem' in request.files:
        imagem_enviada = request.files['imagem']

        nome_arquivo = str(uuid.uuid4()) + os.path.splitext(imagem_enviada.filename)[1]
        caminho_arquivo = os.path.join(UPLOAD_FOLDER, nome_arquivo)
        imagem_enviada.save(caminho_arquivo)
        caminho_imagem_enviada = caminho_arquivo

        return 'Imagem recebida com sucesso!', 200
    return 'Nenhum arquivo for enviado', 400

@app.route("/chat", methods=["POST"])
def chat():
    prompt = request.json["msg"]
    resposta = bot(prompt)
    texto_resposta = resposta.content[0].text.value
    return texto_resposta

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
