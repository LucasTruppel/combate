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

        
        self.borda_frame_principal = Frame(self.janela_principal,
                                           bg="black")
        self.borda_frame_principal.place(anchor="center",
                                   width=int(self.lado_borda_frame_principal), 
                                   height=int(self.lado_borda_frame_principal),
                                   x = LARGURA//2,
                                   y = ALTURA//2)
        
        self.frame_principal = Frame(self.janela_principal,
                                     bg="black")
        self.frame_principal.place(anchor="center",
                                   width=self.lado_frame_principal, 
                                   height=self.lado_frame_principal,
                                   x = LARGURA//2,
                                   y = ALTURA//2)
        
        self.lado_celula = self.lado_frame_principal//10 - int(0.0030*self.lado_frame_principal)
        
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
        
        self.janela_principal.mainloop()



InterfaceGraficaJogador()