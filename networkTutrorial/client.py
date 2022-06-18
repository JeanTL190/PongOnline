import pygame
from network import Network
pygame.font.init()

width = 700
height = 700
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")


class AntiStress:
    # Inicialização dos parâmetros do objeto antiestresse
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.color = color
        self.width = 50
        self.height = 50
        self.rect = (x, y, width, height)
        self.vel = 3

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x -= self.vel
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x += self.vel
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.y -= self.vel
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.y += self.vel

        self.update()

    def update(self):
        # Atualiza a posição do antiestresse
        self.rect = (self.x, self.y, self.width, self.height)


class Button:
    # Inicialização dos parâmetros dos botões
    def __init__(self, text, x, y, color):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = 150
        self.height = 100
        self.btn = (x, y, width, height)
        self.vel = 3

    # Aparência dos botões
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("arial", 40)
        text = font.render(self.text, True, (255, 255, 255))
        win.blit(text,
                 (self.x + round(self.width/2) - round(text.get_width()/2),
                  self.y + round(self.height/2) - round(text.get_height()/2)))

    # Configuração do click nos botões
    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False


def redrawWindow(win, game, p, anti):
    win.fill((128, 128, 128))

    if not(game.connected()):
        font = pygame.font.SysFont("arial", 80)
        text = font.render("Waiting for Player...", True, (255, 0, 0))
        win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
    else:
        font = pygame.font.SysFont("arial", 60)
        text = font.render("Your Move", True, (0, 255, 255))
        win.blit(text, (80, 200))

        text = font.render("Opponents", True, (0, 255, 255))
        win.blit(text, (380, 200))

        move1 = game.get_player_move(0)
        move2 = game.get_player_move(1)
        if game.bothWent():
            text1 = font.render(move1, True, (0, 0, 0))
            text2 = font.render(move2, True, (0, 0, 0))
        else:
            if game.p1Went and p == 0:
                text1 = font.render(move1, True, (0, 0, 0))
            elif game.p1Went:
                text1 = font.render("Locked In", True, (0, 0, 0))
            else:
                text1 = font.render("Waiting...", True, (0, 0, 0))

            if game.p2Went and p == 1:
                text2 = font.render(move2, True, (0, 0, 0))
            elif game.p2Went:
                text2 = font.render("Locked In", True, (0, 0, 0))
            else:
                text2 = font.render("Waiting...", True, (0, 0, 0))

        if p == 1:
            win.blit(text2, (100, 350))
            win.blit(text1, (400, 350))
        else:
            win.blit(text1, (100, 350))
            win.blit(text2, (400, 350))

        for btn in btns:
            btn.draw(win)

        anti.draw(win)

    pygame.display.update()


btns = [Button("Rock", 50, 500, (0, 0, 0)),
        Button("Scissors", 250, 500, (255, 0, 0)),
        Button("Paper", 450, 500, (0, 255, 0))
        ]


def main():
    run = True
    clock = pygame.time.Clock()
    n = Network()
    # Obtém o número do jogador
    player = int(n.getP())
    print("You are player", player)

    anti = AntiStress(50, 50, width, height, (0, 0, 255))

    while run:
        clock.tick(60)
        try:
            # Envio de solicitação de jogo
            game = n.send("get")
        except:
            # Se não recebido de volta, não obtém um jogo
            run = False
            print("Couldn't get game")
            break

        if game.bothWent():
            redrawWindow(win, game, player, anti)
            pygame.time.delay(500)
            try:
                # Se ambos os jogadores já jogaram, envia o reset
                game = n.send("reset")
            except:
                run = False
                print("Couldn't get game")
                break

            # Determina o resultado do jogo
            font = pygame.font.SysFont("arial", 90)
            if (game.winner() == 1 and player == 1) or (game.winner() == 0 and player == 0):
                text = font.render("You Won!", True, (255, 0, 0))
            elif game.winner() == -1:
                text = font.render("Tie Game!", True, (255, 0, 0))
            else:
                text = font.render("You Lost...", True, (255, 0, 0))

            win.blit(text, (width/2 - text.get_width()/2, height/8 - text.get_height()/8))
            pygame.display.update()
            pygame.time.delay(2000)

        for event in pygame.event.get():
            # Comportamento do botão de fechar
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            # Comportamento do clique
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for btn in btns:
                    if btn.click(pos) and game.connected():
                        if player == 0:
                            if not game.p1Went:
                                n.send(btn.text)
                        else:
                            if not game.p2Went:
                                n.send(btn.text)

        anti.move()
        redrawWindow(win, game, player, anti)


def menu_screen():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        win.fill((128, 128, 128))
        font = pygame.font.SysFont("arial", 60)
        text = font.render("Click to Play!", True, (255, 0, 0))
        win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False

    main()


while True:
    menu_screen()
