from gerador_casos_uso import gerar_caso_uso
from gerador_cenario_teste import gerar_cenario_teste
from gerador_scrip_teste import gerar_script_teste
from tools import salva


def main():
    pedido_usuario = input("Digite um caso de uso:")

    casos_uso = gerar_caso_uso(pedido_usuario)
    print(f"\nCaso de Uso\n", casos_uso)

    cenario_teste = gerar_cenario_teste(caso_uso=casos_uso)
    print(f"\nCenário Teste\n",cenario_teste)

    script_teste = gerar_script_teste(caso_uso=casos_uso, cenario_teste=cenario_teste)
    print("\nCenario Teste\n", script_teste)

    salva("script_temp_ia.py", script_teste)

if __name__ == "__main__":
    main()
