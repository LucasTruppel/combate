class Peca:
    
    def __init__(self, forca: int, tipo: str, casas_por_movimento: int) -> None:
        self.forca = forca
        self.tipo = tipo
        self.casas_por_movimento = casas_por_movimento
        
    def get_forca(self) -> int:
        return self.forca
        
    def get_casas_por_movimento(self) -> int:
        return self.casas_por_movimento

    def get_tipo(self) -> str:
        return self.tipo
    