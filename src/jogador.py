from peca import Peca
from posicao import Posicao
from constantes import quantidade_inicial, nome_peca


class Jogador:
    
    def __init__(self) -> None:
        self.turno = False
        self.vencedor = False
        self.pecas_fora_tabuleiro = []
        self.posicao_selecionada = None
        self.posicoes_alcancaveis_posicao_selecionada = []
        self.peca_selecionada = None
        self.jogador2 = False
    
    def get_posicoes_alcancaveis_posicao_selecionada(self) -> list:
        return self.posicoes_alcancaveis_posicao_selecionada
        
    def get_turno(self) -> bool:
        return self.turno
    
    def get_posicao_selecionada(self) -> Posicao:
        return self.posicao_selecionada
    
    def get_peca_selecionada(self) -> Peca:
        return self.peca_selecionada
    
    def get_pecas_fora_tabuleiro(self) -> list:
        return self.pecas_fora_tabuleiro
    
    def get_quantidade_pecas_fora_tabuleiro(self) -> list:
        quantidades = []
        for lista_pecas in self.pecas_fora_tabuleiro:
            quantidades.append(len(lista_pecas))
        return quantidades
     
    def get_jogador2(self) -> bool:
        return self.jogador2

    def get_vencedor(self) -> bool:
        return self.vencedor
       
    def set_jogador2(self, eh_jogador2: bool) -> None:
        self.jogador2 = eh_jogador2
        
    def set_posicao_selecionada(self, posicao: Posicao) -> None:
        self.posicao_selecionada = posicao
        
    def set_peca_selecionada(self, peca: Peca) -> None:
        self.peca_selecionada = peca

    def set_posicoes_alcancaveis_posicao_selecionada(self, posicoes: list) -> None:
        self.posicoes_alcancaveis_posicao_selecionada = posicoes

    def set_vencedor(self, eh_vencedor: bool) -> None:
        self.vencedor = eh_vencedor

    def set_pecas_fora_tabuleiro(self, pecas_fora_tabuleiro: list) -> None:
        self.pecas_fora_tabuleiro = pecas_fora_tabuleiro
        
    def instanciar_pecas(self) -> None:
        self.pecas_fora_tabuleiro = [[] for _ in range(12)]
        for forca in range(12):
            for quantidade in range(quantidade_inicial[forca]):
                if forca == 0 or forca == 11:
                    casas_por_movimento = 0
                elif forca == 2:
                    casas_por_movimento = 9
                else:
                    casas_por_movimento = 1
                self.pecas_fora_tabuleiro[forca].append(Peca(forca, nome_peca[forca], casas_por_movimento))
                
    def selecionar_peca_fora_tabuleiro(self, linha: int, coluna: int) -> None:
        if len(self.pecas_fora_tabuleiro[linha + 6*coluna]) > 0:
            self.peca_selecionada = self.pecas_fora_tabuleiro[linha + 6*coluna][0]
        else:
            self.peca_selecionada = None
            
    def adicionar_peca_fora_tabuleiro(self, peca: Peca) -> None:
        lista_tipo_peca = self.pecas_fora_tabuleiro[peca.get_forca()]
        lista_tipo_peca.append(peca)
            
    def remover_peca_fora_tabuleiro(self, peca: Peca) -> None:
        lista_tipo_peca = self.pecas_fora_tabuleiro[peca.get_forca()]
        lista_tipo_peca.remove(peca)

    def inverter_turno(self) -> None:
        self.turno = not self.turno

    def reiniciar(self) -> None:
        self.turno = False
        self.vencedor = False
        self.posicao_selecionada = None
        self.posicoes_alcancaveis_posicao_selecionada = []
        self.peca_selecionada = None
