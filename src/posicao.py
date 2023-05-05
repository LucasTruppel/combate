from peca import Peca

class Posicao:
    
    def __init__(self, ocupante, i: int, j: int, peca: Peca, eh_lago: bool) -> None:
        self.ocupante = None
        self.coordenada = (i, j)
        self.peca = None
        self.eh_lago = eh_lago
        
    def get_ocupante(self):
        return self.ocupante
    
    def get_peca(self) -> Peca:
        return self.peca
    
    def set_peca(self, peca: Peca) -> None:
        self.peca = peca
        
    def set_ocupante(self, ocupante):
        self.ocupante = ocupante
