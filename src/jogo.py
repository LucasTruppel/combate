from estado import Estado
from tabuleiro import *
from imageminterface import ImagemInterface
import pprint as p


class Jogo:

    def __init__(self) -> None:
        self.estado = Estado.NAO_COMECOU
        self.tabuleiro = Tabuleiro()
        self.jogador_local = Jogador()
        self.jogador_remoto = Jogador()
        self.exercito_adversario_recebido = False
        self.exercito_enviado = False
        self.mensagem = ""

    def inicializar(self) -> None:
        self.tabuleiro.iniciar_tabuleiro()
        self.jogador_local.instanciar_pecas()
        self.jogador_remoto.instanciar_pecas()

    def comecar_partida(self) -> None:
        self.jogador_remoto.set_jogador2(True)
        self.continuar_inicio()

    def receber_inicio(self) -> None:
        self.jogador_local.set_jogador2(True)
        self.continuar_inicio()

    def continuar_inicio(self) -> None:
        self.estado = Estado.PREPARACAO
        self.mensagem = "Posicione suas peças e clique em terminar preparação!"

    def obter_status(self) -> ImagemInterface:
        tabuleiro_int = [[-1 for j in range(10)] for i in range(10)]
        for i in range(10):
            for j in range(10):
                posicao = self.tabuleiro.get_posicao(i, j)
                peca = self.tabuleiro.get_posicao(i, j).get_peca()
                if peca is not None:
                    if posicao.get_ocupante() == self.jogador_local:
                        tabuleiro_int[i][j] = peca.get_forca()
                    else:
                        tabuleiro_int[i][j] = 12

        posicoes_selecionadas = [[0 for j in range(10)] for i in range(10)]
        posicao_selecionada = self.jogador_local.get_posicao_selecionada()
        if posicao_selecionada is not None:
            linha, coluna = posicao_selecionada.get_coordenada()
            posicoes_selecionadas[linha][coluna] = 1
            for i, j in self.jogador_local.get_posicoes_alcancaveis_posicao_selecionada():
                posicoes_selecionadas[i][j] = 2
        p.pprint(posicoes_selecionadas)

        # Peça de fora do tabuleiro selecionada
        peca_selecionada = self.jogador_local.get_peca_selecionada()
        forca_peca_selecionada = -1
        if peca_selecionada is not None:
            forca_peca_selecionada = peca_selecionada.get_forca()

        return ImagemInterface(self.mensagem, tabuleiro_int, forca_peca_selecionada, posicoes_selecionadas,
                               self.jogador_local.get_quantidade_pecas_fora_tabuleiro())

    def selecionar_posicao(self, linha: int, coluna: int, peca_fora_tabuleiro: bool) -> dict:
        jogada = None
        turno = self.jogador_local.get_turno()
        if self.estado == Estado.PREPARACAO or (self.estado == Estado.COMBATE and turno):
            posicao_selecionada = self.jogador_local.get_posicao_selecionada()
            peca_selecionada = self.jogador_local.get_peca_selecionada()

            if posicao_selecionada is None and peca_selecionada is None:
                self.selecionar_origem(linha, coluna, peca_fora_tabuleiro)
            else:
                jogada = self.selecionar_destino(linha, coluna)
        return jogada

    def selecionar_origem(self, linha: int, coluna: int, peca_fora_tabuleiro: bool) -> None:
        if peca_fora_tabuleiro and self.estado == Estado.PREPARACAO:
            self.jogador_local.selecionar_peca_fora_tabuleiro(linha, coluna)
        else:
            posicao = self.tabuleiro.get_posicao(linha, coluna)
            jogador = posicao.get_ocupante()
            peca = posicao.get_peca()
            if peca is not None and jogador == self.jogador_local:
                casas_por_movimento = peca.get_casas_por_movimento()
                if casas_por_movimento > 0 or self.estado == Estado.PREPARACAO:
                    self.jogador_local.set_posicao_selecionada(posicao)
                    if self.estado == Estado.COMBATE:
                        self.tabuleiro.verificar_lances_possiveis(posicao, self.jogador_local)

    def selecionar_destino(self, linha: int, coluna: int) -> dict:
        jogada = {}
        peca_selecionada = self.jogador_local.get_peca_selecionada()
        posicao_origem = self.jogador_local.get_posicao_selecionada()
        if posicao_origem is not None:
            peca_origem = posicao_origem.get_peca()
        else:
            peca_origem = None
        posicao_destino = self.tabuleiro.get_posicao(linha, coluna)
        peca_destino = posicao_destino.get_peca()

        if self.estado == Estado.PREPARACAO:
            if peca_selecionada is not None:
                if peca_destino is None and 6 <= linha < 10:
                    posicao_destino.set_peca(peca_selecionada)
                    self.jogador_local.remover_peca_fora_tabuleiro(peca_selecionada)
                    posicao_destino.set_ocupante(self.jogador_local)
                    self.jogador_local.set_peca_selecionada(None)
                else:
                    self.jogador_local.set_peca_selecionada(None)
            else:
                if posicao_origem == posicao_destino:
                    posicao_destino.set_peca(None)
                    posicao_destino.set_ocupante(None)
                    self.jogador_local.adicionar_peca_fora_tabuleiro(peca_origem)
                    self.jogador_local.set_posicao_selecionada(None)
                else:
                    self.jogador_local.set_posicao_selecionada(None)
        else:
            if (linha, coluna) in self.jogador_local.get_posicoes_alcancaveis_posicao_selecionada():
                if peca_destino is not None:
                    self.comparar_pecas(peca_origem, peca_destino, linha, coluna, jogada)
                else:
                    posicao_destino.set_peca(peca_origem)
                    posicao_destino.set_ocupante(self.jogador_local)
                    jogada["info_combate_pecas"] = 0
                    jogada["bandeira_capturada"] = False
                posicao_origem.set_peca(None)
                posicao_origem.set_ocupante(None)
                self.jogador_local.set_posicao_selecionada(None)
                self.jogador_local.set_posicoes_alcancaveis_posicao_selecionada([])
                self.jogador_local.inverter_turno()
                jogada["preparacao"] = False
                jogada["lance_preparacao"] = None
                jogada["lance_combate"] = [posicao_origem.get_coordenada(), posicao_destino.get_coordenada()]
                jogada["match_status"] = "next"
                self.espelhar_jogada(jogada)
            else:
                self.jogador_local.set_posicao_selecionada(None)
                self.jogador_local.set_posicoes_alcancaveis_posicao_selecionada([])
        return jogada

    def inverter_posicao(self, coordenadas: tuple) -> tuple:
        i, j = coordenadas
        return 9 - i, 9 - j
    
    def espelhar_jogada(self, jogada: dict) -> dict:
        if jogada["preparacao"]:
            matriz = [[-1 for j in range(10)] for i in range(10)]
            for i in range(6, 10):
                for j in range(10):
                    peca = self.tabuleiro.get_posicao(i, j).get_peca()
                    matriz[9 - i][9 - j] = peca.get_forca()
            jogada["lance_preparacao"] = matriz
        else:
            jogada["lance_combate"][0] = self.inverter_posicao(jogada["lance_combate"][0])
            jogada["lance_combate"][1] = self.inverter_posicao(jogada["lance_combate"][1])
        return jogada
        
    def terminar_preparacao(self) -> dict:
        jogada = {}
        if self.estado == Estado.PREPARACAO and self.jogador_local.pecas_fora_tabuleiro_vazio():
            self.exercito_enviado = True
            jogada["preparacao"] = True
            jogada["bandeira_capturada"] = False
            jogada["adversario_venceu_combate_pecas"] = False
            jogada["lance_combate"] = None
            jogada["match_status"] = "next"
            jogada = self.espelhar_jogada(jogada)
            
            if self.exercito_adversario_recebido:
                self.iniciar_combate()
            else:
                self.mensagem = "Aguardando oponente"
        return jogada
            
    def receber_jogada(self, jogada: dict) -> None:
        if not jogada["bandeira_capturada"]:
            if jogada["preparacao"]:
                self.exercito_adversario_recebido = True
                self.tabuleiro.alocar_pecas_adversario(jogada["lance_preparacao"], self.jogador_remoto)
                
                if self.exercito_enviado:
                    self.iniciar_combate()
            else:
                self.tabuleiro.atualizar_tabuleiro(jogada, self.jogador_local, self.jogador_remoto)
                self.jogador_local.inverter_turno()
        else:
            self.finalizar()
    
    def iniciar_combate(self) -> None:
        self.estado = Estado.COMBATE
        if not self.jogador_local.jogador2:
            self.jogador_local.inverter_turno()
        self.mensagem = "Combate iniciado!"

    def alocar_rapidamente(self) -> None:
        self.tabuleiro.alocar_rapidamente(self.jogador_local)

    def comparar_pecas(self, peca_local: Peca, peca_remoto: Peca, linha: int, coluna: int, jogada: dict):
        tipo_local = peca_local.get_tipo()
        tipo_remoto = peca_remoto.get_tipo()
        forca_local = peca_local.get_forca()
        forca_remoto = peca_remoto.get_forca()
        posicao_destino = self.tabuleiro.get_posicao(linha, coluna)

        jogada["bandeira_capturada"] = False

        if tipo_remoto == "Bandeira":
            self.jogador_local.set_vencedor(True)
            self.finalizar()
            jogada["info_combate_pecas"] = 1
            jogada["bandeira_capturada"] = True
        elif tipo_remoto == "Bomba":
            if tipo_local == "Cabo":
                self.jogador_remoto.adicionar_peca_fora_tabuleiro(peca_remoto)
                posicao_destino.ocupar(peca_local, self.jogador_local)
                jogada["info_combate_pecas"] = 1
            else:
                self.jogador_local.adicionar_peca_fora_tabuleiro(peca_local)
                self.jogador_remoto.adicionar_peca_fora_tabuleiro(peca_remoto)
                posicao_destino.desocupar()
                jogada["info_combate_pecas"] = 3
        elif tipo_local == "Espião":
            if tipo_remoto == "General":
                self.jogador_remoto.adicionar_peca_fora_tabuleiro(peca_remoto)
                posicao_destino.ocupar(peca_local, self.jogador_local)
                jogada["info_combate_pecas"] = 1
            elif tipo_remoto == "Espião":
                self.jogador_local.adicionar_peca_fora_tabuleiro(peca_local)
                self.jogador_remoto.adicionar_peca_fora_tabuleiro(peca_remoto)
                posicao_destino.desocupar()
                jogada["info_combate_pecas"] = 3
            else:
                self.jogador_local.adicionar_peca_fora_tabuleiro(peca_local)
                jogada["info_combate_pecas"] = 2
        else:
            if forca_local > forca_remoto:
                self.jogador_remoto.adicionar_peca_fora_tabuleiro(peca_remoto)
                posicao_destino.ocupar(peca_local, self.jogador_local)
                jogada["info_combate_pecas"] = 1
            elif forca_local < forca_remoto:
                self.jogador_local.adicionar_peca_fora_tabuleiro(peca_local)
                jogada["info_combate_pecas"] = 2
            else:
                self.jogador_local.adicionar_peca_fora_tabuleiro(peca_local)
                self.jogador_remoto.adicionar_peca_fora_tabuleiro(peca_remoto)
                posicao_destino.desocupar()
                jogada["info_combate_pecas"] = 3

    def finalizar(self):
        pass
