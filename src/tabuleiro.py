from posicao import Posicao

class Tabuleiro:
    
    def __init__(self) -> None:
        matriz_posicoes = [[] for i in range(10)]
        
    def iniciar_tabuleiro(self) -> None:
        for i in range(10):
            for j in range(10):
                if (i==4 or i == 5) and (j == 2 or j== 3 or j == 6 or j == 7):
                    self.matriz_posicoes[i][j] = Posicao(None, (i, j), None, True)
                else:
                    self.matriz_posicoes[i][j] = Posicao(None, (i, j), None, False)
