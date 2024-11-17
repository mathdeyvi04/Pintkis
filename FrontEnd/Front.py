from Aplicativos.Tkinter.Reprodutor_Musical_Pintkis.FrontEnd.FuncoesFrontEnd import *


def pintkis():
    try:
        # Vamos iniciar o pygame
        init()
        mixer.init()

        # Vamos criar a janela
        janela = criando_janela(
            "PintKis",
            dicionario_de_geometria["Principal"]
        )

        # Devemos construir as coisas básicas!
        coisas_basicas(janela, dicionario_de_geometria)

        # Vamos construir nossa caixa de ferramentas
        caixa_de_ferramentas(janela, dicionario_de_geometria)

        # Por segurança, vamos setar sempre bem baixo
        volumando(
            variaveis_globais["VALOR_DE_SOM_SEGURO"]
        )

        janela.mainloop()

    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"Erro detectado: {e}")
    finally:
        print("Executei o encerrador.")
        # Para encerrarmos tudo com segurança.
        # Aqui devemos rodar cada uma das atualizações que devemos ter.
        encerrador()


if __name__ == '__main__':
    pintkis()
