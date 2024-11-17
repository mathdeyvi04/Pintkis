from customtkinter import *  # Importação de Interface
from tkinter import *  # Importação de Interface
from tkinter import ttk  # Importação de Interface

from os import listdir, mkdir, remove  # Para manipularmos os arquivos
from PIL import Image  # Para colocarmos imagens dentro dos botões
from send2trash import send2trash  # Para levar coisas à lixeira
from pytube import YouTube  # Para iniciarmos o download de uma música
from moviepy.editor import AudioFileClip  # Para as conversões de mp4 para mp3

from pygame import init, mixer  # Para manipularmos música
from pprint import pprint  # Para podermos visualizar melhor estruturas
from tkinter import messagebox  # Para enviarmos mensagens ao usuário
from time import time  # Para o contador


def definindo_caminhos() -> dict[str: str]:
    """Função responsável por criarmos nossos caminhos para cada área. Extremamente Importante.
    """
    CAMINHO_TOTAL = r"C:\Users\deyvi\Documents\ImperioPy\Aplicativos\Tkinter\ReprodutorMusicalPintKis"

    return {
        "Músicas": CAMINHO_TOTAL + r"\BackEndCompleto\Musicas",

        "Base_Dados": CAMINHO_TOTAL + r"\BackEndCompleto\dados.txt",

        "Figuras": CAMINHO_TOTAL + r"\BackEndCompleto\Figuras",

        "Geometrico": CAMINHO_TOTAL + r"\BackEndCompleto\geometria.txt",

        "ONDE_MP4_VAI": CAMINHO_TOTAL
    }


caminhos_possiveis = definindo_caminhos()

# Lista de Objetos que Podem a cor alterada.
lista_de_objetos_coloridos = {}

# Objetos Globais
objetos_globais = {}

# Vamos salvar as músicas tocadas.
musicas_tocadas_na_sessao = {
    # Vamos ter "música" = [ [tempo_total] [tempo_inicial_que_ela_começou] ]
}

# Criamos para poder ter variáveis globais mesmo podem alterá-las
variaveis_globais = {
    # Para não precisarmos percorrer toda a estrutura procurando a informação.
    "ULTIMA_MUSICA_TOCADA": None,

    # Para não precisarmos comparar duas matrizes em cada término de sessão.
    "HOUVE_MUDANÇA_GEOMETRICA": False,

    # Para controlarmos quantas vezes vamos ouvir uma mesma música.
    "LOOPS_DE_MUSICA": -1,

    # Para iniciarmos cada música com a segurança que não explodir nossos ouvidos.
    "VALOR_DE_SOM_SEGURO": 10,

    # Para podermos ver informações preciosas
    "VISUALIZAR_INFORMAÇÕES": False,
}

if variaveis_globais["VISUALIZAR_INFORMAÇÕES"]:
    print("\033[1m\033[7m")


def obtendo_cores() -> list[str]:
    """Função responsável por sempre manter o arquivo de dados existente e com as cores
    presentes."""
    try:

        p = open(caminhos_possiveis["Base_Dados"], 'r', encoding="utf-8")
        info_de_cores = p.readlines()[0].replace("\n", '').split("=")[1].split("_")
        p.close()

        return info_de_cores

    except:
        # Ou o arquivo não existe, ou sei lá o que aconteceu

        # Vamos criar o arquivo e colocar esses dados nele.
        p = open(caminhos_possiveis["Base_Dados"], 'x', encoding="utf-8")

        p.write("cores=#dde_#fab4af_#fcd0cc_#3B8ED0_#36719F")

        p.close()

        # Afinal, baseamos nosso projeto pensando haver sempre algo nesse arquivo de merda.

        return [
            "#dde",
            "#fab4af",
            "#fcd0cc",
            "#3B8ED0",
            "#36719F",
        ]


COR_JANELA, COR_CAIXA, COR_HOVER_CAIXA, COR_PASSADOR, COR_HOVER_PASSADOR = obtendo_cores()
