import pygame


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
        print("anti")

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
