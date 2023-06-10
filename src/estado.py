from enum import Enum


class Estado(Enum):
    NAO_COMECOU = 0
    PREPARACAO = 1
    COMBATE = 2
    FIM_DE_JOGO = 3
