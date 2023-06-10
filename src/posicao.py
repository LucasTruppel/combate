class Posicao:
    
    def __init__(self, ocupante, i: int, j: int, peca, eh_lago: bool) -> None:
        self.ocupante = ocupante
        self.coordenada = (i, j)
        self.peca = peca
        self.eh_lago = eh_lago
        
    def get_ocupante(self):
        return self.ocupante
    
    def get_peca(self):
        return self.peca
    
    def get_coordenada(self) -> tuple:
        return self.coordenada

    def get_eh_lago(self) -> bool:
        return self.eh_lago
    
    def set_peca(self, peca) -> None:
        self.peca = peca
        
    def set_ocupante(self, ocupante) -> None:
        self.ocupante = ocupante

    def ocupar(self, peca, jogador) -> None:
        self.peca = peca
        self.ocupante = jogador

    def desocupar(self) -> None:
        self.peca = None
        self.ocupante = None
