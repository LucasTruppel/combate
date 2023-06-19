from jogador import *
from random import shuffle


class Tabuleiro:

    def __init__(self) -> None:
        self.matriz_posicoes = None

    def get_posicao(self, linha: int, coluna: int) -> Posicao:
        return self.matriz_posicoes[linha][coluna]

    def iniciar_tabuleiro(self) -> None:
        self.matriz_posicoes = [[None for _ in range(10)] for _ in range(10)]
        for i in range(10):
            for j in range(10):
                if (i == 4 or i == 5) and (j == 2 or j == 3 or j == 6 or j == 7):
                    self.matriz_posicoes[i][j] = Posicao(None, i, j, None, True)
                else:
                    self.matriz_posicoes[i][j] = Posicao(None, i, j, None, False)

    def alocar_pecas_adversario(self, matriz_adversario: list, jogador_adversario: Jogador) -> None:
        pecas_fora_tabuleiro_adversario = jogador_adversario.get_pecas_fora_tabuleiro()
        for i in range(0, 4):
            for j in range(10):
                forca_peca = int(matriz_adversario[i][j])
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
        for i in range(6, 10):
            for j in range(10):
                posicao = self.matriz_posicoes[i][j]
                if posicao.get_peca() is None:
                    peca = pecas.pop()
                    posicao.set_ocupante(jogador)
                    posicao.set_peca(peca)
                    jogador.remover_peca_fora_tabuleiro(peca)
        pecas_fora_tabuleiro = [[] for _ in range(12)]
        jogador.set_pecas_fora_tabuleiro(pecas_fora_tabuleiro)

    def verificar_lances_possiveis(self, posicao: Posicao, jogador: Jogador) -> None:
        i_peca, j_peca = posicao.get_coordenada()
        peca = posicao.get_peca()
        casas_por_movimento = peca.get_casas_por_movimento()
        tipo_peca = peca.get_tipo()
        posicoes_alcancaveis = []

        # Cima
        for k in range(1, casas_por_movimento+1):
            i = i_peca - k
            j = j_peca
            if i < 0:
                break
            posicao_atual = self.matriz_posicoes[i][j]
            ocupante = posicao_atual.get_ocupante()
            if ocupante == jogador or posicao_atual.get_eh_lago():
                break
            posicoes_alcancaveis.append((i, j))
            if ocupante is not None and ocupante != jogador:
                if tipo_peca == "Soldado" and k > 1:
                    posicoes_alcancaveis.remove((i, j))
                break

        # Direita
        for k in range(1, casas_por_movimento+1):
            i = i_peca
            j = j_peca + k
            if j > 9:
                break
            posicao_atual = self.matriz_posicoes[i][j]
            ocupante = posicao_atual.get_ocupante()
            if ocupante == jogador or posicao_atual.get_eh_lago():
                break
            posicoes_alcancaveis.append((i, j))
            if ocupante is not None and ocupante != jogador:
                if tipo_peca == "Soldado" and k > 1:
                    posicoes_alcancaveis.remove((i, j))
                break

        # Baixo
        for k in range(1, casas_por_movimento+1):
            i = i_peca + k
            j = j_peca
            if i > 9:
                break
            posicao_atual = self.matriz_posicoes[i][j]
            ocupante = posicao_atual.get_ocupante()
            if ocupante == jogador or posicao_atual.get_eh_lago():
                break
            posicoes_alcancaveis.append((i, j))
            if ocupante is not None and ocupante != jogador:
                if tipo_peca == "Soldado" and k > 1:
                    posicoes_alcancaveis.remove((i, j))
                break

        # Esquerda
        for k in range(1, casas_por_movimento+1):
            i = i_peca
            j = j_peca - k
            if j < 0:
                break
            posicao_atual = self.matriz_posicoes[i][j]
            ocupante = posicao_atual.get_ocupante()
            if ocupante == jogador or posicao_atual.get_eh_lago():
                break
            posicoes_alcancaveis.append((i, j))
            if ocupante is not None and ocupante != jogador:
                if tipo_peca == "Soldado" and k > 1:
                    posicoes_alcancaveis.remove((i, j))
                break

        jogador.set_posicoes_alcancaveis_posicao_selecionada(posicoes_alcancaveis)

    def pecas_moveis_acabaram(self, jogador) -> bool:
        pecas_acabaram = True
        for i in range(9, -1, -1):
            for j in range(9, -1, -1):
                posicao = self.matriz_posicoes[i][j]
                peca = posicao.get_peca()
                if peca is not None and posicao.get_ocupante() == jogador and peca.get_casas_por_movimento() > 0:
                    pecas_acabaram = False
                    break
            if not pecas_acabaram:
                break
        return pecas_acabaram

    def campo_esta_pronto(self) -> bool:
        campo_pronto = True
        for i in range(6, 10):
            for j in range(10):
                if self.matriz_posicoes[i][j].get_peca() is None:
                    campo_pronto = False
                    break
            if not campo_pronto:
                break
        return campo_pronto
