from Aplicativos.Tkinter.Reprodutor_Musical_Pintkis.Versão_1_0.BackEndCompleto.FuncoesMusica import *


def passador(sinal: int, cb_p: ttk.Combobox, cb_m: ttk.Combobox) -> None | str:
    """Função responsável por movimentar as músicas pelo tocador."""

    # Devemos alterar o combobox para a música que virá antes ou depois.
    # Além disso, devemos conseguir tocar essa música imediatamente.

    if not cb_m.get().endswith(".mp3"):
        # Então não temos uma música
        return messagebox.showwarning("Error",
                                      "Isso não é uma música.")

    # Já que é uma música, vamos manipular tudo
    lista_musicas: list = cb_m["values"]
    # print(f"A lista de músicas é {lista_musicas}")

    # Agora, devemos obter qual é o index dessa música dentro da lista
    index_setada = lista_musicas.index(
        cb_m.get()
    )
    # print(f"O index é {index_setada}")

    # Vamos obter a nova música
    nova_musica = lista_musicas[
        (index_setada + sinal) % len(lista_musicas)
        ]

    # Vamos setar no combobox
    cb_m.set(
        nova_musica
    )

    # E vamos tocá-la.
    tocar(cb_p.get(), cb_m.get())


def playlist_selecionada(conjunto_de_playlist: ttk.Combobox,
                         conjunto_de_musicas: ttk.Combobox) -> None:
    """Função responsável por atualizar o combobox das músicas a cada vez que selecionamos uma
    playlist."""

    # Devemos obter qual a playlist foi selecionada
    pl_selec: str = conjunto_de_playlist.get()

    # Após isso, devemos colocar essas músicas dentro do combobox das músicas
    conjunto_de_musicas["values"]: list[str] = listdir(
        caminhos_possiveis["Músicas"] + fr"\{pl_selec}"
    )

    conjunto_de_musicas.set("Selec Música")

    def desetando():
        conjunto_de_musicas.configure(foreground="black")

    conjunto_de_musicas.bind("<<ComboboxSelected>>", lambda event: desetando())


def atualizando_comboboxs(cb_a_ser_atualizado: ttk.Combobox, caminho: str, para_setar: str | bool = False) -> None:
    # Atualizando
    cb_a_ser_atualizado[
        "values"
    ] = listdir(
        caminho
    )

    if para_setar:
        # Se não for False
        cb_a_ser_atualizado.set(
            para_setar
        )


def apagando_playlist(cb_pl: ttk.Combobox) -> None:
    # Vamos pegar um caminho e enviá-lo para o lixo.
    caminho_para_diretorio = caminhos_possiveis["Músicas"] + fr"\{cb_pl.get()}"

    # Se existir alguma dentro,
    if listdir(
            caminho_para_diretorio
    ):
        # Vamos perguntar ao usuário

        if not messagebox.askokcancel(
                "Eita!",
                "Há músicas dentro dessa playlist, deseja mesmo apagar?"
        ):
            return None

    # Caso esteja vazia, não há problema algum
    send2trash(
        caminho_para_diretorio
    )

    # E devemos atualizar o combobox de playlist
    atualizando_comboboxs(
        cb_pl,
        caminhos_possiveis["Músicas"]
    )

    return None


def criando_playlist(entrada_do_nome: Entry, frase_de_ajuda: str) -> None:
    # Vamos apenas colocar uma nova playlist no local indicado.

    # Devemos tratar o nome também né.
    if entrada_do_nome.get() in [frase_de_ajuda, ""]:
        return None

    caminho_novo_diretorio = caminhos_possiveis["Músicas"] + fr"\{entrada_do_nome.get()}"

    mkdir(
        caminho_novo_diretorio
    )

    # Como criamos uma playlist, devemos no minimo acrescentá-la ao combobox.
    atualizando_comboboxs(
        objetos_globais["Playlist"],
        caminhos_possiveis["Músicas"],
        entrada_do_nome.get()
    )

    entrada_do_nome.delete(
        0, 'end'
    )


def baixando_musica(nome_playlist: str, nome_da_musica: str, link_da_musica: str) -> bool:
    if not messagebox.askokcancel(
            "Rapaz",
            f"Tem certeza que deseja baixar {nome_da_musica} dentro de {nome_playlist}?"
    ):
        return False

    # Carregando a música como video, .mp4, mas contendo apenas
    # o som do vídeo
    def se_deu_certo_baixar_mp4() -> bool:
        try:
            yt = YouTube(
                link_da_musica
            ).streams.filter(
                only_audio=True,
            ).first().download(
                caminhos_possiveis["ONDE_MP4_VAI"]
            )

            return True
        except Exception as e:
            print(e)
            # Pode dar um erro ao tentar carregar ou baixar a música
            messagebox.showerror(
                "ERROR",
                "Erro ao tentar achar ou baixar a música referente ao link. Talvez conexão ou link errado."
            )

            return False

    if not se_deu_certo_baixar_mp4():
        return False

    # Agora, devemos converter o video .mp4 para um som .mp3
    def se_deu_certo_converter() -> bool:

        try:
            # Vamos procurar o arquivo
            for arquivo in listdir(caminhos_possiveis["ONDE_MP4_VAI"]):
                if arquivo.endswith(".mp4"):
                    # Achamos a música .mp4

                    # Então vamos pegar ela e reescrevê-la
                    AudioFileClip(
                        # Dizendo de qual arquivo desejamos o .mp3
                        caminhos_possiveis["ONDE_MP4_VAI"] + rf"\{arquivo}"
                    ).write_audiofile(
                        # Vamos finalmente criar o arquivo .mp3
                        caminhos_possiveis["Músicas"] + fr"\{nome_playlist}\{nome_da_musica}.mp3"
                    )

                    # Como já extraimos o .mp3 do .mp4, não precisamos mais dele
                    remove(
                        caminhos_possiveis["ONDE_MP4_VAI"] + rf"\{arquivo}"
                    )

                    # Pelo jeito que construimos, garantimos que há apenas 1 .mp4
                    break

            return True

        except:
            messagebox.showerror(
                "ERROR",
                "Erro ao tentar converter do mp4 para mp3"
            )

            return False

    if not se_deu_certo_converter():
        return False

    return True


def atualizando_apos_download(playlist_download: str, musica_download: str) -> None:
    # Vamos atualizar nossos pontos

    se_estamos_na_mesma_playlist_de_download: bool = objetos_globais["Playlist"].get() == playlist_download

    if not se_estamos_na_mesma_playlist_de_download:
        # Então devemos setar primeiro a playlist e logo mais colocar a música.
        objetos_globais["Playlist"].set(
            # Colocando dentro da playlist de download
            playlist_download
        )

    atualizando_comboboxs(
        objetos_globais["Musicas"],
        caminhos_possiveis["Músicas"] + rf"\{playlist_download}",
        musica_download
    )

    return None


def definindo_loops(resultado_cb: str) -> None:
    """Função responsável por alterar a fila de músicas"""

    novo_modo: int = 0
    if resultado_cb.startswith("Inf"):
        novo_modo = -1
    else:
        # Esse menos um é devido à biblioteca mesmo
        novo_modo = int(resultado_cb.split()[0]) - 1

    if variaveis_globais["LOOPS_DE_MUSICA"] == novo_modo:
        return None

    variaveis_globais["LOOPS_DE_MUSICA"] = novo_modo

    # Vamos colocar a música para ser tocada do ínicio utilizando esse novo modo
    tocar(
        objetos_globais["Playlist"].get(),
        objetos_globais["Musicas"].get()
    )
