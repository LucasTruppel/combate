from jogador import *
from random import shuffle

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
                    
    def alocar_pecas_adversario(self, matriz_adversario: list, jogador_adversario: Jogador) -> None:
        pecas_fora_tabuleiro_adversario = jogador_adversario.get_pecas_fora_tabuleiro()
        for i in range(0, 4):
            for j in range(10):
                forca_peca = matriz_adversario[i][j]
                posicao = self.matriz_posicoes[i][j]
                peca = pecas_fora_tabuleiro_adversario[forca_peca][0]
                posicao.set_ocupante(jogador_adversario)
                posicao.set_peca(peca)
                
    def alocar_rapidamente(self, jogador: Jogador):
        pecas_fora_tabuleiro = jogador.get_pecas_fora_tabuleiro()
        pecas = []
        for lista_pecas in pecas_fora_tabuleiro:
            for peca in lista_pecas:
                pecas.append(peca) 
        shuffle(pecas)
        pecas_fora_tabuleiro = [[] for i in range(12)]
        
        for i in range(6,10):
            for j in range(10):
                posicao = self.matriz_posicoes[i][j]
                peca = pecas.pop()
                posicao.set_ocupante(jogador)
                posicao.set_peca(peca)
                jogador.remover_peca_fora_tabuleiro(peca)
