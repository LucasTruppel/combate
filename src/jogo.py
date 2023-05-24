from estado import Estado
from jogador import Jogador
from tabuleiro import Tabuleiro
from imageminterface import ImagemInterface

class Jogo:
    
    def __init__(self) -> None:
        self.estado = Estado.NAO_COMECOU
        self.tabuleiro = Tabuleiro()
        self.jogador_local = Jogador()
        self.jogador_remoto = Jogador()
        
    def inicializar(self) -> None:
        self.tabuleiro.iniciar_tabuleiro()
        self.jogador_local.instanciar_pecas()
        
    def comecar_partida(self) -> None:
        pass
    
    def receber_inicio(self) -> None:
        self.jogador_local.set_jogador2(True)
        
    def continuar_inicio(self) -> None:
        self.estado = Estado.PREPARACAO
    
    def obter_status(self) -> ImagemInterface:
        tabuleiro_int = [[-1 for j in range(10)] for i in range(10)]
        for i in range(10):
            for j in range(10):
                peca = self.tabuleiro.get_posicao(i, j).get_peca()
                if peca != None:
                    tabuleiro_int[i][j] = peca.get_forca()
                    
        posicoes_selecionadas = [[0 for j in range(10)] for i in range(10)]
        posicao_selecionada = self.jogador_local.get_posicao_selecionada()
        if posicao_selecionada != None:
            linha,coluna = posicao_selecionada.get_coordenada()
            posicoes_selecionadas[linha][coluna] = 1
        
        # Peça de fora do tabuleiro selecionada
        peca_selecionada = self.jogador_local.get_peca_selecionada()
        forca_peca_selecionada = -1
        if peca_selecionada != None:
            forca_peca_selecionada = peca_selecionada.get_forca()
                   
        return ImagemInterface("", tabuleiro_int, forca_peca_selecionada, posicoes_selecionadas, self.jogador_local.get_quantidade_pecas_fora_tabuleiro())
    
    def selecionar_posicao(self, linha: int, coluna: int, peca_fora_tabuleiro: bool) -> dict:
        jogada = None
        turno = self.jogador_local.get_turno()
        if (self.estado == Estado.PREPARACAO or self.estado == Estado.COMBATE) and turno:
            posicao_selecionada = self.jogador_local.get_posicao_selecionada()
            peca_selecionada = self.jogador_local.get_peca_selecionada()
            
            if posicao_selecionada == None and peca_selecionada == None:
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
            if peca != None and jogador == self.jogador_local:
                casas_por_movimento = peca.get_casas_por_movimento()
                if casas_por_movimento > 0 or self.estado == Estado.PREPARACAO:
                    self.jogador_local.set_posicao_selecionada(posicao)
                    if self.estado == Estado.COMBATE:
                        self.jogador_local.verificar_lances_possiveis()
            
    def selecionar_destino(self, linha: int, coluna: int) -> dict:
        peca_selecionada = self.jogador_local.get_peca_selecionada()
        posicao_origem = self.jogador_local.get_posicao_selecionada()
        if posicao_origem != None:
            peca_origem = posicao_origem.get_peca()
        else:
            peca_origem = None
        posicao_destino = self.tabuleiro.get_posicao(linha, coluna)
        peca_destino = posicao_destino.get_peca()
        
        if self.estado == Estado.PREPARACAO:
            if peca_selecionada != None:
                if peca_destino == None and linha >= 6 and linha < 10:
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
            pass
            # TODO
                
        

