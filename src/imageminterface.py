class ImagemInterface:
    
    def __init__(self, mensagem: str, tabuleiro: list, posicoes_selecionadas: list, pecas_fora_tabuleiro: list) -> None:
        self.mensagem = mensagem
        self.tabuleiro = tabuleiro
        self.posicoes_selecionada = posicoes_selecionadas
        self.pecas_fora_tabuleiro = pecas_fora_tabuleiro