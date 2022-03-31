import pygame
import os
import random
import math

pygame.init()

width = 600
height = 600
screen = pygame.display.set_mode((width, height))


def write(text, x, y, size):
    font = pygame.font.SysFont("Arial", size)
    rend = font.render(text, True, (255, 100, 100))
    screen.blit(rend, (x, y))


what_shows = 'MENU'


class Obstacle:
    def __init__(self, x, wide):
        self.x = x
        self.wide = wide
        self.y_up = 0
        self.h_up = random.randint(150, 250)
        self.gap = 200
        self.y_down = self.h_up + self.gap
        self.h_down = height - self.y_down
        self.colour = (52, 140, 235)
        self.shape_up = pygame.Rect(self.x, self.y_up, self.wide, self.h_up)
        self.shape_down = pygame.Rect(self.x, self.y_down, self.wide, self.h_down)

    def draw(self):
        pygame.draw.rect(screen, self.colour, self.shape_up, 0)
        pygame.draw.rect(screen, self.colour, self.shape_down, 0)

    def movement(self, v):  # v = speed of obstacle
        self.x = self.x - v
        self.shape_up = pygame.Rect(self.x, self.y_up, self.wide, self.h_up)
        self.shape_down = pygame.Rect(self.x, self.y_down, self.wide, self.h_down)

    def collision(self, player):
        if self.shape_up.colliderect(player) or self.shape_down.colliderect(player):
            return True
        else:
            return False


class Helicopter:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.height = 10
        self.width = 50
        self.shape = pygame.Rect(self.x, self.y, self.width, self.height)
        self.image = pygame.image.load(os.path.join('heli.png'))

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

    def movement(self, v):
        self.y = self.y + v
        self.shape = pygame.Rect(self.x, self.y, self.width, self.height)


obstacles = []
for i in range(21):
    obstacles.append(Obstacle(i*width/20, width/20))

player = Helicopter(250, 275)

dy = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                dy = -0.1
            if event.key == pygame.K_DOWN:
                dy = 0.1
            if event.key == pygame.K_SPACE:
                if what_shows != "Game":
                    player = Helicopter(250, 275)
                    dy = 0
                    what_shows = "Game"
                    points = 0

    screen.fill((0, 0, 0))
    if what_shows == 'MENU':
        write("Press space to begin", 80, 150, 20)
        logo = pygame.image.load(os.path.join('logo.png'))
        screen.blit(logo, (200, 200))
    elif what_shows == "Game":
        for p in obstacles:
            p.movement(1)
            p.draw()
            if p.collision(player.shape):
                what_shows = "Game Over"
        for p in obstacles:
            if p.x <= -p.wide:
                obstacles.remove(p)
                obstacles.append((Obstacle(width, width/20)))
                points = points + math.fabs(dy)
        player.draw()
        player.movement(dy)
        write(str(points), 50, 50, 20)
    elif what_shows == "Game Over":
        logo = pygame.image.load(os.path.join('logo.png'))
        screen.blit(logo, (200, 200))
        write("Game Over", 50, 350, 20)
        write("Your score is: " + str(round(points, 2)), 50, 380, 20)
        write("Press space to play again", 50, 410, 20)

    pygame.display.update()
