from assistente import Assistente

def criar_assistente():
    nome_assistente = "Analisador de Código"
    instrucoes_assistente = """
    Você reveberá um script em Python que resolve um problema computacional
    Seu objectivo é avaliar a complexidade de algoritmo desta solução ee dar um parecer aao final do processo.

    # Para isso:

    1. Faça uma leitura do Script, analisando seu propṕsito e associando ao pedido do usuário
    2. FAla um análise da complexidade do algoritimo implementando, considerando o pior caso
    3. Faça uma análise da eficiência do algoritmo, considerando o uso de memóriaa e processamento
    4. Dê um parecer final sobre a solução, indicando se é adequada par o problema proposto
    5. Caso identifique oportunidade de melhoria, sugira aalterações ou otimizações.
    """

    return Assistente(nome=nome_assistente, instrucoes=instrucoes_assistente)

def chat(pergunta, caminho_arquivo):
    professor = criar_assistente()

    while pergunta != "fim":
        resposta = professor.perguntar(
            pergunta=pergunta,
            caminho_arquivo=caminho_arquivo
        )
        print(f"\n\nResposta: {resposta}")

        #resposta_avaliada = professor.avaliar_resultado(resposta, pergunta)

        #print(f"\n\nAvaliação: {resposta_avaliada}")

        pergunta = input("\nDigite a sua nova pergunta, ou digite 'fim' para encerrar: ")

    professor.apagar_agente()

def main():
    caminho_arquivo = input("Digite o nome do arquivo que você deseja analisar: ")
    pergunta_inicial = input("Digite a sua dúvida: ")

    chat(pergunta=pergunta_inicial, caminho_arquivo=caminho_arquivo)

if __name__ == "__main__":
    main()
