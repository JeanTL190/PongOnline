import pygame


class Button:
    # Inicialização dos parâmetros dos botões
    def __init__(self, text, x, y, color):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = 150
        self.height = 100

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