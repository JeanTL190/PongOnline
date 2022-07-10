class Game:
    def __init__(self, id, antiStresses):
        # jogador fez uma jogada?
        self.p1Went = False
        self.p2Went = False
        # jogador pronto?
        self.ready = False
        # id para cada jogo
        self.id = id
        # quantas jogadas foram feitas por ambas as partes
        # vitórias e empate
        self.moves = [None, None]
        self.wins = [0, 0]
        self.ties = 0
        self.antiStresses = antiStresses
        print("Construtor")

    # Captura o anti stress especifico
    def get_anti_stress(self, p):
        return self.antiStresses[p]

    # Captura o movimento feito pelo jogador
    def get_player_move(self, p):
        """
        :param p: [0,1]
        :return: Move
        """
        return self.moves[p]

    # Atualiza a lista de movimentos quando o jogador faz um
    def play(self, player, move):
        self.moves[player] = move
        if player == 0:
            self.p1Went = True
        else:
            self.p2Went = True

    # Retorna se os jogadores estão conectados ao jogo
    def connected(self):
        return self.ready

    # Retorna se os jogadores já jogaram
    def bothWent(self):
        return self.p1Went and self.p2Went

    # Retorna o vencedor
    def winner(self):
        # Busca a palavra relacionada à opção escolhida
        p1 = self.moves[0]
        p2 = self.moves[1]

        winner = -1
        if p1 == "Rock" and p2 == "Scissors":
            winner = 0
        elif p1 == "Scissors" and p2 == "Rock":
            winner = 1
        elif p1 == "Paper" and p2 == "Rock":
            winner = 0
        elif p1 == "Rock" and p2 == "Paper":
            winner = 1
        elif p1 == "Scissors" and p2 == "Paper":
            winner = 0
        elif p1 == "Paper" and p2 == "Scissors":
            winner = 1

        return winner

    # Retorna que o jogador está disponível pra jogar
    def resetWent(self):
        self.p1Went = False
        self.p2Went = False
