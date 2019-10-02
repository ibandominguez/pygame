import pygame
import constants
from sprites.player import Player

pygame.init()
pygame.display.set_caption(constants.TITLE)
screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT)) # pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
player = Player(width=135, height=115, x=200, y=400, frames_count=25)
all_sprites.add(player)


while True:
    clock.tick(constants.FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    all_sprites.update()
    screen.fill(constants.WHITE)
    all_sprites.draw(screen)
    pygame.display.flip()
