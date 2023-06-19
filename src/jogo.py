from estado import Estado
from tabuleiro import *
from imageminterface import ImagemInterface


class Jogo:

    def __init__(self) -> None:
        self.estado = Estado.NAO_COMECOU
        self.tabuleiro = Tabuleiro()
        self.jogador_local = Jogador()
        self.jogador_remoto = Jogador()
        self.exercito_adversario_recebido = False
        self.exercito_enviado = False
        self.mensagem = "Clique em iniciar partida para jogar!"

    def get_estado(self):
        return self.estado

    def inicializar(self) -> None:
        self.tabuleiro.iniciar_tabuleiro()
        self.jogador_local.instanciar_pecas()
        self.jogador_remoto.instanciar_pecas()

    def comecar_partida(self) -> None:
        self.jogador_local.set_jogador2(False)
        self.jogador_remoto.set_jogador2(True)
        self.continuar_inicio()

    def receber_inicio(self) -> None:
        self.jogador_remoto.set_jogador2(False)
        self.jogador_local.set_jogador2(True)
        self.continuar_inicio()

    def continuar_inicio(self) -> None:
        if self.estado == Estado.FIM_DE_JOGO:
            self.reiniciar()
        self.estado = Estado.PREPARACAO
        self.mensagem = "Posicione suas peças e clique em terminar preparação!"

    def receber_desistencia(self) -> None:
        self.estado = Estado.FIM_DE_JOGO
        self.mensagem = f"Seu oponente desistiu. Você venceu a partida!"

    def finalizar(self, acabaram_pecas: bool = False) -> None:
        self.estado = Estado.FIM_DE_JOGO
        if not acabaram_pecas:
            resultado = "venceu" if self.jogador_local.get_vencedor() else "perdeu"
            self.mensagem = f"Bandeira capturada! Você {resultado} a partida."
        else:
            if not self.jogador_local.get_vencedor() and not self.jogador_remoto.get_vencedor():
                self.mensagem = "Ambos jogadores sem peças móveis. Empate."
            elif self.jogador_local.get_vencedor():
                self.mensagem = "As peças móveis do adversário acabaram. Você venceu a partida."
            else:
                self.mensagem = "Suas peças móveis acabaram. Você perdeu a partida."

    def reiniciar(self) -> None:
        for i in range(10):
            for j in range(10):
                posicao = self.tabuleiro.get_posicao(i, j)
                jogador = posicao.get_ocupante()
                peca = posicao.get_peca()
                if peca is not None:
                    jogador.adicionar_peca_fora_tabuleiro(peca)
                    posicao.desocupar()
        self.jogador_local.reiniciar()
        self.jogador_remoto.reiniciar()
        self.resetar()
    
    def resetar(self) -> None:
        self.exercito_adversario_recebido = False
        self.exercito_enviado = False

    def obter_status(self) -> ImagemInterface:
        tabuleiro_int = [[-1 for _ in range(10)] for _ in range(10)]
        for i in range(10):
            for j in range(10):
                posicao = self.tabuleiro.get_posicao(i, j)
                peca = self.tabuleiro.get_posicao(i, j).get_peca()
                if peca is not None:
                    if posicao.get_ocupante() == self.jogador_local:
                        tabuleiro_int[i][j] = peca.get_forca()
                    elif self.estado == Estado.COMBATE or self.estado == Estado.FIM_DE_JOGO:
                        tabuleiro_int[i][j] = 12

        posicoes_selecionadas = [[0 for _ in range(10)] for _ in range(10)]
        posicao_selecionada = self.jogador_local.get_posicao_selecionada()
        if posicao_selecionada is not None:
            linha, coluna = posicao_selecionada.get_coordenada()
            posicoes_selecionadas[linha][coluna] = 1
            for i, j in self.jogador_local.get_posicoes_alcancaveis_posicao_selecionada():
                posicoes_selecionadas[i][j] = 2

        # Peça de fora do tabuleiro selecionada
        peca_selecionada = self.jogador_local.get_peca_selecionada()
        forca_peca_selecionada = -1
        if peca_selecionada is not None:
            forca_peca_selecionada = peca_selecionada.get_forca()

        if self.estado != Estado.COMBATE:
            turno = ""
        else:
            turno = "Seu turno!" if self.jogador_local.get_turno() else "Turno do adversário."

        return ImagemInterface(self.mensagem, turno, tabuleiro_int, forca_peca_selecionada, posicoes_selecionadas,
                               self.jogador_local.get_quantidade_pecas_fora_tabuleiro())

    def selecionar_posicao(self, linha: int, coluna: int, peca_fora_tabuleiro: bool) -> dict:
        jogada = {}
        turno = self.jogador_local.get_turno()
        if (self.estado == Estado.PREPARACAO and not self.exercito_enviado) or (self.estado == Estado.COMBATE and turno):
            posicao_selecionada = self.jogador_local.get_posicao_selecionada()
            peca_selecionada = self.jogador_local.get_peca_selecionada()

            if posicao_selecionada is None and peca_selecionada is None:
                self.selecionar_origem(linha, coluna, peca_fora_tabuleiro)
            else:
                jogada = self.selecionar_destino(linha, coluna)
        return jogada

    def selecionar_origem(self, linha: int, coluna: int, peca_fora_tabuleiro: bool) -> None:
        if peca_fora_tabuleiro and self.estado == Estado.PREPARACAO:
            self.jogador_local.selecionar_peca_fora_tabuleiro(linha, coluna)
        else:
            posicao = self.tabuleiro.get_posicao(linha, coluna)
            jogador = posicao.get_ocupante()
            peca = posicao.get_peca()
            if peca is not None and jogador == self.jogador_local:
                casas_por_movimento = peca.get_casas_por_movimento()
                if casas_por_movimento > 0 or self.estado == Estado.PREPARACAO:
                    self.jogador_local.set_posicao_selecionada(posicao)
                    if self.estado == Estado.COMBATE:
                        self.tabuleiro.verificar_lances_possiveis(posicao, self.jogador_local)

    def selecionar_destino(self, linha: int, coluna: int) -> dict:
        jogada = {}
        peca_selecionada = self.jogador_local.get_peca_selecionada()
        posicao_origem = self.jogador_local.get_posicao_selecionada()
        peca_origem = None
        if posicao_origem is not None:
            peca_origem = posicao_origem.get_peca()
        posicao_destino = self.tabuleiro.get_posicao(linha, coluna)
        peca_destino = posicao_destino.get_peca()

        if self.estado == Estado.PREPARACAO:
            if peca_selecionada is not None:
                if peca_destino is None and 6 <= linha < 10:
                    posicao_destino.ocupar(peca_selecionada, self.jogador_local)
                    self.jogador_local.remover_peca_fora_tabuleiro(peca_selecionada)
                    self.jogador_local.set_peca_selecionada(None)
                else:
                    self.jogador_local.set_peca_selecionada(None)
            else:
                if posicao_origem == posicao_destino:
                    posicao_destino.desocupar()
                    self.jogador_local.adicionar_peca_fora_tabuleiro(peca_origem)
                    self.jogador_local.set_posicao_selecionada(None)
                else:
                    self.jogador_local.set_posicao_selecionada(None)
        else:
            if (linha, coluna) in self.jogador_local.get_posicoes_alcancaveis_posicao_selecionada():
                if peca_destino is not None:
                    self.comparar_pecas(peca_origem, peca_destino, linha, coluna, jogada)
                else:
                    posicao_destino.ocupar(peca_origem, self.jogador_local)
                    self.mensagem = f"Seu {peca_origem.get_tipo()} se moveu."
                    jogada["info_combate_pecas"] = 0
                    jogada["bandeira_capturada"] = False
                posicao_origem.desocupar()
                self.jogador_local.set_posicao_selecionada(None)
                self.jogador_local.set_posicoes_alcancaveis_posicao_selecionada([])
                self.jogador_local.inverter_turno()
                jogada["preparacao"] = False
                jogada["lance_preparacao"] = None
                jogada["lance_combate"] = [posicao_origem.get_coordenada(), posicao_destino.get_coordenada()]
                self.avaliar_fim_pecas(jogada)
                if not jogada["bandeira_capturada"] and jogada["info_fim_pecas"] == 0:
                    jogada["match_status"] = "next"
                else:
                    jogada["match_status"] = "finished"
                self.espelhar_jogada(jogada)
            else:
                self.jogador_local.set_posicao_selecionada(None)
                self.jogador_local.set_posicoes_alcancaveis_posicao_selecionada([])
        return jogada

    def inverter_posicao(self, coordenadas: tuple) -> tuple:
        i, j = coordenadas
        return 9 - i, 9 - j
    
    def espelhar_jogada(self, jogada: dict) -> dict:
        if jogada["preparacao"]:
            matriz = [[-1 for _ in range(10)] for _ in range(10)]
            for i in range(6, 10):
                for j in range(10):
                    peca = self.tabuleiro.get_posicao(i, j).get_peca()
                    matriz[9 - i][9 - j] = peca.get_forca()
            jogada["lance_preparacao"] = matriz
        else:
            jogada["lance_combate"][0] = self.inverter_posicao(jogada["lance_combate"][0])
            jogada["lance_combate"][1] = self.inverter_posicao(jogada["lance_combate"][1])
        return jogada
        
    def terminar_preparacao(self) -> dict:
        jogada = {}
        if self.estado == Estado.PREPARACAO and self.tabuleiro.campo_esta_pronto():
            self.exercito_enviado = True
            jogada["preparacao"] = True
            jogada["bandeira_capturada"] = False
            jogada["adversario_venceu_combate_pecas"] = False
            jogada["lance_combate"] = None
            jogada["match_status"] = "next"
            jogada = self.espelhar_jogada(jogada)
            
            if self.exercito_adversario_recebido:
                self.iniciar_combate()
            else:
                self.mensagem = "Aguardando oponente"
        return jogada
            
    def receber_jogada(self, jogada: dict) -> None:
        if bool(jogada["preparacao"]):
            self.exercito_adversario_recebido = True
            self.tabuleiro.alocar_pecas_adversario(jogada["lance_preparacao"], self.jogador_remoto)
            if self.exercito_enviado:
                self.iniciar_combate()
        elif bool(jogada["bandeira_capturada"]):
            self.atualizar_tabuleiro(jogada)
            self.jogador_remoto.set_vencedor(True)
            self.finalizar()
        elif int(jogada["info_fim_pecas"]) != 0:
            self.atualizar_tabuleiro(jogada)
            if int(jogada["info_fim_pecas"]) == 1:
                self.jogador_remoto.set_vencedor(True)
            elif int(jogada["info_fim_pecas"]) == 2:
                self.jogador_local.set_vencedor(True)
            self.finalizar(acabaram_pecas=True)
        else:
            self.atualizar_tabuleiro(jogada)
            self.jogador_local.inverter_turno()

    def iniciar_combate(self) -> None:
        self.estado = Estado.COMBATE
        if not self.jogador_local.get_jogador2():
            self.jogador_local.inverter_turno()
        self.mensagem = "Combate iniciado!"

    def alocar_rapidamente(self) -> None:
        self.tabuleiro.alocar_rapidamente(self.jogador_local)

    def comparar_pecas(self, peca_local: Peca, peca_remoto: Peca, linha: int, coluna: int, jogada: dict):
        tipo_local = peca_local.get_tipo()
        tipo_remoto = peca_remoto.get_tipo()
        forca_local = peca_local.get_forca()
        forca_remoto = peca_remoto.get_forca()
        posicao_destino = self.tabuleiro.get_posicao(linha, coluna)

        jogada["bandeira_capturada"] = False

        if tipo_remoto == "Bandeira":
            self.jogador_remoto.adicionar_peca_fora_tabuleiro(peca_remoto)
            posicao_destino.ocupar(peca_local, self.jogador_local)
            self.jogador_local.set_vencedor(True)
            self.finalizar()
            jogada["info_combate_pecas"] = 1
            jogada["bandeira_capturada"] = True
        elif tipo_remoto == "Explosivo":
            if tipo_local == "Cabo":
                self.jogador_remoto.adicionar_peca_fora_tabuleiro(peca_remoto)
                posicao_destino.ocupar(peca_local, self.jogador_local)
                jogada["info_combate_pecas"] = 1
            else:
                self.jogador_local.adicionar_peca_fora_tabuleiro(peca_local)
                self.jogador_remoto.adicionar_peca_fora_tabuleiro(peca_remoto)
                posicao_destino.desocupar()
                jogada["info_combate_pecas"] = 3
        elif tipo_local == "Espião":
            if tipo_remoto == "General":
                self.jogador_remoto.adicionar_peca_fora_tabuleiro(peca_remoto)
                posicao_destino.ocupar(peca_local, self.jogador_local)
                jogada["info_combate_pecas"] = 1
            elif tipo_remoto == "Espião":
                self.jogador_local.adicionar_peca_fora_tabuleiro(peca_local)
                self.jogador_remoto.adicionar_peca_fora_tabuleiro(peca_remoto)
                posicao_destino.desocupar()
                jogada["info_combate_pecas"] = 3
            else:
                self.jogador_local.adicionar_peca_fora_tabuleiro(peca_local)
                jogada["info_combate_pecas"] = 2
        else:
            if forca_local > forca_remoto:
                self.jogador_remoto.adicionar_peca_fora_tabuleiro(peca_remoto)
                posicao_destino.ocupar(peca_local, self.jogador_local)
                jogada["info_combate_pecas"] = 1
            elif forca_local < forca_remoto:
                self.jogador_local.adicionar_peca_fora_tabuleiro(peca_local)
                jogada["info_combate_pecas"] = 2
            else:
                self.jogador_local.adicionar_peca_fora_tabuleiro(peca_local)
                self.jogador_remoto.adicionar_peca_fora_tabuleiro(peca_remoto)
                posicao_destino.desocupar()
                jogada["info_combate_pecas"] = 3

        if not jogada["bandeira_capturada"]:
            texto_vencedor = {1: "você!", 2: "adversário!", 3: "nenhum!"}
            self.mensagem = f'Seu {peca_local.get_tipo()} atacou um {peca_remoto.get_tipo()} do adversário. ' \
                            f'Vencedor: {texto_vencedor[jogada["info_combate_pecas"]]}'

    def avaliar_fim_pecas(self, jogada: dict):
        jogada["info_fim_pecas"] = 0
        acabaram_pecas_local = self.tabuleiro.pecas_moveis_acabaram(self.jogador_local)
        acabaram_pecas_remoto = self.tabuleiro.pecas_moveis_acabaram(self.jogador_remoto)
        if acabaram_pecas_local and acabaram_pecas_remoto:
            jogada["info_fim_pecas"] = 3
            self.finalizar(acabaram_pecas=True)
        elif acabaram_pecas_local:
            jogada["info_fim_pecas"] = 2
            self.jogador_remoto.set_vencedor(True)
            self.finalizar(acabaram_pecas=True)
        elif acabaram_pecas_remoto:
            jogada["info_fim_pecas"] = 1
            self.jogador_local.set_vencedor(True)
            self.finalizar(acabaram_pecas=True)

    def atualizar_tabuleiro(self, jogada: dict) -> None:
        x, y = jogada["lance_combate"][0]
        w, z = jogada["lance_combate"][1]
        posicao_origem = self.tabuleiro.get_posicao(x, y)
        posicao_destino = self.tabuleiro.get_posicao(w, z)
        peca_origem = posicao_origem.get_peca()
        peca_destino = posicao_destino.get_peca()
        if jogada["info_combate_pecas"] == 0:
            posicao_destino.ocupar(peca_origem, self.jogador_remoto)
            self.mensagem = "Uma peça do adversário se moveu."
        elif jogada["info_combate_pecas"] == 1:
            posicao_destino.ocupar(peca_origem, self.jogador_remoto)
            self.jogador_local.adicionar_peca_fora_tabuleiro(peca_destino)
            self.mensagem = f"Seu {peca_destino.get_tipo()} foi atacado por um {peca_origem.get_tipo()} do " \
                            f"adversário. Vencedor: adversário."
        elif jogada["info_combate_pecas"] == 2:
            self.jogador_remoto.adicionar_peca_fora_tabuleiro(peca_origem)
            self.mensagem = f"Seu {peca_destino.get_tipo()} foi atacado por um {peca_origem.get_tipo()} do " \
                            f"adversário. Vencedor: você."
        elif jogada["info_combate_pecas"] == 3:
            posicao_destino.desocupar()
            self.jogador_remoto.adicionar_peca_fora_tabuleiro(peca_origem)
            self.jogador_local.adicionar_peca_fora_tabuleiro(peca_destino)
            self.mensagem = f"Seu {peca_destino.get_tipo()} foi atacado por um {peca_origem.get_tipo()} do " \
                            f"adversário. Vencedor: nenhum."
        posicao_origem.desocupar()
