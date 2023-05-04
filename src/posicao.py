from peca import Peca

class Posicao:
    
    def __init__(self, coordenadas: tuple, eh_lago: bool) -> None:
        self.ocupante = None
        self.coordenada = coordenadas
        self.peca = None
        self.eh_lago = eh_lago