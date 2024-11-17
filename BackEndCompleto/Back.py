def voltando_a_fabrica():
    """Função responsável por apagar arquivo de geometria e reiniciar."""

    def se_ja_esta_em_fabrica() -> bool:
        """Função responsável por informar se já estamos em configuração de fábrica ou não."""
        try:

            p = open(caminhos_possiveis["Geometrico"], "r")
            p.close()

            return False

        except FileNotFoundError:

            return True

    if not se_ja_esta_em_fabrica():
        if messagebox.askokcancel(
                "Eita",
                "Você vai precisar iniciar o app novamente! Tem certeza?"
        ):
            os.remove(
                caminhos_possiveis["Geometrico"]
            )

            # E pede o reinício.
            exit(3)

    messagebox.showwarning(
        "Rapaz",
        "Já estamos na Geometria de Fábrica."
    )


def atualizador() -> None:
    """Função responsável por, no momemento em que várias músicas não estiverem registradas,
    registrá-las em dados.txt com seu tempo total respectivo zerado."""

    # Vamos apenas varrer as músicas baixadas e ver se cada uma está dentro do arquivo.
    # Pois podemos ter apenas passado por todas e não tê-las lá.
    # Assim essa função aqui não faz alterações, ela apenas adiciona músicas
    # que não estão no arquivo de dados

    # Devemos primeiro, obter o nome de cada uma das músicas.
    # Note que só o ato de obtê-las, já temos um O(n)
    def obtendo_baixadas() -> list[str]:
        """Função responsável por obter todas as músicas que estão dentro da cada playlist"""

        baixadas1 = []
        for pl in listdir(caminhos_possiveis["Músicas"]):
            for mus in listdir(caminhos_possiveis["Músicas"] + rf"\{pl}"):
                if mus.endswith(".mp3"):
                    baixadas1.append(mus)

        return baixadas1

    baixadas: list[str] = obtendo_baixadas()

    def obtendo_registradas() -> list[str] | None:
        """Função responsável por verificar quais são as músicas que já estão no arquivo de dados.
        Note que sempre vamos ter esse arquivo de dados, já que ele é inicializado dentro de variáveis."""

        p = open(caminhos_possiveis["Base_Dados"], 'r', encoding="utf-8")
        linhas = [
            linha.replace("\n", '').split("=")[0] for linha in p.readlines()[1:]
        ]
        p.close()

        return linhas

    registradas: list[str] = obtendo_registradas()

    def verificando():
        return [
            musica for musica in baixadas if musica not in registradas
        ]

    # Se não houver nenhuma registrada, então todas as que estão baixadas
    # também não estão registradas
    nao_registradas: list[str] = baixadas if len(registradas) == 0 else verificando()

    # Então devemos preencher exatamente essas.
    def preenchendo():
        se_ha_outras_musicas = len(registradas) > 0

        with open(caminhos_possiveis["Base_Dados"], 'a', encoding="utf-8") as base:
            for musica in nao_registradas:
                base.write(
                    f"\n{musica}=0"
                )

    # Se houver pelo menos uma música não registrada
    if len(nao_registradas) != 0:
        preenchendo()


def ranking_de_musicas() -> tuple[list[list], str]:
    """Função responsável por obter uma lista ordenada de cada uma das músicas.
    Retornamos exatamente uma lista de listas de músicas e seus tempos em floats"""

    def obtendo_lista_nao_ordenada() -> list[list]:
        """Obtém a lista não ordenada"""

        p = open(caminhos_possiveis["Base_Dados"], 'r', encoding="utf-8")

        linhas = []
        for linha in p.readlines()[1:]:
            linha = linha.replace("\n", '').split("=")

            linhas.append(
                [
                    linha[0],
                    float(linha[1])
                ]
            )

        p.close()

        return linhas

    # Vamos aplicar um método para sorteá-la. Entretanto, queremos apenas as 3 músicas
    # mais tocadas! Então vamos ter que fazer manualmente

    def ordenando(lista_nao_ordenada: list[list], total_no_podio: int = 3) -> list[list]:
        """Vai ordenar nossa lista da forma que desejamos, além de deixar um número
        fixo de cara no pódio."""

        """return sorted(
            lista_nao_ordenada,
            key=lambda sublista: sublista[1],
            reverse=True,
        )[:total_no_podio]
        
        # Dessa forma, nós somos obrigados a ordenar a lista completa. Compreende o quão ruim isso é?"""

        def se_nao_estiver_presente(nome_mus: str, lista: list[list]) -> bool:
            """Apenas uma função que vai verificar se algo NÃO está dentro ou se está."""

            for valor1, valor2 in lista:
                if valor1 == nome_mus:
                    # Afinal, ela foi encontrada na lista
                    return False

            # De fato não está dentro da lista
            return True

        conjunto = []

        # Não vamos ficar nessa de remove, lembre-se que é uma operação de O(n)
        while True:

            if len(conjunto) == total_no_podio or len(conjunto) == len(lista_nao_ordenada):
                return conjunto

            maior = -1
            musica_relativa_ao_maior = None

            for musica, tempo in lista_nao_ordenada:
                # Se for maior que o maior, é porque o maior é ele.
                if tempo > maior:
                    # Veja que estamos fazendo verificações na lista que só vai ter 3 elementos
                    if se_nao_estiver_presente(musica, conjunto):
                        maior = tempo
                        musica_relativa_ao_maior = musica

            conjunto.append(
                [musica_relativa_ao_maior, maior]
            )

        # Note como esse código é bem melhor.

    # De posse dos três caras, devemos obter uma unidade de tempo correspondente
    ordenados = ordenando(
        obtendo_lista_nao_ordenada()
    )

    def obtendo_unidade_temporal_justa(lista_ordenada: list[list]) -> str:
        # Vamos obter o tempo total do último cara, tendo em vista que ele possui o menor tempo
        # Por isso, é a nossa melhor chance

        valores_disponiveis = {
            60: "min",  # Afinal, com 60 segundos, temos 1 minuto.
            60 * 60: "hor",  # Afinal, 60 minutos, temos 60*60 segundos.
            24 * 60 * 60: "dias",  # Você entendeu né?
            30 * 24 * 60 * 60: "mes",
        }

        def obtendo_menor_divisor_comum() -> tuple[int, str]:
            """Nós desejamos modificar os valores dos tempos apenas os dividindo.
            Afinal, estaremos convertendo os valores em novas unidades temporais."""
            menor_tempo: float = ordenados[-1][-1]

            for chave in valores_disponiveis.keys():

                if (menor_tempo / chave) < 1:
                    # Então devemos retornar esse sanhudo
                    return chave, valores_disponiveis[chave]

            # Caso nada pare, devemos deixar no maior possível
            return 30 * 24 * 60 * 60, valores_disponiveis[30 * 24 * 60 * 60]

        menor_divisor, unidade = obtendo_menor_divisor_comum()

        def tratando_os_valores_de_tempo(divisor: int) -> None:

            for index, sublista in enumerate(ordenados):
                # Vamos pegar a divisão e sanhar
                sublista[1]: float = round(
                    sublista[1] / divisor,
                    1
                )

                ordenados[
                    index
                ] = sublista

        tratando_os_valores_de_tempo(
            menor_divisor
        )

        return unidade

    unid = obtendo_unidade_temporal_justa(ordenados)

    return ordenados, unid


def encerrador() -> None:
    """Função responsável por, assim que o usuário fechar o aplicativo de alguma,
    encerrar todos os processos e realizar todos os salvamentos da maneira mais segura possível."""

    # Primeiro, encerrarmos o uso do mixer
    def encerrando_mixer() -> None:
        """Função Responsável por fechar o mixer com segurança"""
        # Se algo estiver tocando, encerramos
        if mixer.music.get_busy():
            # E encerrar a música que está tocando
            encerrando_contador_musica(
                musicas_tocadas_na_sessao
            )

        # Se algo já foi tocado alguma vez
        if variaveis_globais["ULTIMA_MUSICA_TOCADA"] is not None:
            # Vamos parar
            mixer.music.stop()
            # Descarregar
            mixer.music.unload()

    encerrando_mixer()

    # Podemos verificar se há musicas que não estão baixadas.
    atualizador()

    # Vamos atualizar o tempo total das músicas
    def obtendo_dados_salvos() -> dict[str, float]:
        """
        Função responsável por ler todos os dados guardados dentro do
        arquivo de dados.

        Dentro do arquivo de dados devemos ter:

        cores= ##_##_##_##
        música=tempo_total

        Apenas.
        """

        p = open(caminhos_possiveis["Base_Dados"], 'r', encoding="utf-8")
        linhas = p.readlines()[1:]
        p.close()

        informacoes_de_musicas = {}
        for linha in linhas:
            musica, tempo_total = linha.replace("\n", "").split("=")

            informacoes_de_musicas[musica] = float(tempo_total)

        return informacoes_de_musicas

    info_musicas = obtendo_dados_salvos()

    # Devemos salvar os dados de novas cores.
    def salvando_cores() -> str:
        """Função responsável por pegar os widgets e salvar as cores que colocamos em cada um deles."""

        # Devemos pegar os objetos coloridos e analisar as cores meu caro!
        # Se forem iguais às cores padrões, não alteramos nada.
        # Se forem diferentes, devemos por no arquivo.

        novas_cores = []

        # Devemos ter uma forma de pegar as cores de cada widget.

        def comparando_janela():
            novas_cores.append(
                lista_de_objetos_coloridos["Principal"][1].cget("bg_color")
            )

        comparando_janela()

        def comparando_caixa_hover():
            novas_cores.append(
                lista_de_objetos_coloridos["Caixa"][0].cget("fg_color")
            )

            novas_cores.append(
                lista_de_objetos_coloridos["Caixa"][2].cget("hover_color")
            )

        comparando_caixa_hover()

        def comparando_passadores_hover():
            novas_cores.append(
                lista_de_objetos_coloridos["Passadores"][0].cget("fg_color")
            )

            novas_cores.append(
                lista_de_objetos_coloridos["Passadores"][0].cget("hover_color")
            )

        comparando_passadores_hover()

        # Temos nossas cores.
        # Não ironicamente, o join do path se confundiu com o join de iteraveis em strings

        return "=".join(
            ["cores", "_".join(novas_cores)]
        )

    info_cores = salvando_cores()

    # Salvando músicas
    def atualizando_tempo_de_musica():
        """Função Responsável por obter o tempo total de cada música
        e incrementar do valor que acabamos de tocar.
        Note que devido ao atualizador que fizemos no início, sempre vamos ter tudo aqui."""

        # Para cada música que já foi tocada, vamos inseri-la.

        for musica in musicas_tocadas_na_sessao.keys():
            info_musicas[musica] = round(info_musicas[musica] + musicas_tocadas_na_sessao[musica][0], 1)
            print(f"Atualizando {musica} para {info_musicas[musica]}")

    if len(musicas_tocadas_na_sessao.keys()) != 0:
        # Quer dizer que alguma música já foi tocada, então
        # Devemos atualizar o valor.
        atualizando_tempo_de_musica()

    def salvando_geometria():
        """Função responsável por salvar as geometrias."""

        # Podemos inclusive fazer as verificações agora que temos as duas formas salvas.

        """Antes a ideia que tinhamos era percorrer as matrizes a fim de descobrir se há alguma alteração
        e só dps percorrer a matriz de novo para escrevê-la em um arquivo. Entretanto, note que isso nos leva 
        a fazer duas varreduras. Não desejamos isso.
        
        Vamos fazer as verificações enquanto escrevemos em um arquivo. Caso no final todos os elementos sejam realmente 
        iguais, basta apagarmos o arquivo."""

        # Vamos obter a geometria de nascimento
        geo_nascimento: dict[str, list[int]] = obtendo_dicionario_de_geometria()

        # Variável que nos permitirá a otimização.
        ha_mudanca_de_fato: bool = False

        # Vamos escrever nossas informações.
        try:
            arquivo = open(
                caminhos_possiveis["Geometrico"],
                "x"
            )
        except:
            arquivo = open(
                caminhos_possiveis["Geometrico"],
                "w"
            )

        # Temos a chave para ambos.
        primeiro = True
        for chave in dicionario_de_geometria.keys():
            chave: str

            if not chave.startswith("Ferr"):

                # Além de que as listas também são
                for index, elemento in enumerate(dicionario_de_geometria[chave]):

                    # Se houver algum que seja diferente, já sabemos que com certeza houve mudança.
                    if elemento != geo_nascimento[chave][index]:
                        ha_mudanca_de_fato = True

                # Devemos escrever dentro dele
                if primeiro:
                    arquivo.write(f"{chave}={dicionario_de_geometria[chave]}")
                    primeiro = False
                else:
                    arquivo.write(f"\n{chave}={dicionario_de_geometria[chave]}")

        arquivo.close()

        if not ha_mudanca_de_fato:
            # Devemos destruí-lo
            os.remove(
                caminhos_possiveis["Geometrico"]
            )

    if variaveis_globais[
        "HOUVE_MUDANÇA_GEOMETRICA"
    ]:
        salvando_geometria()

    # Finalmente, escrevemos as informações
    def registrando():
        """Função responsável por escrever finalmente as coisas."""

        def escrevendo_cores() -> None:
            """Função responsável por escrever as cores dentro dos arquivos.
            Note que com certeza essa merda deve existir."""
            with open(caminhos_possiveis["Base_Dados"], 'w', encoding="utf-8") as base:
                base.write(info_cores + '\n')

        escrevendo_cores()

        def escrevendo_musicas() -> None:

            # Temos a garantia que o arquivo existe
            # E que colocamos ou não as informações de cores,
            # Sendo assim, podemos:

            # Devemos ter uma forma de saber se estamos no último a colocar
            quant_total = len(info_musicas.keys())
            indice = 0
            with open(caminhos_possiveis["Base_Dados"], 'a', encoding="utf-8") as base:

                for musica in info_musicas.keys():

                    if indice != (quant_total - 1):
                        base.write(f"{musica}={info_musicas[musica]}\n")
                    else:
                        base.write(f"{musica}={info_musicas[musica]}")

                    indice += 1

        escrevendo_musicas()

    registrando()
