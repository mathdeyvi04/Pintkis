from Aplicativos.Tkinter.Reprodutor_Musical_Pintkis.Versão_1_0.BackEndCompleto.Variaveis import *

def volumando(volume_setado: float) -> None:
    mixer.music.set_volume(
        volume_setado / 100
    )


def pausador() -> None:
    """Função responsável por proporcionar a pausa da música.
    Não se limitando à música, também pausa e controla o contador
    da música."""

    # Se estiver tocando algo
    if mixer.music.get_busy():
        mixer.music.pause()

        encerrando_contador_musica(
            musicas_tocadas_na_sessao
        )
    else:
        mixer.music.unpause()

        inicia_contador_musica(
            variaveis_globais[
                "ULTIMA_MUSICA_TOCADA"
            ],
            musicas_tocadas_na_sessao
        )


def inicia_contador_musica(musica: str, estrutura: dict[str: list[bool, float, float]]) -> None:
    """Função responsável por dizer ao programa que algo está tocando, com seu True e com a
    mudança da variável global musica_tocada. Além de salvar em que momento ela inicia."""

    # Como é um dicionário, HashMap, assim que colocarmos ["sanha"],
    # Se a entrada existir, só vai ser atualizada. Caso não exista, será criada.

    # Caso exista, .get(musica) não ser None. Caso não, vai ser None e entramos no else do if.
    tempo_ate_agora = estrutura.get(musica)[0] if estrutura.get(musica) else 0

    # Daí, inicializamos
    estrutura[musica] = [
        tempo_ate_agora,
        round(
            time(),
            1
        )
    ]

    variaveis_globais[
        "ULTIMA_MUSICA_TOCADA"
    ] = musica

    if variaveis_globais["VISUALIZAR_INFORMAÇÕES"]:
        print(f"\nMúsica Inicializada {musica}")
        print(f"A estrutura de músicas tocadas na sessão neste instante:")
        pprint(musicas_tocadas_na_sessao)


def encerrando_contador_musica(estrutura: dict[str: list[bool, float, float]]) -> None:
    """Função responsável por finalizar a reprodução de uma música, colocando False.
    Além de obter a diferença entre os momentos de início e fim da música e incrementar
    o resultado no tempo total em que a música foi ouvida."""

    """Analise a possibilidade de termos uma variável que guarda o nome da música.
    Daí nem precisariamos de um loop procurando essa música. É isso que iremos fazer."""

    # Como não vamos alterar o valor da variável global, podemos só usar ela.
    # Temos a garantia que a música está sendo tocada e, portanto, foi inicializada na estrutura.

    ultima_musica_tocada = variaveis_globais[
        "ULTIMA_MUSICA_TOCADA"
    ]

    # Vamos encerrá-la e atualizar o valor do contador.
    estrutura[ultima_musica_tocada] = [
        round(estrutura[ultima_musica_tocada][0] + (round(time(), 1) - estrutura[ultima_musica_tocada][1]), 1),
        0
    ]

    if variaveis_globais["VISUALIZAR_INFORMAÇÕES"]:
        print(f"\nMúsica Encerrada {ultima_musica_tocada}")
        print(f"A estrutura de músicas tocadas neste instante:")
        pprint(musicas_tocadas_na_sessao)


def tocar(playlist: str, musica: str) -> None:
    """Função responsável por inicializar a música e seu contador.
    Caso algo já esteja sendo tocado, toma as providências necessárias."""

    # Caso não seja uma música
    if not musica.endswith(".mp3"):
        # Então não temos uma música
        messagebox.showwarning("Error",
                               "Isso não é uma música.")
        return None

    # Se algo está já estiver sendo tocado
    if mixer.music.get_busy():
        # Vamos parar
        mixer.music.stop()
        # Descarregar
        mixer.music.unload()
        # E encerrar a música que está tocando
        encerrando_contador_musica(
            musicas_tocadas_na_sessao
        )

        # Chamamos novamente
        return tocar(playlist, musica)
    # Então vamos tocar algo
    else:

        try:

            # Já que nada está sendo tocado, vamos apenas tocar
            mixer.music.load(
                caminhos_possiveis[
                    "Músicas"
                ] + rf"\{playlist}\{musica}"
            )
            mixer.music.play(
                loops=variaveis_globais["LOOPS_DE_MUSICA"]
            )

            # Como tocamos a música com sucesso.
            inicia_contador_musica(
                musica,
                musicas_tocadas_na_sessao,
            )

            if variaveis_globais["VISUALIZAR_INFORMAÇÕES"]:
                print(f"\nMúsica Sendo Tocada em {variaveis_globais['LOOPS_DE_MUSICA']} loops: {musica}")


        except FileNotFoundError:
            messagebox.showerror("ERROR",
                                 "Musica Não Encontrada.")
        except:
            messagebox.showerror(
                "ERROR",
                f"Não foi possível reproduzi-la, erro: {Exception}"
            )
