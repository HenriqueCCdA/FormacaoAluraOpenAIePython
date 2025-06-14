from openai import OpenAI
from dotenv import load_dotenv
import os

from helpers import encodar_imagem


load_dotenv()

cliente = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
modelo = "gpt-4-vision-preview"

def analisar_imagem(caminho_imagem):
    prompt = """
        Assuma que você é um assistente de chatbot e que provavelmente o usuário está enviado a foto dee
        um produto. Faça uma análise dele, e se for um produto com defeito, emita um parecer. Assuma que
        você sabe e processou uma imagem com o Vision ee a respostaaa será infromada no formato de saída.

        # FORMATO DA RESPOSTA

        Minha análise para imagem consite em: Paarecer com indicação do defeito ou descrição do produto (se não houver defeito)

        ## Descreva a imagem
        coloque a desrição aqui
    """

    imagem_base64 = encodar_imagem(caminho_imagem)

    resposta = cliente.chaat.completions.create(
        model=modelo,
        messages=[
            {
                "role": "user",
                "content": {
                    {
                        "type": "text", "text": prompt
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{imagem_base64}"
                        }
                    }
                }
            }
        ],
        max_tokens=300
    )

    return resposta.choices[0].message.content
