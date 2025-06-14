from openai import OpenAI
from dotenv import load_dotenv
import os


load_dotenv()

cliente = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
modelo = "gpt-4-1106-preview"

minha_tools = [
    # {"type": "retrievel"},
    {'type': 'file_search'},
    {
        "type": "function",
            "function": {
            "name": "validar_codigo_promocional",
            "description": "Valide um código promocional com base nas diretrizes de Descontos e Promoções da empresa",
            "parameters": {
                "type": "object",
                "properties": {
                    "codigo": {
                        "type": "string",
                        "description": "O código promocional, no formato, CUPOM_XX. Por exemplo: CUPOM_ECO",
                    },
                    "validade": {
                        "type": "string",
                         "description": f"A validade do cupom, caso seja válido e esteja associado as políticas. No formato DD/MM/YYYY.",
                    },
                },
                "required": ["codigo", "validade"],
            }
        }
    }
]

def validar_codigo_promocional(argumentos):
    codigo = argumentos.get("codigo")
    validade = argumentos.get("validade")

    return f"""

        # Formato de Resposta

        {codigo} com validade: {validade}.
        Ainda, diga se é vaslido ou não para o usuário.
    """

minhas_funcoes = {
    "validar_codigo_promocional": validar_codigo_promocional
}
