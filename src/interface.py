from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
from dog.dog_interface import DogPlayerInterface
from dog.dog_actor import DogActor
from constantes import *
from ObjetoInterface import ObjetoInterface
from PIL import Image, ImageTk
from jogo import Jogo, Estado
from imageminterface import ImagemInterface


class InterfaceGraficaJogador(DogPlayerInterface):

    def __init__(self) -> None:
        super().__init__()

        self.lado_borda_frame_principal = int(ALTURA * 0.85)
        self.lado_frame_principal = int(self.lado_borda_frame_principal * 0.98)
        self.lado_celula = self.lado_frame_principal // 10 - int(0.0030 * self.lado_frame_principal)

        self.matriz_labels_pecas = []
        self.matriz_labels_pecas_esquerda = []
        self.matriz_labels_pecas_direita = []

        self.frame_principal = None
        self.borda_frame_principal = None
        self.borda_frame_pecas_esquerda = None
        self.frame_pecas_esquerda = None
        self.borda_frame_pecas_direita = None
        self.frame_pecas_direita = None
        self.frameMensagem = None
        self.labelMensagem = None
        self.label_nome_adversario = None
        self.label_turno = None

        self.janela_principal = Tk()
        self.init_tkinter()

        self.imagens = self.ler_imagens()

        self.barra_menu = None
        self.criar_menu()
        self.desenhar_janela()

        self.jogo = Jogo()
        self.jogo.inicializar()

        # dog
        player_name = simpledialog.askstring(title="Player Identification", prompt="Qual o seu nome?")
        self.dog_server_interface = DogActor()
        message = self.dog_server_interface.initialize(player_name, self)
        messagebox.showinfo(message=message)

        self.janela_principal.mainloop()

    def init_tkinter(self):
        self.janela_principal.title("Combate")
        self.janela_principal.geometry(f"{LARGURA}x{ALTURA}")
        self.janela_principal.resizable(False, False)
        self.janela_principal.configure(bg="gray")

    def desenhar_janela(self):
        self.desenhar_frame_principal()
        self.desenhar_celulas()
        self.desenhar_pecas_direita()
        self.desenhar_pecas_esquerda()
        self.desenhar_mensagem("Clique em iniciar partida para jogar!")
        self.desenhar_turno()

    def criar_menu(self):
        self.barra_menu = Menu(self.janela_principal)
        self.janela_principal.config(menu=self.barra_menu)
        self.barra_menu.add_command(label="Iniciar partida",
                                    command=lambda: self.start_match())
        self.barra_menu.add_command(label="Alocar rapidamente",
                                    command=lambda: self.alocar_rapidamente())
        self.barra_menu.add_command(label="Terminar preparação",
                                    command=lambda: self.terminar_preparacao())

    def desenhar_frame_principal(self):
        self.borda_frame_principal = Frame(self.janela_principal,
                                           bg="black")
        self.borda_frame_principal.place(anchor="center",
                                         width=int(self.lado_borda_frame_principal),
                                         height=int(self.lado_borda_frame_principal),
                                         x=LARGURA // 2,
                                         y=ALTURA // 2 + ALTURA // 20)

        self.frame_principal = Frame(self.janela_principal,
                                     bg="black")
        self.frame_principal.place(anchor="center",
                                   width=self.lado_frame_principal,
                                   height=self.lado_frame_principal,
                                   x=LARGURA // 2,
                                   y=ALTURA // 2 + ALTURA // 20)

    def desenhar_celulas(self):
        for i in range(10):
            linha_matriz = []
            for j in range(10):

                if (i == 4 or i == 5) and (j == 2 or j == 3 or j == 6 or j == 7):
                    cor = "blue"
                else:
                    cor = "green"

                label_posicao = Label(self.frame_principal,
                                      bg=cor)
                label_posicao.place(x=j * self.lado_frame_principal // 10 + self.lado_frame_principal // 20,
                                    y=i * self.lado_frame_principal // 10 + self.lado_frame_principal // 20,
                                    width=self.lado_celula,
                                    height=self.lado_celula,
                                    anchor="center"
                                    )
                linha_matriz.append(label_posicao)
                label_posicao.bind("<Button-1>", lambda event, linha=i, coluna=j, objeto=ObjetoInterface.TABULEIRO.value: self.click(event, linha, coluna, objeto))
            self.matriz_labels_pecas.append(linha_matriz)

    def desenhar_pecas_esquerda(self):
        self.borda_frame_pecas_esquerda = Frame(self.janela_principal,
                                                bg="black",
                                                )
        self.borda_frame_pecas_esquerda.place(anchor="e",
                                              width=2 * self.lado_celula + int(
                                                  0.0125 * self.lado_borda_frame_principal),
                                              height=int(
                                                  0.6 * self.lado_borda_frame_principal
                                                  + 0.0125 * self.lado_borda_frame_principal),
                                              x=LARGURA // 2 - self.lado_borda_frame_principal // 2,
                                              y=ALTURA // 2 + ALTURA // 20)

        self.frame_pecas_esquerda = Frame(self.janela_principal,
                                          bg="black")
        self.frame_pecas_esquerda.place(anchor="e",
                                        width=2 * self.lado_celula,
                                        height=int(0.6 * self.lado_frame_principal),
                                        x=LARGURA // 2 - self.lado_borda_frame_principal // 2 - int(
                                            0.02 * self.lado_celula),
                                        y=ALTURA // 2 + ALTURA // 20)

        for i in range(6):
            linha_matriz = []
            for j in range(2):
                if j == 0:
                    label_posicao = Label(self.frame_pecas_esquerda,
                                          bg="white",
                                          text=self.criar_texto_peca(i, quantidade_inicial[i]),
                                          font="arial 10",
                                          width=self.lado_celula,
                                          height=self.lado_celula)
                else:
                    label_posicao = Label(self.frame_pecas_esquerda,
                                          bg="white",
                                          image=self.imagens[i],
                                          width=self.lado_celula,
                                          height=self.lado_celula)

                label_posicao.place(x=j * self.lado_celula,
                                    y=i * self.lado_frame_principal // 10,
                                    width=self.lado_celula,
                                    height=self.lado_celula,
                                    anchor="nw"
                                    )
                linha_matriz.append(label_posicao)
                label_posicao.bind("<Button-1>", lambda event, linha=i, coluna=j, objeto=ObjetoInterface.PECAS_ESQUERDA.value: self.click(event, linha, coluna, objeto))

            self.matriz_labels_pecas_esquerda.append(linha_matriz)

    def desenhar_pecas_direita(self):
        self.borda_frame_pecas_direita = Frame(self.janela_principal,
                                               bg="black")
        self.borda_frame_pecas_direita.place(anchor="w",
                                             width=2 * self.lado_celula + int(0.0125 * self.lado_borda_frame_principal),
                                             height=int(
                                                 0.6 * self.lado_borda_frame_principal +
                                                 0.0125 * self.lado_borda_frame_principal),
                                             x=LARGURA // 2 + self.lado_borda_frame_principal // 2,
                                             y=ALTURA // 2 + ALTURA // 20)

        self.frame_pecas_direita = Frame(self.janela_principal,
                                         bg="black")
        self.frame_pecas_direita.place(anchor="w",
                                       width=2 * self.lado_celula,
                                       height=int(0.6 * self.lado_frame_principal),
                                       x=LARGURA // 2 + self.lado_borda_frame_principal // 2 + int(
                                           0.02 * self.lado_celula),
                                       y=ALTURA // 2 + ALTURA // 20)

        for i in range(6):
            linha_matriz = []
            for j in range(2):
                if j == 1:
                    label_posicao = Label(self.frame_pecas_direita,
                                          bg="white",
                                          text=self.criar_texto_peca(6 + i, quantidade_inicial[6 + i]),
                                          font="arial 10",
                                          width=self.lado_celula,
                                          height=self.lado_celula)
                else:
                    label_posicao = Label(self.frame_pecas_direita,
                                          bg="white",
                                          image=self.imagens[6 + i],
                                          width=self.lado_celula,
                                          height=self.lado_celula)

                label_posicao.place(x=j * self.lado_celula,
                                    y=i * self.lado_frame_principal // 10,
                                    width=self.lado_celula,
                                    height=self.lado_celula,
                                    anchor="nw"
                                    )
                linha_matriz.append(label_posicao)
                label_posicao.bind("<Button-1>", lambda event, linha=i, coluna=j, objeto=ObjetoInterface.PECAS_DIREITA.value: self.click(event, linha, coluna, objeto))
            self.matriz_labels_pecas_direita.append(linha_matriz)

    def desenhar_mensagem(self, mensagem):

        self.frameMensagem = Frame(self.janela_principal,
                                   bg="gray"
                                   )
        self.frameMensagem.place(anchor="n",
                                 width=int(LARGURA * 0.95),
                                 height=int(self.lado_borda_frame_principal // 8),
                                 x=LARGURA // 2,
                                 y=int(0.01 * ALTURA))

        self.labelMensagem = Label(self.frameMensagem,
                                   bg="gray",
                                   text=mensagem,
                                   font="arial 25"
                                   )
        self.labelMensagem.place(anchor="nw",
                                 width=int(LARGURA * 0.95),
                                 height=int(self.lado_borda_frame_principal // 8),
                                 x=0,
                                 y=0
                                 )

    def desenhar_nome_adversario(self, nome: str):

        self.label_nome_adversario = Label(self.janela_principal,
                                           bg="gray",
                                           text=f"Adversário:\n{nome}",
                                           font="arial 15"
                                           )
        self.label_nome_adversario.place(anchor="sw",
                                         width=int(LARGURA * 0.23),
                                         height=int(LARGURA * 0.05),
                                         x=0,
                                         y=ALTURA)

    def desenhar_turno(self):

        self.label_turno = Label(self.janela_principal,
                                 bg="gray",
                                 text="",
                                 font="arial 15")
        self.label_turno.place(anchor="sw",
                               width=int(LARGURA * 0.23),
                               height=int(LARGURA * 0.05),
                               x=int(LARGURA * 0.77),
                               y=ALTURA)

    def click(self, event, i, j, objeto):
        if objeto == ObjetoInterface.TABULEIRO.value:
            self.selecionar_posicao(i, j, False)
        elif objeto == ObjetoInterface.PECAS_ESQUERDA.value:
            self.selecionar_posicao(i, 0, True)
        elif objeto == ObjetoInterface.PECAS_DIREITA.value:
            self.selecionar_posicao(i, 1, True)

    def ler_imagens(self):
        imagens = []
        for i in range(13):
            imagem = Image.open(f"./resources/images/{i}.png").convert("RGBA")
            imagem = imagem.resize((int(self.lado_celula * 0.9), int(self.lado_celula * 0.9)), Image.ANTIALIAS)
            imagens.append(ImageTk.PhotoImage(imagem))
        return imagens

    def criar_texto_peca(self, peca, quantidade):
        return nome_peca[peca] + "\nF: " + str(peca) + "\nD: " + str(quantidade)

    def start_match(self) -> None:
        estado = self.jogo.get_estado()
        if estado == Estado.NAO_COMECOU or estado == Estado.FIM_DE_JOGO:
            start_status = self.dog_server_interface.start_match(2)
            code = start_status.get_code()
            message = start_status.get_message()

            if code == "0" or code == "1":
                messagebox.showinfo(message=message)
            elif code == "2":
                self.jogo.comecar_partida()
                messagebox.showinfo(message=message)
                players = start_status.get_players()
                self.desenhar_nome_adversario(players[1][0])
                status = self.jogo.obter_status()
                self.atualizar_interface(status)
        else:
            messagebox.showinfo(message="Você já está em uma partida.")

    def receive_start(self, start_status) -> None:
        self.jogo.receber_inicio()
        message = start_status.get_message()
        messagebox.showinfo(message=message)
        players = start_status.get_players()
        self.desenhar_nome_adversario(players[1][0])
        status = self.jogo.obter_status()
        self.atualizar_interface(status)

    def receive_move(self, a_move):
        self.jogo.receber_jogada(a_move)
        status = self.jogo.obter_status()
        self.atualizar_interface(status)

    def receive_withdrawal_notification(self):
        self.jogo.receber_desistencia()
        status = self.jogo.obter_status()
        self.atualizar_interface(status)

    def selecionar_posicao(self, linha: int, coluna: int, peca_fora_tabuleiro: bool) -> None:
        jogada = self.jogo.selecionar_posicao(linha, coluna, peca_fora_tabuleiro)
        if jogada != {}:
            self.dog_server_interface.send_move(jogada)
        status = self.jogo.obter_status()
        self.atualizar_interface(status)

    def terminar_preparacao(self) -> None:
        estado = self.jogo.get_estado()
        if estado == Estado.PREPARACAO:
            jogada = self.jogo.terminar_preparacao()
            if jogada != {}:
                self.dog_server_interface.send_move(jogada)
                status = self.jogo.obter_status()
                self.atualizar_interface(status)
            else:
                messagebox.showinfo(message="Você não posicionou todas as suas peças.")
        else:
            messagebox.showinfo(message="Você não está em preparação.")

    def alocar_rapidamente(self) -> None:
        estado = self.jogo.get_estado()
        if estado == Estado.PREPARACAO:
            self.jogo.alocar_rapidamente()
            status = self.jogo.obter_status()
            self.atualizar_interface(status)
        else:
            messagebox.showinfo(message="Você não está em preparação.")

    def atualizar_interface(self, status: ImagemInterface) -> None:
        for i in range(10):
            for j in range(10):
                if not ((i == 4 or i == 5) and (j == 2 or j == 3 or j == 6 or j == 7)):  # Os lagos nunca atualizam
                    label = self.matriz_labels_pecas[i][j]
                    forca = status.tabuleiro[i][j]
                    selecionado = status.posicoes_selecionada[i][j]

                    if selecionado == 1:
                        label.config(bg="red")
                    elif selecionado == 2:
                        label.config(bg="yellow")
                    else:
                        label.config(bg="green")

                    if forca > -1:
                        label.config(image=self.imagens[forca])
                    else:
                        label.config(image="")

        peca = status.peca_fora_tabuleiro_selecionada
        for i in range(12):
            cor = "red" if i == peca else "white"
            if i < 6:
                label_texto_peca = self.matriz_labels_pecas_esquerda[i][0]
                novo_texto = self.criar_texto_peca(i, status.pecas_fora_tabuleiro[i])
                label_texto_peca.config(text=novo_texto, bg=cor)

                label_peca = self.matriz_labels_pecas_esquerda[i][1]
                label_peca.config(bg=cor)
            else:
                label_texto_peca = self.matriz_labels_pecas_direita[i - 6][1]
                novo_texto = self.criar_texto_peca(i, status.pecas_fora_tabuleiro[i])
                label_texto_peca.config(text=novo_texto, bg=cor)

                label_peca = self.matriz_labels_pecas_direita[i - 6][0]
                label_peca.config(bg=cor)

        self.labelMensagem.config(text=status.mensagem)
        self.label_turno.config(text=status.turno)

