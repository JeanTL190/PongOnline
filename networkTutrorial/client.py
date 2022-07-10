import pygame
from network import Network
from button import Button

pygame.font.init()

width = 700
height = 700
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")


def redrawWindow(win, game, p, antiStress1, antiStress2):
    win.fill((128, 128, 128))
    if not(game.connected()):
        font = pygame.font.SysFont("arial", 80)
        text = font.render("Waiting for Player...", True, (255, 0, 0))
        win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
    else:
        antiStress1.draw(win)
        antiStress2.draw(win)
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

    pygame.display.update()


btns = [Button("Rock", 50, 500, (0, 0, 0)),
        Button("Scissors", 275, 500, (255, 0, 0)),
        Button("Paper", 500, 500, (0, 255, 0))
        ]


def main():
    run = True
    clock = pygame.time.Clock()
    n = Network()
    # Obtém o número do jogador
    player = int(n.getP())
    antiStress1 = n.getAnti()
    # Obtém o anti-stress
    print("You are player", player)

    while run:
        clock.tick(60)
        try:
            # Envio de solicitação de jogo
            game = n.send("get")
            # Get Anti stress;
            if player == 0:
                antiStress2 = game.get_anti_stress(1)
            else:
                antiStress2 = game.get_anti_stress(0)

        except:
            # Se não recebido de volta, não obtém um jogo
            run = False
            print("Couldn't get game")
            break

        print("1")
        print(antiStress1)
        print("2")
        print(antiStress2)

        if game.bothWent():
            redrawWindow(win, game, player, antiStress1, antiStress2)
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
            pygame.time.delay(3000)

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
                                game = n.send(btn.text)
                        else:
                            if not game.p2Went:
                                game = n.send(btn.text)

        game = n.send(antiStress1)
        if player == 0:
            antiStress2 = game.get_anti_stress(1)
        else:
            antiStress2 = game.get_anti_stress(0)
        antiStress1.move()
        redrawWindow(win, game, player, antiStress1, antiStress2)


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
