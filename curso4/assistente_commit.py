from datetime import datetime
from assistente_base import AssistenteBase
from util_io import pegar_nome_arquivo_json, calcular_diferencas, ler_conteudo_arquivo, salvar_json
from util_hash import gerar_hash
import os
import json


class  AssistenteCommit(AssistenteBase):
    def __init__(self, caminho_arquivo: str):
        self.caminho_arquivo = caminho_arquivo
        self.caminho_json = pegar_nome_arquivo_json(self.caminho_arquivo)
        self.gerar_resposta()
        self.nome = self.nome_assistente
        self.instrucoes = self.instrucoes_assistente
        super().__init__(self.nome, self.instrucoes, caminho_arquivo)

    def gerar_resposta(self):
        hash_documento = gerar_hash(self.caminho_arquivo)
        data_atual = datetime.now().isoformat()
        conteudo_atual = ler_conteudo_arquivo(self.caminho_arquivo)

        if os.path.exists(self.caminho_json):
            with open(self.caminho_json, 'r', encoding='utf-8') as file:
                dados = json.load(file)
                conteudo_anterior = dados["conteudo"]
        else:
            dados = {
                'caminho_arquivo': self.caminho_arquivo,
                'data_criacao': data_atual,
                'data_atualizacao': data_atual,
                'hash_atual': hash_documento,
                'versao': 1,
                'conteudo': conteudo_atual,
                'mudancas': '',
            }
            salvar_json(self.caminho_json, dados)

        if dados['hash_atual'] != hash_documento:
            dados['data_atualizacao'] = data_atual
            dados['hash_atual'] = hash_documento
            dados['versao'] += 1
            dados['conteudo'] = conteudo_atual
            dados['mutancas'] = calcular_diferencas(conteudo_anterior, conteudo_atual)

            salvar_json(self.caminho_json, dados)

        return dados

    @property
    def nome_assistente(self):
        return "Assistente de Commits"

    @property
    def instrucoes_assistente(self):

        return f"""
        Assuma que você é um assistente especialista em gerar commits para o Github.
        Você, nos títulos, escolhe até dois símbolos que representam o código que você está analisando.

        Além disso, você usa textos objetivos para o título, e usa commit patterns para ele.
        Na descrição você faz detalhes que demonstram o nome da classe e os métodos implementados.

        # Referência de Imagens para título (use sempre a referencia textual, exemplo :sparkles:)
        Initial commit:tada:
        Version tag:bookmark:
        New feature:sparkles:
        Bugfix:bug:
        Metadata:card_index:
        Documentation:books:
        Documenting source code :bulb:
        Performance :racehorse:
        Cosmetic:lipstick:
        Tests:rotating_light:
        Adding a test:white_check_mark:
        Make a test pass :heavy_check_mark:
        General update :zap:
        Improve format/structure :art:
        Refactor code :hammer:
        Removing code/files :fire:
        Continuous Integration :green_heart:
        Security :lock:
        Upgrading dependencies :arrow_up:
        Downgrading dependencies :arrow_down:
        Lint :shirt:
        Translation:alien:
        Text :pencil:
        Critical hotfix:ambulance:
        Deploying stuff:rocket:
        Fixing on MacOS:apple:
        Fixing on Linux:penguin:
        Fixing on Windows:checkered_flag:
        Work in progress:construction:
        Adding CI build system:construction_worker:
        Analytics or tracking code:chart_with_upwards_trend:
        Removing a dependency:heavy_minus_sign:
        Adding a dependency:heavy_plus_sign:
        Docker: whale:
        Configuration files:wrench:
        Package.json in JS:package:
        Merging branches:twisted_rightwards_arrows:
        Bad code / need improv. :hankey:
        Reverting changes:rewind:
        Breaking changes:boom:
        Code review changes:ok_hand:
        Accessibility	:wheelchair:
        Move/rename repository :truck:
        Other	Be creative

        # Tarefa

        1. Analisar o código para entender as funcionalidades providas no script.
        2. Descreva cada método e suas funcionalidades.
        3. Gere uma mensagem de commit, em português, clara e concisa que resuma a introdução e o propósito desta nova classe, considerando as melhores práticas para mensagens de commit.
        4. Para resolver a tarefa, considere os metadados do usuário, disponíveis em: {ler_conteudo_arquivo(self.caminho_json)}, e acesse o atributo mudanças do JSON.
        4.1 Caso não existam mudanças, considere como primeira versão
        4.2 Caso existam, considere como uma atualização.
        """
