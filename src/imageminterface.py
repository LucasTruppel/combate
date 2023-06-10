class ImagemInterface:
    
    def __init__(
                 self, 
                 mensagem: str,
                 turno: str,
                 tabuleiro: list, 
                 peca_fora_tabuleiro_selecionada: int,  
                 posicoes_selecionadas: list, 
                 pecas_fora_tabuleiro: list
                ) -> None:
        
        self.mensagem = mensagem
        self.turno = turno
        self.tabuleiro = tabuleiro
        self.peca_fora_tabuleiro_selecionada = peca_fora_tabuleiro_selecionada
        self.posicoes_selecionada = posicoes_selecionadas
        self.pecas_fora_tabuleiro = pecas_fora_tabuleiro
