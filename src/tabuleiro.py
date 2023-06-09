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
                if (i == 4 or i == 5) and (j == 2 or j == 3 or j == 6 or j == 7):
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

        for i in range(6, 10):
            for j in range(10):
                posicao = self.matriz_posicoes[i][j]
                if posicao.get_peca() is None:
                    peca = pecas.pop()
                    posicao.set_ocupante(jogador)
                    posicao.set_peca(peca)
                    jogador.remover_peca_fora_tabuleiro(peca)

    def verificar_lances_possiveis(self, posicao: Posicao, jogador: Jogador) -> None:
        i_peca, j_peca = posicao.get_coordenada()
        casas_por_movimento = posicao.get_peca().get_casas_por_movimento()
        posicoes_alcancaveis = []

        # Cima
        for k in range(1, casas_por_movimento+1):
            i = i_peca - k
            j = j_peca
            if i < 0:
                break
            posicao_atual = self.matriz_posicoes[i][j]
            ocupante = posicao_atual.get_ocupante()
            if ocupante == jogador or posicao.get_eh_lago():
                break
            posicoes_alcancaveis.append((i, j))
            if ocupante is not None and ocupante != jogador:
                break

        # Direita
        for k in range(1, casas_por_movimento+1):
            i = i_peca
            j = j_peca + k
            if j > 9:
                break
            posicao_atual = self.matriz_posicoes[i][j]
            ocupante = posicao_atual.get_ocupante()
            if ocupante == jogador or posicao.get_eh_lago():
                break
            posicoes_alcancaveis.append((i, j))
            if ocupante is not None and ocupante != jogador:
                break

        # Baixo
        for k in range(1, casas_por_movimento+1):
            i = i_peca + k
            j = j_peca
            if i > 9:
                break
            posicao_atual = self.matriz_posicoes[i][j]
            ocupante = posicao_atual.get_ocupante()
            if ocupante == jogador or posicao.get_eh_lago():
                break
            posicoes_alcancaveis.append((i, j))
            if ocupante is not None and ocupante != jogador:
                break

        # Esquerda
        for k in range(1, casas_por_movimento+1):
            i = i_peca
            j = j_peca - k
            if j < 0:
                break
            posicao_atual = self.matriz_posicoes[i][j]
            ocupante = posicao_atual.get_ocupante()
            if ocupante == jogador or posicao.get_eh_lago():
                break
            posicoes_alcancaveis.append((i, j))
            if ocupante is not None and ocupante != jogador:
                break

        jogador.set_posicoes_alcancaveis_posicao_selecionada(posicoes_alcancaveis)

    def atualizar_tabuleiro(self, jogada: dict, jogador_local: Jogador, jogador_remoto: Jogador) -> None:
        x, y = jogada["lance_combate"][0]
        w, z = jogada["lance_combate"][1]
        posicao_origem = self.matriz_posicoes[x][y]
        posicao_destino = self.matriz_posicoes[w][z]
        peca_origem = posicao_origem.get_peca()
        peca_destino = posicao_destino.get_peca()
        if jogada["info_combate_pecas"] == 0:
            posicao_destino.ocupar(peca_origem, jogador_remoto)
        elif jogada["info_combate_pecas"] == 1:
            posicao_destino.ocupar(peca_origem, jogador_remoto)
            jogador_local.adicionar_peca_fora_tabuleiro(peca_destino)
        elif jogada["info_combate_pecas"] == 2:
            jogador_remoto.adicionar_peca_fora_tabuleiro(peca_origem)
        elif jogada["info_combate_pecas"] == 3:
            posicao_destino.desocupar()
            jogador_remoto.adicionar_peca_fora_tabuleiro(peca_origem)
            jogador_local.adicionar_peca_fora_tabuleiro(peca_destino)
        posicao_origem.desocupar()
