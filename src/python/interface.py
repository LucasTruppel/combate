from tkinter import *
from constantes import *
from objetoInterface import objetoInterface
from PIL import Image, ImageTk

class InterfaceGraficaJogador:
    
    def __init__(self) -> None:
        self.janela_principal = Tk()
        self.janela_principal.title("Combate")
        self.janela_principal.geometry(f"{LARGURA}x{ALTURA}")
        self.janela_principal.resizable(False, False)
        self.janela_principal.configure(bg="gray")
        
        self.lado_borda_frame_principal = int(ALTURA*0.85)
        self.lado_frame_principal = int(self.lado_borda_frame_principal*0.98)
        self.lado_celula = self.lado_frame_principal//10 - int(0.0030*self.lado_frame_principal)

        self.matriz_pecas = []
        self.matriz_pecas_esquerda = []
        self.matriz_pecas_direita = []
        
        self.imagens = self.ler_imagens()

        self.criar_menu()
        self.desenhar_frame_principal()
        self.desenhar_celulas()
        self.desenhar_pecas_direita()
        self.desenhar_pecas_esquerda()
        self.desenhar_mensagem()
        
        self.janela_principal.mainloop()
        
    def criar_menu(self):
        self.barra_menu = Menu(self.janela_principal)
        self.janela_principal.config(menu=self.barra_menu)
        self.barra_menu.add_command(label="Conectar")
        self.barra_menu.add_command(label="Iniciar partida")
        self.barra_menu.add_command(label="Terminar preparação")

        
        
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
                                      text=self.criar_texto_peca(i),
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
                                      text=self.criar_texto_peca(6+i),
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
    
    def desenhar_mensagem(self):
        mensagem = "Conecte-se para jogar!"
        self.frameMensagem = Frame(self.janela_principal,
                                   bg="gray"
                                   )
        self.frameMensagem.place(anchor="n", 
                                 width=int(self.lado_borda_frame_principal), 
                                 height=int(self.lado_borda_frame_principal//8),
                                 x = LARGURA//2,
                                 y = int(0.01*ALTURA))
        
        self.labelMensagem = Label(self.frameMensagem,
                                   bg="gray",
                                   text=mensagem,
                                   font="arial 40"
                                   )
        self.labelMensagem.place(anchor="nw",
                                 width=int(self.lado_borda_frame_principal), 
                                 height=int(self.lado_borda_frame_principal//8),
                                 x = 0,
                                 y = 0
                                 )

    def click(self, event, i, j, objeto):
        if objeto == objetoInterface.TABULEIRO.value:
            label = self.matriz_pecas[i][j]
            if label.cget("bg") != "red":
                label.config(bg="red")
            else:
                if (i==4 or i==5) and (j==2 or j==3 or j==6 or j==7):
                    label.config(bg="blue")
                else:
                    label.config(bg="green")
        
        elif objeto == objetoInterface.PECAS_ESQUERDA.value:
            label_esquerda = self.matriz_pecas_esquerda[i][0]
            label_direita = self.matriz_pecas_esquerda[i][1]
            if label_esquerda.cget("bg") != "red":
                label_esquerda.config(bg="red")
                label_direita.config(bg="red")
            else:
                label_esquerda.config(bg="white")
                label_direita.config(bg="white")
                
        elif objeto == objetoInterface.PECAS_DIREITA.value:
            label_esquerda = self.matriz_pecas_direita[i][0]
            label_direita = self.matriz_pecas_direita[i][1]
            if label_esquerda.cget("bg") != "red":
                label_esquerda.config(bg="red")
                label_direita.config(bg="red")
            else:
                label_esquerda.config(bg="white")
                label_direita.config(bg="white")

    def ler_imagens(self):
        imagens = []
        for i in range(13):
            imagem = Image.open(f"./src/resources/images/{i}.png").convert("RGBA")
            imagem = imagem.resize((int(self.lado_celula*0.9), int(self.lado_celula*0.9)), Image.ANTIALIAS)
            imagens.append(ImageTk.PhotoImage(imagem))
        return imagens
    
    def criar_texto_peca(self, peca):
        return nome_peca[peca] +"\nF: " + str(peca) +"\nD: " + str(quantidade_inicial[peca])

if __name__ == "__main__":
    InterfaceGraficaJogador()
