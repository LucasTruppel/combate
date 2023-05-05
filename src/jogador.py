from peca import Peca
from posicao import Posicao
from constantes import quantidade_inicial, nome_peca

class Jogador:
    
    def __init__(self) -> None:
        self.turno = True
        self.vencedor = False
        self.pecas_fora_tabuleiro = [[] for i in range(11)]
        self.nome = ""
        self.posicao_selecionada = None
        self.posicoes_alcancaveis_posicao_selecionada = []
        self.peca_selecionada = None
        self.jogador2 = False
        
    def get_turno(self) -> bool:
        return self.turno
    
    def get_posicao_selecionada(self) -> Posicao:
        return self.posicao_selecionada
    
    def get_peca_selecionada(self) -> Peca:
        return self.peca_selecionada
        
    def set_jogador2(self, eh_jogador2: bool) -> None:
        self.jogador2 = eh_jogador2
        
    def set_posicao_selecionada(self, posicao: Posicao) -> None:
        self.posicao_selecionada = posicao
        
    def set_peca_selecionada(self, peca: Peca) -> None:
        self.peca_selecionada = peca
        
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
                
    def selecionar_peca_fora_tabuleiro(self, linha: int, coluna: int) -> None:
        if len(self.pecas_fora_tabuleiro[linha + 6*coluna]) > 0:
            self.peca_selecionada = self.pecas_fora_tabuleiro[linha + 6*coluna]
        else:
            self.peca_selecionada = None
            
    def adicionar_peca_fora_tabuleiro(self, peca: Peca) -> None:
        lista_tipo_peca = self.pecas_fora_tabuleiro[peca.get_forca()]
        lista_tipo_peca.append(peca)
            
    def remover_peca_fora_tabuleiro(self, peca: Peca) -> None:
        lista_tipo_peca = self.pecas_fora_tabuleiro[peca.get_forca()]
        lista_tipo_peca.remove(peca)
            
    def verificar_lances_possiveis(self, posicao: Posicao) -> None:
        pass
    
        
        
        