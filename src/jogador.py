from peca import Peca
from constantes import quantidade_inicial, nome_peca

class Jogador:
    
    def __init__(self) -> None:
        self.turno = True
        self.vencedor = False
        self.pecas_fora_tabuleiro = [[] for i in range(11)]
        self.nome = ""
        self.posicao_selecionada = None
        self.posicoes_alcancaveis_posicao_selecionada = []
        self.peca_selecionada = []
        self.jogador2 = False
        
    def get_turno(self) -> bool:
        return self.turno
    
    def get_posicao_selecionada(self) -> bool:
        return self.posicao_selecionada
    
    def get_peca_selecionada(self) -> bool:
        return self.peca_selecionada
        
    def set_jogador2(self, eh_jogador2: bool) -> None:
        self.jogador2 = eh_jogador2
        
    def instanciar_pecas(self) -> None:
        for forca in range(11):
            for quantidade in range(quantidade_inicial[forca]):
                if forca == 0 or forca == 12:
                    casas_por_movimento = 0
                elif forca == 2:
                    casas_por_movimento = 9
                else:
                    casas_por_movimento = 1
                self.pecas_fora_tabuleiro[forca].append(Peca(forca, nome_peca[forca], casas_por_movimento))
    
        
        
        