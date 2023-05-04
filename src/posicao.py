from peca import Peca

class Posicao:
    
    def __init__(self, i: int, j: int, eh_lago: bool) -> None:
        self.ocupante = None
        self.coordenada = (i, j)
        self.peca = None
        self.eh_lago = eh_lago