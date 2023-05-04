from estado import Estado
from jogador import Jogador
from tabuleiro import Tabuleiro

class Jogo:
    
    def __init__(self) -> None:
        self.estado = Estado.NAO_COMECOU
        self.tabuleiro = Tabuleiro()
        self.jogador_local = Jogador()
        self.jogador_remoto = Jogador()
        
    def comecar_partida(self) -> None:
        pass
    
    def receber_inicio(self) -> None:
        self.jogador_local.set_jogador2(True)
        
    def continuar_inicio(self) -> None:
        self.estado = Estado.PREPARACAO
        self.tabuleiro.iniciar_tabuleiro
    
    def obter_status(self) -> None:
        pass
    
    def selecionar_posicao(self, linha: int, coluna: int, peca_fora_tabuleiro: bool) -> dict:
        turno = self.jogador_local.get_turno()
        if turno:
            posicao_selecionada = self.jogador_local.get_posicao_selecionada()
            peca_selecionada = self.jogador_local.get_peca_selecionada()
            #TODO
