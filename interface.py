from tkinter import *
from constantes import *

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

        self.desenhar_frame_principal()
        self.desenhar_celulas()
        self.desenhar_pecas_direita()
        self.desenhar_pecas_esquerda()
        self.desenhar_mensagem()
        
        self.janela_principal.mainloop()
        
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
                
    def desenhar_pecas_esquerda(self):
        self.borda_frame_pecas_esquerda = Frame(self.janela_principal,
                                               bg="black")
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
            for j in range(2):
                label_posicao = Label(self.frame_pecas_esquerda,
                                      bg="white")
                label_posicao.place(x=j*self.lado_celula,
                                    y=i*self.lado_frame_principal//10,
                                    width=self.lado_celula, 
                                    height=self.lado_celula,
                                    anchor="nw"
                                    )
    
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
            for j in range(2):
                label_posicao = Label(self.frame_pecas_direita,
                                      bg="white")
                label_posicao.place(x=j*self.lado_celula,
                                    y=i*self.lado_frame_principal//10,
                                    width=self.lado_celula, 
                                    height=self.lado_celula,
                                    anchor="nw"
                                    )
    
    def desenhar_mensagem(self):
        mensagem = "Seu turno!"
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
                                   font="arial 30"
                                   )
        self.labelMensagem.place(anchor="nw",
                                 width=int(self.lado_borda_frame_principal), 
                                 height=int(self.lado_borda_frame_principal//8),
                                 x = 0,
                                 y = 0
                                 )

InterfaceGraficaJogador()