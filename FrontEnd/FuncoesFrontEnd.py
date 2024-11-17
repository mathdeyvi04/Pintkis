def criando_janela(titulo: str, dimensoes: tuple[int, int], sub: bool = False) -> Tk | Toplevel:
    """Função capaz de criar uma instância de janela, seja ela primária ou secundária.
    Já retorna com todas as configurações que precisamos."""

    if sub:
        jan = Toplevel()
    else:
        jan = Tk()
        jan.iconbitmap(
            caminhos_possiveis[
                "Figuras"
            ] + r"\pinto_1.ico"
        )

    jan.title(titulo)
    jan.geometry(f"{dimensoes[0]}x{dimensoes[1]}")
    jan.configure(bg=COR_JANELA)
    jan.resizable(width=False, height=False)

    # Vamos adicionar a janela aos serem coloridos
    if not sub:
        # Afinal, só queremos uma janela principal.
        lista_de_objetos_coloridos[
            "Principal"
        ] = [jan]

        objetos_globais[
            "Principal"
        ] = jan

    return jan


def coisas_basicas(mestre: Tk, dicionario_de_cartesiano: dict[str: tuple[int]]) -> None:
    """Função do FrontEnd que cria todos os widgets mais simples que temos na interface."""

    # Vamos construir as coisas mais super básicas

    def combobox_das_playlists() -> ttk.Combobox:
        # O Label Indicando.

        lb = CTkLabel(
            mestre,
            text='Playlists',
            text_color="black",

            bg_color=COR_JANELA,
        )
        lb.place(
            x=dicionario_de_cartesiano["Label de Playlists"][0],
            y=dicionario_de_cartesiano["Label de Playlists"][1],
        )

        objetos_globais[
            "Label de Playlists"
        ] = lb

        lista_de_objetos_coloridos[
            "Principal"
        ].append(
            lb
        )

        cb = ttk.Combobox(
            mestre,
            values=listdir(
                caminhos_possiveis[
                    "Músicas"
                ]
            ),
            state="readonly"
        )
        cb.place(
            x=dicionario_de_cartesiano["ComboBox_Playlists"][0],
            y=dicionario_de_cartesiano["ComboBox_Playlists"][1],
            width=dicionario_de_cartesiano["ComboBox_Playlists"][2]
        )

        objetos_globais["Playlist"] = cb

        return cb

    cb_playlist = combobox_das_playlists()

    def combobox_das_musicas() -> ttk.Combobox:
        lb = CTkLabel(
            mestre,
            text='Músicas',
            text_color="black",

            bg_color=COR_JANELA,

        )
        lb.place(
            x=dicionario_de_cartesiano["Label de Musicas"][0],
            y=dicionario_de_cartesiano["Label de Musicas"][1]
        )

        objetos_globais[
            "Label de Musicas"
        ] = lb

        lista_de_objetos_coloridos[
            "Principal"
        ].append(
            lb
        )

        cb = ttk.Combobox(
            mestre,
            state="readonly"
        )
        cb.place(
            x=dicionario_de_cartesiano["ComboBox_Musicas"][0],
            y=dicionario_de_cartesiano["ComboBox_Musicas"][1],
            width=dicionario_de_cartesiano["ComboBox_Musicas"][2]
        )

        objetos_globais["Musicas"] = cb

        return cb

    cb_musicas = combobox_das_musicas()

    # Toda vez que colocarmos uma playlist selecionada,
    # o combobox das músicas também deve ser atualizado

    cb_playlist.bind("<<ComboboxSelected>>", lambda event: playlist_selecionada(cb_playlist, cb_musicas))

    def proxima_musica(combo_playlist: ttk.Combobox, combo_musicas: ttk.Combobox) -> None:
        btn = CTkButton(mestre,
                        text=" > ",

                        command=lambda: passador(
                            1,
                            combo_playlist,
                            combo_musicas
                        ),

                        fg_color=COR_PASSADOR,
                        hover_color=COR_HOVER_PASSADOR,

                        width=dicionario_de_cartesiano["Proximo"][2],
                        height=dicionario_de_cartesiano["Proximo"][3],
                        )

        btn.place(
            x=dicionario_de_cartesiano["Proximo"][0],
            y=dicionario_de_cartesiano["Proximo"][1]
        )

        lista_de_objetos_coloridos[
            "Passadores"
        ] = [btn]

        objetos_globais["Proximo"] = btn

    proxima_musica(
        cb_playlist,
        cb_musicas
    )

    def anterior_musica(combo_playlist: ttk.Combobox, combo_musicas: ttk.Combobox) -> None:
        btn = CTkButton(mestre,
                        text=" < ",

                        command=lambda: passador(
                            -1,
                            combo_playlist,
                            combo_musicas
                        ),

                        fg_color=COR_PASSADOR,
                        hover_color=COR_HOVER_PASSADOR,

                        border_width=0,
                        width=dicionario_de_cartesiano["Anterior"][2],
                        height=dicionario_de_cartesiano["Anterior"][3],
                        )

        btn.place(
            x=dicionario_de_cartesiano["Anterior"][0],
            y=dicionario_de_cartesiano["Anterior"][1]
        )

        lista_de_objetos_coloridos[
            "Passadores"
        ].append(
            btn
        )

        objetos_globais["Anterior"] = btn

    anterior_musica(
        cb_playlist,
        cb_musicas
    )

    def botao_atualizador():
        btn = CTkButton(
            mestre,
            text="",
            image=CTkImage(
                light_image=Image.open(
                    caminhos_possiveis["Figuras"] + r"\atualiza.png"
                ),
                size=(
                    20,
                    20,
                )
            ),

            command=atualizador,

            hover_color="#e4e4ed",
            fg_color=COR_JANELA,
            width=dicionario_de_cartesiano["Atualizador"][2],
            height=dicionario_de_cartesiano["Atualizador"][3]

        )

        btn.place(
            x=dicionario_de_cartesiano["Atualizador"][0],
            y=dicionario_de_cartesiano["Atualizador"][1]
        )

        lista_de_objetos_coloridos[
            "Principal"
        ].append(
            btn
        )

        objetos_globais["Atualizador"] = btn

    botao_atualizador()


def caixa_de_ferramentas(mestre: Tk, dicionario_de_cartesiano: dict[str: tuple[int]]) -> None:
    """Função que cria todos os widgets que ficam dentro da caixa de ferramentas, isto é,
    o CTkFrame."""

    # Vamos iniciar construindo um Frame central.
    def frame_central() -> CTkFrame:
        fr = CTkFrame(
            mestre,
            width=dicionario_de_cartesiano["Caixa"][2],
            height=dicionario_de_cartesiano["Caixa"][3],
            corner_radius=8,
            bg_color=COR_JANELA,
            fg_color=COR_CAIXA
        )
        fr.place(
            x=dicionario_de_cartesiano["Caixa"][0],
            y=dicionario_de_cartesiano["Caixa"][1],
        )

        lista_de_objetos_coloridos[
            "Caixa"
        ] = fr

        # Vamos colocar todos os outros objetos dentro da lista subsequente.
        objetos_globais["Caixa"] = fr

        lista_de_objetos_coloridos["Caixa"] = [fr]

        return fr

    # A caixa
    frame = frame_central()

    # Vamos colocar nossos botões dentro

    n_linha = 0
    n_coluna = 0

    def botao_colorir():
        btn = CTkButton(
            frame,
            text="",
            image=CTkImage(
                light_image=Image.open(
                    caminhos_possiveis["Figuras"] + r"\colorir.png"
                ),
                size=(
                    dicionario_de_cartesiano["Ferramenta"][2],
                    dicionario_de_cartesiano["Ferramenta"][3]
                )
            ),

            command=colorindo,

            fg_color=frame.cget("fg_color"),
            # Mudar a cor após passar o mouse
            hover_color=COR_HOVER_CAIXA,
            width=dicionario_de_cartesiano["Ferramenta"][2],
            height=dicionario_de_cartesiano["Ferramenta"][3]
        )

        btn.grid(
            row=n_linha,
            column=n_coluna,
            padx=dicionario_de_cartesiano["Ferramenta"][0],
            pady=dicionario_de_cartesiano["Ferramenta"][1]
        )

        lista_de_objetos_coloridos["Caixa"].append(
            btn
        )

    botao_colorir()

    n_coluna += 1

    def botao_download():
        btn = CTkButton(
            frame,
            text="",
            image=CTkImage(
                light_image=Image.open(
                    caminhos_possiveis["Figuras"] + r"\download.png"
                ),
                size=(
                    dicionario_de_cartesiano["Ferramenta"][2],
                    dicionario_de_cartesiano["Ferramenta"][3]
                )
            ),

            command=gerenciador_de_arquivos,

            fg_color=frame.cget("fg_color"),
            # Mudar a cor após passar o mouse
            hover_color=COR_HOVER_CAIXA,
            width=dicionario_de_cartesiano["Ferramenta"][2],
            height=dicionario_de_cartesiano["Ferramenta"][3]
        )

        btn.grid(
            row=n_linha,
            column=n_coluna,
            padx=dicionario_de_cartesiano["Ferramenta"][0],
            pady=dicionario_de_cartesiano["Ferramenta"][1]
        )

        lista_de_objetos_coloridos["Caixa"].append(
            btn
        )

    botao_download()

    n_coluna += 1

    def botao_config():
        btn = CTkButton(
            frame,
            text="",
            image=CTkImage(
                light_image=Image.open(
                    caminhos_possiveis["Figuras"] + r"\configuracoes.png"
                ),
                size=(
                    dicionario_de_cartesiano["Ferramenta"][2],
                    dicionario_de_cartesiano["Ferramenta"][3]
                )
            ),

            command=configurador,

            fg_color=frame.cget("fg_color"),
            # Mudar a cor após passar o mouse
            hover_color=COR_HOVER_CAIXA,
            width=dicionario_de_cartesiano["Ferramenta"][2],
            height=dicionario_de_cartesiano["Ferramenta"][3]
        )

        btn.grid(
            row=n_linha,
            column=n_coluna,
            padx=dicionario_de_cartesiano["Ferramenta"][0],
            pady=dicionario_de_cartesiano["Ferramenta"][1]
        )

        lista_de_objetos_coloridos["Caixa"].append(
            btn
        )

    botao_config()

    n_linha += 1
    n_coluna = 0

    def botao_reiniciar():
        btn = CTkButton(
            frame,
            text="",
            image=CTkImage(
                light_image=Image.open(
                    caminhos_possiveis["Figuras"] + r"\reiniciar.png"
                ),
                size=(
                    dicionario_de_cartesiano["Ferramenta"][2],
                    dicionario_de_cartesiano["Ferramenta"][3]
                )
            ),

            command=lambda: tocar(
                objetos_globais["Playlist"].get(),
                objetos_globais["Musicas"].get()
            ),

            fg_color=frame.cget("fg_color"),
            # Mudar a cor após passar o mouse
            hover_color=COR_HOVER_CAIXA,
            width=dicionario_de_cartesiano["Ferramenta"][2],
            height=dicionario_de_cartesiano["Ferramenta"][3]
        )

        btn.grid(
            row=n_linha,
            column=n_coluna,
            padx=dicionario_de_cartesiano["Ferramenta"][0],
            pady=dicionario_de_cartesiano["Ferramenta"][1]
        )

        lista_de_objetos_coloridos["Caixa"].append(
            btn
        )

    botao_reiniciar()

    n_coluna += 1

    def botao_tocar():
        btn = CTkButton(
            frame,
            text="",
            image=CTkImage(
                light_image=Image.open(
                    caminhos_possiveis["Figuras"] + r"\tocador.png"
                ),
                size=(
                    dicionario_de_cartesiano["Ferramenta"][2],
                    dicionario_de_cartesiano["Ferramenta"][3]
                )
            ),

            command=lambda: tocar(
                objetos_globais["Playlist"].get(),
                objetos_globais["Musicas"].get()
            ),

            fg_color=frame.cget("fg_color"),
            # Mudar a cor após passar o mouse
            hover_color=COR_HOVER_CAIXA,
            width=dicionario_de_cartesiano["Ferramenta"][2],
            height=dicionario_de_cartesiano["Ferramenta"][3],
        )

        btn.grid(
            row=n_linha,
            column=n_coluna,
            padx=dicionario_de_cartesiano["Ferramenta"][0],
            pady=dicionario_de_cartesiano["Ferramenta"][1]
        )

        lista_de_objetos_coloridos["Caixa"].append(
            btn
        )

    botao_tocar()

    n_coluna += 1

    def botao_pause():
        btn = CTkButton(
            frame,
            text="",
            image=CTkImage(
                light_image=Image.open(
                    caminhos_possiveis["Figuras"] + r"\pause.png"
                ),
                size=(
                    dicionario_de_cartesiano["Ferramenta"][2],
                    dicionario_de_cartesiano["Ferramenta"][3]
                )
            ),

            command=pausador,

            fg_color=frame.cget("fg_color"),
            # Mudar a cor após passar o mouse
            hover_color=COR_HOVER_CAIXA,
            width=dicionario_de_cartesiano["Ferramenta"][2],
            height=dicionario_de_cartesiano["Ferramenta"][3],
        )

        btn.grid(
            row=n_linha,
            column=n_coluna,
            padx=dicionario_de_cartesiano["Ferramenta"][0],
            pady=dicionario_de_cartesiano["Ferramenta"][1]
        )

        lista_de_objetos_coloridos["Caixa"].append(
            btn
        )

    botao_pause()

    n_linha += 1
    n_coluna = 0

    def barra_volume():
        barra = CTkSlider(
            frame,
            from_=0,
            to=100,
            hover=True,
            fg_color=COR_CAIXA,
            button_color="black",
            command=volumando
        )
        barra.set(
            variaveis_globais["VALOR_DE_SOM_SEGURO"]
        )

        barra.grid(
            row=n_linha,
            column=n_coluna,
            columnspan=3,
            padx=dicionario_de_cartesiano["Ferramenta"][0],
            pady=dicionario_de_cartesiano["Ferramenta"][1]
        )

        lista_de_objetos_coloridos["Caixa"].append(
            barra
        )

    barra_volume()


def colorindo() -> None:
    """Função responsável por criar toda a interface e manejamento das opções de cores
    para o usuário escolher."""

    # Vamos disponibilizar uma forma
    # do usuário decidir qual cor ele deseja.

    cores_disponiveis = [['Preto', 'black'],
                         ['Branco', 'white'],
                         ['Vermelho', 'red'],
                         ['Verde', 'green'],
                         ['Azul', 'blue'],
                         ['Amarelo', 'yellow'],
                         ['Laranja', 'orange'],
                         ['Roxo', 'purple'],
                         ['Rosa', 'pink'],
                         ['Marrom', 'brown'],
                         ['Cinza', 'gray'],
                         ['Persona', 'persona'],
                         ]

    # Conjunto de Títulos de Cada Frame
    # Muito responsável pelo layout
    apresentacoes = [
        "Cor Para Janela Principal",
        "Cor Para Caixa de Ferramentas",
        "Cor Para Hover do Mouse",
        "Cor Para Passadores",
        "Cor Para Hover de Passadores"
    ]

    # Conjunto de classes de objetos que possuem background e hover.
    nomes = [
        "Caixa",
        "Passadores"
    ]

    quantidade_de_cores = len(apresentacoes)
    comprimento = 190 * quantidade_de_cores
    altura = 70 + len(cores_disponiveis) * 30

    # Aqui já criamos nossa instância como sendo TopLevel
    jan = criando_janela(
        "Colorindo",
        (comprimento, altura),
        True
    )

    # Devemos criar frames para apresentar nossos pontos.
    def criando_frames() -> list[CTkFrame]:

        frames = []
        for i in range(0, quantidade_de_cores):
            fr = CTkFrame(
                jan,

                fg_color="#dde",
                bg_color="#dde",

                height=altura - 20,
                width=(comprimento // quantidade_de_cores) - 2 * 10,

                border_width=5,
                border_color="black",
            )
            fr.grid(
                row=0,
                column=i,
                padx=10,
                pady=10
            )

            frames.append(
                fr
            )

        return frames

    frames_possiveis = criando_frames()

    def apresentando_labels():

        for cada_frame, titulo in zip(frames_possiveis, apresentacoes):
            CTkLabel(
                cada_frame,

                text=titulo,
                text_color="black",

                bg_color="#dde",

                font=("Arial", 11)

            ).place(
                x=10,
                y=10
            )

    apresentando_labels()

    def apresentando_cores():
        # E aqui devemos ter nossas cores.

        def obtendo_variaveis() -> list[StringVar]:

            variaveis = []
            for i in range(0, quantidade_de_cores):
                p = StringVar(jan)
                p.set("")

                variaveis.append(
                    p
                )

            return variaveis

        variaveis_de_cor = obtendo_variaveis()

        # Devemos apresentar os radios button

        def apresentando_botoes():

            def obtendo_cor_do_usuario(rb: CTkRadioButton, frame: CTkFrame, var_da_cor_atual: StringVar):

                # Devemos apresentar uma entrada de dados.
                frase = "Cor Hexadecimal"
                codigo_da_cor = CTkEntry(
                    frame,

                    fg_color="white",
                    text_color="black",

                    placeholder_text=frase,
                    placeholder_text_color="gray",

                    height=20,
                    width=80,

                )
                codigo_da_cor.place(
                    x=rb.winfo_x() + 70,
                    y=rb.winfo_y()
                )

                def aplicando(event):
                    if codigo_da_cor.get() != frase and codigo_da_cor.get().startswith("#"):

                        # Queremos que:
                        var_da_cor_atual.set(codigo_da_cor.get())

                    else:
                        messagebox.showwarning(
                            "ERROR",
                            "Cor Inválida."
                        )

                codigo_da_cor.bind(
                    "<Return>", aplicando
                )

            for cada_frame, cor_do_momento in zip(frames_possiveis, variaveis_de_cor):

                # Em cada frame devemos ter todas as cores possíveis
                pos = 40
                for cor_portugues, cor_ingles in cores_disponiveis:
                    btn = CTkRadioButton(
                        cada_frame,

                        text_color="black",
                        text=cor_portugues,
                        font=("Arial", 11),

                        variable=cor_do_momento,
                        value=cor_ingles,

                        corner_radius=5,

                    )

                    btn.place(
                        x=10,
                        y=pos,
                    )

                    if cor_portugues == "Persona":
                        btn.bind(
                            "<Button-1>",
                            lambda event, rb=btn, frame=cada_frame, variavel=cor_do_momento: obtendo_cor_do_usuario(rb,
                                                                                                                    frame,
                                                                                                                    variavel))

                    pos += 30

        apresentando_botoes()

        def finalizador():
            # Aqui, devemos construir nossa lógica de mudança de cor.

            def fazendo_verificacoes(conjuntos_de_variaveis: list[StringVar]):
                # Devemos verificar se o maldito colocou uma cor válida.

                def eh_cor_valida(cor: str):

                    # Vamos tentar fazer uma conversão, caso não dê certo, a cor é inválida.
                    if len(cor) in [4, 7] or cor == "" or cor.isalpha():
                        return True

                    return False

                indice = 0
                for varia_cor in conjuntos_de_variaveis:
                    varia_cor = varia_cor.get()

                    if varia_cor == "persona":

                        conjuntos_de_variaveis[
                            indice
                        ].set("")

                        messagebox.showwarning(
                            "Rapaz",
                            "Você esqueceu de apertar ENTER na cor personalizada."
                        )

                    elif not eh_cor_valida(varia_cor):
                        conjuntos_de_variaveis[
                            indice
                        ].set("")

                        messagebox.showwarning(
                            "ERROR",
                            "Há uma Cor Inválida."
                        )

                    indice += 1

            fazendo_verificacoes(variaveis_de_cor)

            def obtendo_as_selecionadas() -> dict[str, dict[str, str]]:

                cores = {}

                # Agora, vamos adicionando o sanha.
                j: int = 0
                for i in range(1,  # Início das duplas
                               len(variaveis_de_cor) - 1,  # final das duplas
                               2,  # de dupla em dupla no caso
                               ):
                    cores[nomes[j]] = {
                        "background": variaveis_de_cor[i].get(),
                        "hover": variaveis_de_cor[i + 1].get(),
                    }

                    j += 1

                return cores

            cores_selecionadas = obtendo_as_selecionadas()

            # Vamos aplicar primeiro a cor da janela principal, afinal não há
            # nenhum botão com hover modificado nela.
            def aplicando_principal() -> None:

                cor_da_janela_principal: str = variaveis_de_cor[0].get()

                if cor_da_janela_principal == "":
                    return None

                for componente in lista_de_objetos_coloridos["Principal"]:
                    # Então temos algo para aplicar.
                    match componente.__class__.__name__:

                        case "Tk":
                            componente.configure(
                                bg=cor_da_janela_principal
                            )

                        case "CTkLabel":
                            componente.configure(
                                bg_color=cor_da_janela_principal
                            )

                        case "CTkButton":
                            componente.configure(
                                fg_color=cor_da_janela_principal
                            )

            aplicando_principal()

            # Agora, o restante.
            def aplicando_demais():

                """Note que mesmo que o usuário não queira alterar o background,
                ele pode querer mudar apenas o hover!"""

                for chave in lista_de_objetos_coloridos.keys():

                    if chave != "Principal":

                        # Vai ser mais eficiente se:
                        if cores_selecionadas[chave]["background"] != "":

                            # Vamos alterar então
                            for componente in lista_de_objetos_coloridos[chave]:

                                match componente.__class__.__name__:

                                    case "CTkSlider":
                                        componente: CTkSlider

                                        componente.configure(
                                            bg_color=cores_selecionadas[chave]["background"],
                                            fg_color=cores_selecionadas[chave]["background"]
                                        )

                                    case _:
                                        componente: CTkButton

                                        componente.configure(
                                            fg_color=cores_selecionadas[chave]["background"]
                                        )

                        if cores_selecionadas[chave]["hover"] != "":

                            for componente in lista_de_objetos_coloridos[chave]:

                                match componente.__class__.__name__:

                                    case "CTkButton":
                                        componente: CTkButton

                                        componente.configure(
                                            hover_color=cores_selecionadas[chave]["hover"]
                                        )

            aplicando_demais()

        def colocando_bota_finalizador():

            jan.geometry(f"{comprimento}x{altura + 50}")

            CTkButton(
                jan,

                text="Finalizar",
                text_color="black",

                bg_color="#dde",
                fg_color=COR_CAIXA,

                hover_color=COR_HOVER_CAIXA,

                width=400,
                height=30,

                command=finalizador,
            ).grid(
                row=1,
                column=0,
                columnspan=quantidade_de_cores,
                padx=5,
                pady=5
            )

        colocando_bota_finalizador()

    apresentando_cores()


def gerenciador_de_arquivos() -> None:
    """Função responsável por manipular todas as playlists e músicas."""

    # Vamos criar nossa função de gerenciar arquivos
    comp, alt = 400, 200
    pad_do_fr = 20
    janela = criando_janela(
        "Gerenciador",
        (comp, alt),
        True
    )

    def pegando_decisao_do_usuario(opcoes_de_decisao: list[str]) -> tuple[ttk.Combobox, Frame]:

        # Vamos criar um frame aqui dentro.
        frame_de_decisao = Frame(
            janela,
            bg="#dde",
            relief="solid",
            borderwidth=4,
        )

        comp_fr = comp - 2 * pad_do_fr
        alt_fr = alt - 2 * pad_do_fr
        frame_de_decisao.place(
            x=pad_do_fr,
            y=pad_do_fr,
            width=comp_fr,
            height=alt_fr,
        )

        # Vamos colocar um combobox no meio do cara.
        cb = ttk.Combobox(
            frame_de_decisao,
            state="readonly",
            values=opcoes_de_decisao,
            width=20,
        )
        cb.set(opcoes_de_decisao[0])
        cb.grid(
            row=0,
            column=0,
            padx=(comp_fr - cb.winfo_reqwidth()) / 2,
            pady=(alt_fr - cb.winfo_reqheight()) / 2
        )

        return cb, frame_de_decisao

    cb_decisoes, fr_decisao = pegando_decisao_do_usuario(
        [
            "Insira Sua Decisão",
            "Adicionar Música",
            "Apagar Playlist",
            "Criar Playlist",
            "Loops de Música",
            "Ver Ranking de Músicas"
        ]
    )

    def apresentando_apagar_playlist():
        """Função responsável por criar outro frame direcionado para sua respectiva decisão,
        remodelando a janela se necessário."""

        # Vamos criar um frame e aplicar aqui
        fr = Frame(
            janela,
            relief="solid",
            borderwidth=4,
            bg="#dde",
        )
        fr.place(
            x=pad_do_fr,
            y=fr_decisao.winfo_y() + fr_decisao.winfo_reqheight() + 10,
            width=comp - 2 * pad_do_fr,
            height=fr_decisao.winfo_reqheight()
        )

        # Também devemos aumentar o tamanho da tela.
        janela.geometry(f"{comp}x{(2 * fr_decisao.winfo_reqheight()) + (3 * pad_do_fr)}")
        # Não precisa ser tão responsivo assim

        # Como queremos apagar uma playlist, devemos ser capazes de sanhar.
        Label(
            fr,
            bg="#dde",
            text="Selecione a Playlist que deseja apagar:"
        ).grid(
            row=0,
            column=0,
            padx=10,
            pady=10,
        )

        # Um novo combobox apresentando as playlists que existem
        cb_pl = ttk.Combobox(
            fr,
            values=listdir(
                caminhos_possiveis["Músicas"]
            ),
            width=13,
            state="readonly"
        )

        cb_pl.grid(
            row=0,
            column=1,
            padx=5,
            pady=10
        )

        def apresentando_botao_de_apagar():
            # Vamos colocar um botão sanhudo
            CTkButton(
                fr,
                text="Destruir",
                text_color="black",

                fg_color=COR_CAIXA,
                hover_color=COR_HOVER_CAIXA,

                command=lambda: apagando_playlist(cb_pl),

                height=50,

            ).place(
                x=110,
                y=70,
            )

        # Assim que selecionarmos alguma, um botão com a chance de apagarmos ela
        # Deve surgir
        cb_pl.bind(
            "<<ComboboxSelected>>",
            lambda event: apresentando_botao_de_apagar()
        )

    def apresentando_criar_playlist():
        """Função responsável por apresentar a interface ligada a criação de playlists"""

        fr = Frame(
            janela,
            bg="#dde",

            relief="solid",
            borderwidth=4,
        )
        fr.place(
            x=pad_do_fr,
            y=fr_decisao.winfo_y() + fr_decisao.winfo_reqheight() + 10,
            width=comp - 2 * pad_do_fr,
            height=70
        )

        novo_comp = 290
        janela.geometry(
            f"{comp}x{novo_comp}"
        )

        # Vamos apenas colocar um sanhudo dentro e acabou!
        variavel_de_ajuda = StringVar(fr)
        variavel_de_ajuda.set(
            ""
        )
        Label(
            fr,
            textvariable=variavel_de_ajuda,
            bg="#dde",
        ).place(
            x=190,
            y=25,
        )

        frase_ajuda = "Insira o Nome da Nova Playlist"
        nome_da_nova_playlist = Entry(
            fr,
            fg="gray"
        )
        nome_da_nova_playlist.insert(0, frase_ajuda)
        nome_da_nova_playlist.place(
            x=10,
            y=25,
            width=170
        )

        def desetando(event):
            if nome_da_nova_playlist.get() == frase_ajuda:
                # Vamos limpar
                nome_da_nova_playlist.delete(0, "end")
                nome_da_nova_playlist.config(fg="black")
                variavel_de_ajuda.set(
                    "Pressione Enter Para Criá-la"
                )

        def setando(event):
            if nome_da_nova_playlist.get() == "":
                nome_da_nova_playlist.insert(0, frase_ajuda)
                nome_da_nova_playlist.config(
                    fg="gray"
                )
                variavel_de_ajuda.set(
                    ""
                )

        nome_da_nova_playlist.bind(
            "<FocusIn>", desetando
        )

        nome_da_nova_playlist.bind(
            "<FocusOut>", setando
        )

        nome_da_nova_playlist.bind(
            "<Return>", lambda event: criando_playlist(nome_da_nova_playlist, frase_ajuda)
        )

    def apresentando_adicionar_musica():
        """Função Responsável por apresentar a interface de criação de música e de
        puxar a função responsável por efetivamente baixar a música."""

        fr = Frame(
            janela,
            relief="solid",
            borderwidth=4,

            bg="#dde"
        )
        fr.place(
            x=pad_do_fr,
            y=fr_decisao.winfo_y() + fr_decisao.winfo_reqheight() + 10,
            width=comp - 2 * pad_do_fr,
            height=fr_decisao.winfo_reqheight()
        )

        # Redimensionando a janela
        nova_alt = 390
        janela.geometry(
            f"{comp}x{nova_alt}"
        )

        # Devemos disponibilizar um ComboBox pedindo para
        # Escolhermos a playlist que a música vai entrar.
        pedido_de_entrada = "Escolha Playlist de Entrada"

        def escolhendo_playlist() -> ttk.Combobox:
            """Função Responsável por criar um combobox que vai pegar
            a playlist de entrada da música."""

            cb_playlist = ttk.Combobox(
                fr,
                values=listdir(
                    caminhos_possiveis[
                        "Músicas"
                    ]
                ),
                state="readonly",
            )
            cb_playlist.set(
                pedido_de_entrada
            )
            cb_playlist.place(
                x=10,
                y=10,
                width=180,
            )

            return cb_playlist

        cb_pl = escolhendo_playlist()

        def pegando_nome_link(event):
            # Assim que algo for escolhido, devemos ter nossas
            # coisas em condições para pegar as informções.
            if cb_pl.get() == pedido_de_entrada:
                return None

            # Então, devemos continuar
            # Devemos apresentar um Entry pedindo o nome da música,
            # E outro pedindo o link da música.

            def obtendo_nome() -> CTkEntry:
                """Coloca o entry do nome"""
                nome = CTkEntry(
                    fr,
                    fg_color="white",
                    text_color="black",

                    placeholder_text="Insira o Nome da Música",
                    placeholder_text_color="gray",

                    corner_radius=0,

                    height=20,
                    width=170
                )
                nome.place(
                    x=10,
                    y=50
                )

                return nome

            nome_da_musica = obtendo_nome()

            def obtendo_link() -> CTkEntry:
                nome = CTkEntry(
                    fr,
                    fg_color="white",
                    text_color="black",

                    placeholder_text="Insira o Link da Música",
                    placeholder_text_color="gray",

                    corner_radius=0,

                    height=20,
                    width=230
                )
                nome.place(
                    x=10,
                    y=80
                )

                return nome

            link_da_musica = obtendo_link()

            def confirmando() -> str | None:

                se_possui_nome: bool = nome_da_musica.get() != ""
                se_link_valido: bool = link_da_musica.get().startswith(
                    "https:"
                )

                if se_link_valido and se_possui_nome:

                    nome_musica = nome_da_musica.get() if nome_da_musica.get().endswith(
                        ".mp3") else nome_da_musica.get() + ".mp3"
                    nome_playlist = cb_pl.get()

                    if baixando_musica(
                            nome_playlist,
                            nome_musica.replace(".mp3", ''),
                            link_da_musica.get()
                    ):
                        # Devemos atualizar oq vai acontecer.

                        atualizando_apos_download(
                            nome_playlist,
                            nome_musica,
                        )

                        # Limpando os espaços
                        nome_da_musica.delete(0, "end")
                        link_da_musica.delete(0, "end")

                        return None

                return messagebox.showwarning(
                    "Eita",
                    "Entradas Inválidas"
                )

            # Vamos colocar um botão no sanha
            CTkButton(
                fr,

                text="Confirmar",
                text_color="black",

                fg_color=COR_CAIXA,
                hover_color=COR_HOVER_CAIXA,

                command=confirmando,

            ).place(
                x=10,
                y=120
            )

        # Vamos bindar para assim que algo for escolhido, a apresentação inicia.
        cb_pl.bind(
            "<<ComboboxSelected>>",
            pegando_nome_link
        )

    def apresentando_ranking():
        comp_total = 200
        fr = CTkFrame(
            janela,

            fg_color="#dde",
            border_width=4,
            border_color="black",

            width=comp_total,
            height=fr_decisao.winfo_reqheight()
        )

        fr.place(
            x=70,
            y=fr_decisao.winfo_y() + fr_decisao.winfo_reqheight() + 10,
        )

        # Redimensionando a janela
        nova_alt = 390
        janela.geometry(
            f"{comp}x{nova_alt}"
        )

        lista_ordenada, medidor = ranking_de_musicas()

        # Devemos colocar cada uma delas dentro do frame
        def aplicando_label(texto, row: int, coluna: int):
            Label(
                fr,
                text=texto,
                bg='#dde'
            ).grid(
                row=row,
                column=coluna,
                padx=10,
                pady=10
            )

        aplicando_label(
            "Músicas",
            0,
            0
        )

        aplicando_label(
            f"Tempo Total({medidor})",
            0,
            1
        )

        # Agora, vamos colocar as informações
        linha = 1
        # Devemos obter uma lista ordenada de cada música e da sua respectiva quantidade.
        for musica, tempo in lista_ordenada:
            aplicando_label(
                musica,
                linha,
                0,
            )
            aplicando_label(
                tempo,
                linha,
                1,
            )
            linha += 1

    def apresentando_fila_de_musicas():
        comp_total = 300
        fr = CTkFrame(
            janela,

            fg_color="#dde",
            border_width=4,
            border_color="black",

            width=comp_total,
            height=80,
        )

        fr.place(
            x=50,
            y=fr_decisao.winfo_y() + fr_decisao.winfo_reqheight() + 10,
        )

        # Redimensionando a janela
        nova_alt = 300
        janela.geometry(
            f"{comp}x{nova_alt}"
        )

        # Vamos dispor um combobox no centro para pegar a decisão
        possibilidades = [
            "Infinitas",
            "1 Vez",
            "2 vezes",
        ]
        cb = ttk.Combobox(
            fr,
            values=possibilidades,
        )
        cb.place(
            x=80,
            y=40,
        )

        cb.bind(
            "<<ComboboxSelected>>",
            lambda event: definindo_loops(
                cb.get()
            )
        )

        Label(
            fr,
            text="Tente digitar 'x vezes', apertar Enter e assim será.",

            bg="#dde",
        ).place(
            x=20,
            y=10
        )





    """Caso desejemos colocar uma nova feature,
    basta criarmos a função aqui, colocarmos a opção da função
    dentro do combobox de decisão e a própria função
    no Dicionário de Decisões"""

    # Apenas para não termos aquela merda de if's
    Dicionario_de_Decisoes = {
        "Apagar Playlist": apresentando_apagar_playlist,
        "Criar Playlist": apresentando_criar_playlist,
        "Adicionar Música": apresentando_adicionar_musica,
        "Ver Ranking de Músicas": apresentando_ranking,
        "Loops de Música": apresentando_fila_de_musicas,
    }

    def apresentar_decisao(decisao_escolhida: str) -> None:
        # Dependo da decisão escolhida, vamos ter funções a serem executadas.

        # Vamos verificar se há um frame na janela principal
        def tratando_decisao():
            """Caso haja outro frame, quer dizer que uma decisão já foi tomada e por isso
            devemos apagá-lo para construir outro frame que corresponde a outra decisão."""

            if len(janela.winfo_children()) != 1:
                # Devemos pegar o último e destruí-lo.
                janela.winfo_children()[-1].destroy()
                janela.geometry(
                    f"{comp}x{alt}"
                )

        tratando_decisao()
        # Agora, estamos livres para tomar nossa decisão.

        if decisao_escolhida.startswith("Ins"):
            return None

        Dicionario_de_Decisoes[
            decisao_escolhida
        ]()

    # Vamos bindar com nossas funções
    cb_decisoes.bind(
        "<<ComboboxSelected>>", lambda event: apresentar_decisao(cb_decisoes.get())
    )


def configurador() -> None:
    """Função responsável por criar uma interface na qual o usuário vai poder manipular as
    posições e dimensões de cada objeto da interface principal."""

    comp, alt = 450, 400
    janela = criando_janela(
        "Configurador",
        (comp, alt),
        True
    )

    # Vamos pensar:
    """Note que não é interessante que os objetos dentro da caixa de ferramentas
    sejam alteradas, compreende? Afinal, é tudo em grid. 
    É melhor que alteremos posições relativas aos passadores ou aos comboboxs.
    
    Levando isso em consideração, podemos ver que é melhor até que nem disponibilizemos
    tantas formas diferentes. 
    
    O que nos leva a:"""

    def criando_frames(pad: int) -> tuple[CTkFrame, CTkFrame]:
        """Função responsável por dispor nossos frames para podermos ter grids boas"""

        def criando_frame_geral() -> CTkFrame:
            """Vamos criar um frame geral!"""

            fr_geral = CTkFrame(
                janela,

                fg_color="#dde",

                border_color="black",
                border_width=4,

                width=comp - 2 * pad,
                height=alt - 2 * pad,

            )
            fr_geral.place(
                x=pad,
                y=pad,
            )

            return fr_geral

        frame_geral = criando_frame_geral()

        # Vamos criar os frames respectivos

        pulo_em_x = 140

        def fr_de_elementos(cor: str, pad_rel: int) -> CTkFrame:
            fr = CTkFrame(
                frame_geral,

                fg_color=cor,

                border_width=0,
                border_color=cor,

                height=frame_geral.winfo_reqheight() - 2 * pad_rel
            )

            fr.place(
                x=pad_rel,
                y=pad_rel,
            )

            return fr

        def fr_de_componentes(cor: str, pad_rel: int) -> CTkFrame:
            fr = CTkFrame(
                frame_geral,

                fg_color=cor,

                border_width=0,
                border_color=cor,

                width=200,
                height=frame_geral.winfo_reqheight() - 2 * pad_rel
            )

            fr.place(
                x=2 * pad_rel + pulo_em_x,
                y=pad_rel,
            )

            return fr

        def aplicando_frames(cor: str, pad_rel: int) -> tuple[CTkFrame, CTkFrame]:
            return (
                fr_de_elementos(
                    cor,
                    pad_rel
                ),
                fr_de_componentes(
                    cor,
                    pad_rel
                ),
            )

        return aplicando_frames(
            "#dde",
            pad
        )

    frame_de_elementos, frame_de_componentes = criando_frames(
        10
    )

    def aplicando_elementos(elementos: list[str]) -> None:
        """Função que vai dispor os nomes de cada elemento em que é possível modificação."""
        Label(
            frame_de_elementos,

            text="Elementos:",

            bg="#dde"
        ).grid(
            row=0,
            column=0,
            padx=2,
            pady=12,
        )
        for indice, elemento in enumerate(elementos):
            Label(
                frame_de_elementos,

                text=elemento,

                bg="#dde",
            ).grid(
                row=indice + 1,
                column=0,
                padx=0,
                pady=7,
            )

    aplicando_elementos(
        [
            "Janela Principal",
            "Label de Playlists",
            "Caixa de Playlists",
            "Label de Musicas",
            "Caixa de Musicas",
            "Passador para Próximo",
            "Passador para Anterior",
            "Botão de Atualizar",
            "Caixa de Ferramentas",
        ]
    )

    def aplicando_nomes_de_componentes(elementos: list[str]) -> None:
        """Função Responsável por dispor os títulos de cada componente
        possível de ser transformada."""

        for indice, elemento in enumerate(elementos):
            Label(
                frame_de_componentes,

                text=elemento,

                bg=COR_JANELA
            ).grid(
                row=0,
                column=indice,
                padx=20,
                pady=10
            )

    aplicando_nomes_de_componentes(
        [
            "X",
            "Y",
            "Comp",
            "Alt"
        ]
    )

    def aplicando_informacoes_de_cada_elemento(elementos: list[list[int]]) -> None:
        """Vamos criar os spinboxs de cada objeto para podermos atualizá-los."""

        objetos = list(objetos_globais.values())
        for linha, conjunto_de_componentes in enumerate(elementos):
            for coluna, valor in enumerate(conjunto_de_componentes):

                if valor != -1:
                    """
                    Havíamos pensado na ideia de limitar o spinbox pelas dimensões da janela, entretanto, 
                    note que as próprias dimensões da janela ficariam limitadas. Isso seria fácil de consertar,
                    entretanto, note que conforme desejassemos aumentar a geometria de outros widgets, estaríamos 
                    limitados pelas dimensões atuais da janela.
                    
                    A melhor forma seria limitar usando os valores instântaneos dos spinboxs da janela. Entretanto,
                    isso significaria que devessemos guardar os valores em uma lista.
                    Apenas colocando 1000, podemos ter uma ideia melhor né sanhudo.
                    """

                    sb = Spinbox(
                        frame_de_componentes,

                        from_=0,

                        to=1000,

                        width=4,
                    )
                    sb.grid(
                        row=linha + 1,
                        column=coluna,
                        padx=10,
                        pady=8,
                    )

                    sb["command"] \
                        = lambda elem=objetos[linha], spinbox=sb, index=coluna, index_obj=linha: transformador(elem,
                                                                                                               spinbox,
                                                                                                               index,
                                                                                                               index_obj)

                    sb.delete(0, 'end'),
                    sb.insert(0, str(valor))

                    # Note que podemos tanto ir pelo modificador do spinbox quanto
                    # digitar manualmente
                    sb.bind(
                        "<Return>",
                        lambda event, elem=objetos[linha], spinbox=sb, index=coluna, index_obj=linha: transformador(
                            elem, spinbox, index, index_obj)
                    )

    aplicando_informacoes_de_cada_elemento(
        obtendo_informacoes_de_geometria()
    )

    def possibilitando_volta_a_fabrica():
        # Aumentar o tamanho da janela
        janela.geometry(
            f"{comp}x{alt + 30}"
        )

        # Agora colocando o botão
        CTkButton(
            janela,

            text_color="black",
            text="Voltar À Geometria Padrão",

            bg_color="#dde",
            fg_color=COR_CAIXA,
            hover_color=COR_HOVER_CAIXA,

            command=voltando_a_fabrica,
        ).place(
            x=140,
            y=395
        )

    possibilitando_volta_a_fabrica()
