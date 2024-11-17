def obtendo_dicionario_de_geometria() -> dict[str: list[int]]:
    """Função responsável por criar todas as posições e distanciamentos entre objetos.
    Podendo ter valores padrões ou não."""

    # Vamos retornar um dicionário que vai ter explicitamente todas as informações que precisamos
    # Sobre posição e dimensão.

    # Vamos tentar abrir um arquivo e pegar as informações que o usuário setou.

    dicionario = {}

    try:

        def tratando_informacoes(dados: str) -> list[int]:

            # Retirando coisas
            dados = dados.replace("\n", '')
            dados = dados.replace("[", '')
            dados = dados.replace("]", '')

            # Agora devemos fazer
            return [int(inteiro) for inteiro in dados.split(",")]

        with open(caminhos_possiveis["Geometrico"], "r") as base:
            for linha in base:
                # Pegando as informações
                chave, informacoes = linha.split("=")

                informacoes = tratando_informacoes(
                    informacoes
                )

                dicionario[
                    chave
                ] = informacoes

    except FileNotFoundError:
        # Então vamos às configurações de geometria padrões

        # Vamos tentar construir da forma mais automática possível.

        dicionario[
            "Principal"
        ] = [400, 210]

        # Vamos adicionar os passadores
        posy_passador = 10
        dicionario["Anterior"] = [
            10,  # Posx
            posy_passador,  # Posy
            30,  # Comprimento
            dicionario["Principal"][1] - 2 * posy_passador
        ]

        dicionario["Proximo"] = [
            dicionario["Principal"][0] - 4 * dicionario["Anterior"][0],
            dicionario["Anterior"][1],
            dicionario["Anterior"][2],
            dicionario["Principal"][1] - 2 * dicionario["Anterior"][1]
        ]

        dicionario["ComboBox_Playlists"] = [
            50,
            20,
            (dicionario["Principal"][0] / 2) - 80,
            21,
        ]

        dicionario["Label de Playlists"] = [
            dicionario["ComboBox_Playlists"][0],
            dicionario["ComboBox_Playlists"][1] - 20,
        ]

        dicionario["ComboBox_Musicas"] = [
            dicionario["ComboBox_Playlists"][0] + dicionario["ComboBox_Playlists"][2] + 20,
            dicionario["ComboBox_Playlists"][1],
            dicionario["ComboBox_Playlists"][2],
            21
        ]

        dicionario["Label de Musicas"] = [
            dicionario["ComboBox_Musicas"][0],
            dicionario["ComboBox_Musicas"][1] - 20,
        ]

        dicionario["Atualizador"] = [
            dicionario["ComboBox_Musicas"][0] + dicionario["ComboBox_Musicas"][2] + 5,
            dicionario["ComboBox_Playlists"][1] - 5,
            30,
            30
        ]

        dicionario["Caixa"] = [
            dicionario["Anterior"][0] + dicionario["Anterior"][2] + 10,
            dicionario["ComboBox_Playlists"][1] + 30,
            dicionario["Proximo"][0] - (dicionario["Anterior"][0] + dicionario["Anterior"][2] + 10) - 10,
            dicionario["Principal"][1] - (dicionario["ComboBox_Playlists"][1] + 30) - 10
        ]

    # Essa parte é comum às duas formas
    a = 30
    dicionario["Ferramenta"] = [
        dicionario["Principal"][0] * 0.165 - 39,
        10,
        a,
        dicionario["Principal"][1] / 2 - 77
    ]

    return dicionario


# Apenas podermos fazer as alterações manualmente.
dicionario_de_geometria = obtendo_dicionario_de_geometria()


def obtendo_informacoes_de_geometria() -> list[list[int]]:
    """Função responsável por obter as informações de geometria de cada
    objeto global. Quando não existir um valor específico, como a janela não
    possui valores de x e de y, devemos colocar -1."""

    lista_completa = []
    for elemento in objetos_globais.values():
        # Já temos acesso aos elementos da tela.
        elemento: Misc | CTk

        lista_completa.append(
            [
                elemento.winfo_x() if elemento.__class__ != Tk else -1,
                elemento.winfo_y() if elemento.__class__ != Tk else -1,
                elemento.winfo_width() if elemento.__class__ != CTkLabel else -1,
                elemento.winfo_height() if elemento.__class__ != CTkLabel else -1,
            ]
        )

    return lista_completa


def transformador(coisa: Misc | CTk, sb: Spinbox, index: int, index_obj: int) -> None:
    """Função responsável por transformar e por transportar nossos objetos na interface
    principal"""

    # Obtendo o novo valor
    novo_valor: int = int(sb.get())

    def alterando_valor_no_dicionario(index_a_ser_alterado: int) -> None:
        nome_da_coisa_segundo_apresentador: str = [obj for obj in objetos_globais.keys()][index_obj]

        # Agora devemos obter o nome que está no dicionário.
        def obtendo_nome_segundo_dicionario(nome: str) -> str:
            match nome:
                case "Playlist":
                    return "ComboBox_Playlists"
                case "Musicas":
                    return "ComboBox_Musicas"
                case _:
                    return nome

        # Então devemos incrementar ou alterar agora dentro do valor
        dicionario_de_geometria[
            obtendo_nome_segundo_dicionario(
                nome_da_coisa_segundo_apresentador
            )
        ][index_a_ser_alterado] = novo_valor

    def alterando_geometria_na_tela() -> int:
        # Devemos saber qual variável desejamos modificar do widget.
        match index:
            case 0:
                # Desejamos alterar o valor do x
                coisa.place_configure(
                    x=novo_valor
                )
                return 0

            case 1:
                coisa.place_configure(
                    y=novo_valor
                )
                return 1
            case 2:
                if coisa.__class__ == Tk:
                    coisa.geometry(
                        f"{novo_valor}x{coisa.winfo_height()}"
                    )
                    return 0
                else:
                    coisa.place_configure(
                        width=novo_valor
                    )
                    return 2

            case 3:
                if coisa.__class__ == Tk:
                    coisa.geometry(
                        f"{coisa.winfo_width()}x{novo_valor}"
                    )
                    return 1
                else:
                    coisa.place_configure(
                        height=novo_valor
                    )
                    return 3

    # Fazendo as modificações
    alterando_valor_no_dicionario(
        alterando_geometria_na_tela()
    )

    variaveis_globais[
        "HOUVE_MUDANÇA_GEOMETRICA"
    ] = True
