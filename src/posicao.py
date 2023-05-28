class Posicao:
    
    def __init__(self, ocupante, i: int, j: int, peca, eh_lago: bool) -> None:
        self.ocupante = None
        self.coordenada = (i, j)
        self.peca = None
        self.eh_lago = eh_lago
        
    def get_ocupante(self):
        return self.ocupante
    
    def get_peca(self):
        return self.peca
    
    def get_coordenada(self) -> tuple:
        return self.coordenada
    
    def set_peca(self, peca) -> None:
        self.peca = peca
        
    def set_ocupante(self, ocupante):
        self.ocupante = ocupante
