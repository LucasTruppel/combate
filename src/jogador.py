class Jogador:
    
    def __init__(self) -> None:
        self.turno = True
        self.vencedor = False
        self.pecas_fora_tabuleiro = []
        self.nome = ""
        self.posicao_selecionada = None
        self.posicoes_alcancaveis_posicao_selecionada = []
        self.peca_selecionada = []
        self.jogador2 = False
        
    def set_jogador2(self, eh_jogador2: bool) -> None:
        self.jogador2 = eh_jogador2
        