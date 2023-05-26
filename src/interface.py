from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
from dog.dog_interface import DogPlayerInterface
from dog.dog_actor import DogActor
from constantes import *
from objetoInterface import objetoInterface
from PIL import Image, ImageTk
from jogo import Jogo
from imageminterface import ImagemInterface


class InterfaceGraficaJogador(DogPlayerInterface):

    def __init__(self) -> None:
        self.janela_principal = Tk()
        self.init_tkinter()

        self.matriz_pecas = []
        self.matriz_pecas_esquerda = []
        self.matriz_pecas_direita = []

        self.imagens = self.ler_imagens()

        self.criar_menu()
        self.desenhar_janela()

        self.jogo = Jogo()
        self.jogo.inicializar()

        #dog
        player_name = simpledialog.askstring(title= "Player Identification", prompt = "Qual o seu nome?")
        self.dog_server_interface = DogActor()
        message = self.dog_server_interface.initialize(player_name,self)
        messagebox.showinfo(message = message)

        self.janela_principal.mainloop()

    def init_tkinter(self):
        self.janela_principal.title("Combate")
        self.janela_principal.geometry(f"{LARGURA}x{ALTURA}")
        self.janela_principal.resizable(False, False)
        self.janela_principal.configure(bg="gray")

        self.lado_borda_frame_principal = int(ALTURA*0.85)
        self.lado_frame_principal = int(self.lado_borda_frame_principal*0.98)
        self.lado_celula = self.lado_frame_principal//10 - int(0.0030*self.lado_frame_principal)

    def desenhar_janela(self):
        self.desenhar_frame_principal()
        self.desenhar_celulas()
        self.desenhar_pecas_direita()
        self.desenhar_pecas_esquerda()
        self.desenhar_mensagem("Clique em iniciar partida para jogar!")

    def criar_menu(self):
        self.barra_menu = Menu(self.janela_principal)
        self.janela_principal.config(menu=self.barra_menu)
        self.barra_menu.add_command(label="Iniciar partida",
                                    command= lambda: self.start_match())
        self.barra_menu.add_command(label="Terminar preparação",
                                    command= lambda: self.criar_popup("Partida ainda não iniciada."))

    def desenhar_frame_principal(self):
        self.borda_frame_principal = Frame(self.janela_principal,
                                           bg="black")
        self.borda_frame_principal.place(anchor="center",
                                   width=int(self.lado_borda_frame_principal),
                                   height=int(self.lado_borda_frame_principal),
                                   x = LARGURA//2,
                                   y = ALTURA//2 + ALTURA//20)

        self.frame_principal = Frame(self.janela_principal,
                                     bg="black")
        self.frame_principal.place(anchor="center",
                                   width=self.lado_frame_principal,
                                   height=self.lado_frame_principal,
                                   x = LARGURA//2,
                                   y = ALTURA//2 + ALTURA//20)

    def desenhar_celulas(self):
        for i in range(10):
            linha_matriz = []
            for j in range(10):

                if (i==4 or i==5) and (j==2 or j==3 or j==6 or j==7):
                    cor = "blue"
                else:
                    cor = "green"


                label_posicao = Label(self.frame_principal,
                                      bg=cor)
                label_posicao.place(x=j*self.lado_frame_principal//10 + self.lado_frame_principal//20,
                                    y=i*self.lado_frame_principal//10 + self.lado_frame_principal//20,
                                    width=self.lado_celula,
                                    height=self.lado_celula,
                                    anchor="center"
                                    )
                linha_matriz.append(label_posicao)
                label_posicao.bind("<Button-1>", lambda event, linha=i, coluna=j,
                                   objeto=objetoInterface.TABULEIRO.value: self.click(event, linha, coluna, objeto))
            self.matriz_pecas.append(linha_matriz)

    def desenhar_pecas_esquerda(self):
        self.borda_frame_pecas_esquerda = Frame(self.janela_principal,
                                               bg="black",
                                               )
        self.borda_frame_pecas_esquerda.place(anchor="e",
                                             width=2*self.lado_celula + int(0.0125*self.lado_borda_frame_principal),
                                             height=int(0.6*self.lado_borda_frame_principal + 0.0125*self.lado_borda_frame_principal),
                                             x = LARGURA//2 - self.lado_borda_frame_principal//2,
                                             y = ALTURA//2 + ALTURA//20)

        self.frame_pecas_esquerda = Frame(self.janela_principal,
                                      bg="black")
        self.frame_pecas_esquerda.place(anchor="e",
                                    width=2*self.lado_celula,
                                    height=int(0.6*self.lado_frame_principal),
                                    x = LARGURA//2 - self.lado_borda_frame_principal//2 - int(0.02*self.lado_celula),
                                    y = ALTURA//2 + ALTURA//20)

        for i in range(6):
            linha = []
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

                label_posicao.place(x=j*self.lado_celula,
                                    y=i*self.lado_frame_principal//10,
                                    width=self.lado_celula,
                                    height=self.lado_celula,
                                    anchor="nw"
                                    )
                linha.append(label_posicao)
                label_posicao.bind("<Button-1>", lambda event, linha=i, coluna=j,
                                   objeto=objetoInterface.PECAS_ESQUERDA.value: self.click(event, linha, coluna, objeto))

            self.matriz_pecas_esquerda.append(linha)

    def desenhar_pecas_direita(self):
        self.borda_frame_pecas_direita = Frame(self.janela_principal,
                                               bg="black")
        self.borda_frame_pecas_direita.place(anchor="w",
                                             width=2*self.lado_celula + int(0.0125*self.lado_borda_frame_principal),
                                             height=int(0.6*self.lado_borda_frame_principal + 0.0125*self.lado_borda_frame_principal),
                                             x = LARGURA//2 + self.lado_borda_frame_principal//2,
                                             y = ALTURA//2 + ALTURA//20)

        self.frame_pecas_direita = Frame(self.janela_principal,
                                      bg="black")
        self.frame_pecas_direita.place(anchor="w",
                                    width=2*self.lado_celula,
                                    height=int(0.6*self.lado_frame_principal),
                                    x = LARGURA//2 + self.lado_borda_frame_principal//2 + int(0.02*self.lado_celula),
                                    y = ALTURA//2 + ALTURA//20)

        for i in range(6):
            linha = []
            for j in range(2):
                if j == 1:
                    label_posicao = Label(self.frame_pecas_direita,
                                      bg="white",
                                      text=self.criar_texto_peca(6+i, quantidade_inicial[6+i]),
                                      font="arial 10",
                                      width=self.lado_celula,
                                      height=self.lado_celula)
                else:
                    label_posicao = Label(self.frame_pecas_direita,
                                      bg="white",
                                      image=self.imagens[6+i],
                                      width=self.lado_celula,
                                      height=self.lado_celula)

                label_posicao.place(x=j*self.lado_celula,
                                    y=i*self.lado_frame_principal//10,
                                    width=self.lado_celula,
                                    height=self.lado_celula,
                                    anchor="nw"
                                    )
                linha.append(label_posicao)
                label_posicao.bind("<Button-1>", lambda event, linha=i, coluna=j,
                                   objeto=objetoInterface.PECAS_DIREITA.value: self.click(event, linha, coluna, objeto))
            self.matriz_pecas_direita.append(linha)

    def desenhar_mensagem(self, mensagem):

        self.frameMensagem = Frame(self.janela_principal,
                                   bg="gray"
                                   )
        self.frameMensagem.place(anchor="n",
                                 width=int(LARGURA*0.95),
                                 height=int(self.lado_borda_frame_principal//8),
                                 x = LARGURA//2,
                                 y = int(0.01*ALTURA))

        self.labelMensagem = Label(self.frameMensagem,
                                   bg="gray",
                                   text=mensagem,
                                   font="arial 30"
                                   )
        self.labelMensagem.place(anchor="nw",
                                 width=int(LARGURA*0.95),
                                 height=int(self.lado_borda_frame_principal//8),
                                 x = 0,
                                 y = 0
                                 )

    def click(self, event, i, j, objeto):
        if objeto == objetoInterface.TABULEIRO.value:
            self.selecionar_posicao(i, j, False)
        elif objeto == objetoInterface.PECAS_ESQUERDA.value:
            self.selecionar_posicao(i, 0, True)
        elif objeto == objetoInterface.PECAS_DIREITA.value:
            self.selecionar_posicao(i, 1, True)

    def ler_imagens(self):
        imagens = []
        for i in range(13):
            imagem = Image.open(f"./resources/images/{i}.png").convert("RGBA")
            imagem = imagem.resize((int(self.lado_celula*0.9), int(self.lado_celula*0.9)), Image.ANTIALIAS)
            imagens.append(ImageTk.PhotoImage(imagem))
        return imagens

    def criar_texto_peca(self, peca, quantidade):
        return nome_peca[peca] +"\nF: " + str(peca) +"\nD: " + str(quantidade)

    def criar_popup(self, texto):
        popup = Toplevel(self.janela_principal)
        popup.geometry(f"{LARGURA//4}x{ALTURA//4}")
        popup.title("Aviso")
        popup.resizable(False, False)
        Label(popup, text = texto, font = "Arial 18").pack(pady = ALTURA//16)
        Button(popup, text="Fechar", command=popup.destroy).pack()

    def start_match(self) -> None:
        start_status = self.dog_server_interface.start_match(2)
        code = start_status.get_code()
        message = start_status.get_message()

        if code == "0" or code == "1":
            messagebox.showinfo(message=message)
        elif code =="2":
            local_player_id = start_status.get_local_id()
            players = start_status.get_players()
            self.continuar_inicio()
            messagebox.showinfo(message=message)

    def receive_start(self, start_status) -> None:
        local_player_id = start_status.get_local_id()
        players = start_status.get_players()

        message = start_status.get_message()
        messagebox.showinfo(message=message)

        self.jogo.receber_inicio()

    def continuar_inicio(self) -> None:
        self.jogo.continuar_inicio()

    def atualizar_interface(self, status: ImagemInterface) -> None:
        for i in range(10):
            for j in range(10):
                if not ((i==4 or i==5) and (j==2 or j==3 or j==6 or j==7)): # Os lagos nunca atualizam
                    label = self.matriz_pecas[i][j]
                    forca = status.tabuleiro[i][j]
                    selecionado = status.posicoes_selecionada[i][j]

                    if selecionado == 1:
                        label.config(bg="red")
                    elif selecionado == 2:
                        label.config(bg="yellow")
                    else:
                        label.config(bg="green")

                    if forca > -1:
                        label.config(image = self.imagens[forca])
                    else:
                        label.config(image = "")

        peca = status.peca_fora_tabuleiro_selecionada
        for i in range(12):
            cor = "red" if i == peca else "white"
            if i < 6:
                label_texto_peca = self.matriz_pecas_esquerda[i][0]
                novo_texto = self.criar_texto_peca(i, status.pecas_fora_tabuleiro[i])
                label_texto_peca.config(text = novo_texto, bg = cor)

                label_peca = self.matriz_pecas_esquerda[i][1]
                label_peca.config(bg = cor)
            else:
                label_texto_peca = self.matriz_pecas_direita[i-6][1]
                novo_texto = self.criar_texto_peca(i, status.pecas_fora_tabuleiro[i])
                label_texto_peca.config(text = novo_texto, bg = cor)

                label_peca = self.matriz_pecas_direita[i-6][0]
                label_peca.config(bg = cor)
                
        self.labelMensagem.config(text=status.mensagem)
                
        

    def selecionar_posicao(self, linha: int, coluna: int, peca_fora_tabuleiro: bool) -> None:
        jogada = self.jogo.selecionar_posicao(linha, coluna, peca_fora_tabuleiro)
        if jogada != None:
            self.dog_server_interface.send_move(jogada)
        status = self.jogo.obter_status()
        self.atualizar_interface(status)
