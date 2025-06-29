from interface_chat import InterfaceChat
from assistente_commit import AssistenteCommit
from assistente_documentacao import AssistenteDocumentacao
from assistente_revisao import AssistenteRevisao
from assistente_teste_unitario import AssistenteTesteInitario

def main():

    caminho_arquivo = "Projeto_Dados/twitch_analytics/data_analytics.py"

    assistente_commmit = AssistenteCommit(caminho_arquivo=caminho_arquivo)
    assistente_chat = InterfaceChat(assistente_commmit)
    lista_mensagens = assistente_chat.conversar("""
    Você pode gerar uma sugestão de *commit* para o *script*
    data_analytics que estou enviando para você?
    """)
    assistente_chat.apagar_assistentente_completamente()

    assistente_documentacao = AssistenteDocumentacao(caminho_arquivo=caminho_arquivo)
    assistente_chat = InterfaceChat(assistente_documentacao)
    lista_mensagens = assistente_chat.conversar("""
    Você pode gerar a documentação para o *script*
    data_analytics que estou enviando para você?
    """)
    assistente_chat.apagar_assistentente_completamente()

    assistente_revisao = AssistenteRevisao(caminho_arquivo=caminho_arquivo)
    assistente_chat = InterfaceChat(assistente_revisao)
    lista_mensagens = assistente_chat.conversar("""
    Você pode gerar uma revisão para o *script*
    evitando a criação de variáveis desnecessárias,
    estou enviando o script para você
    """)
    assistente_chat.apagar_assistentente_completamente()


    for uma_mensagem in lista_mensagens:
        print(f"\n{uma_mensagem.text.value}")

if __name__ == "__main__":
    main()
