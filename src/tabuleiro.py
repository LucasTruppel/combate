from posicao import Posicao

class Tabuleiro:
    
    def __init__(self) -> None:
        self.matriz_posicoes = None
        
    def get_posicao(self, linha: int, coluna: int) -> Posicao:
        return self.matriz_posicoes[linha][coluna]

    def get_matriz_posicoes(self) -> list[list[Posicao]]:    
        return self.matriz_posicoes

    def iniciar_tabuleiro(self) -> None:
        self.matriz_posicoes = [[None for j in range(10)] for i in range(10)]
        for i in range(10):
            for j in range(10):
                if (i==4 or i == 5) and (j == 2 or j== 3 or j == 6 or j == 7):
                    self.matriz_posicoes[i][j] = Posicao(None, i, j, None, True)
                else:
                    self.matriz_posicoes[i][j] = Posicao(None, i, j, None, False)
                    
