import pygame
import constants
from sprites.player import Player
from sprites.sprite import Sprite

pygame.init()
pygame.display.set_caption(constants.TITLE)
screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT)) # pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
clock = pygame.time.Clock()
rpm = 0

bike = Sprite( file_path='assets/bike.png', width=135, height=115, x=200, y=400, frames_count=25)
donuts = Sprite( file_path='assets/donuts.png', width=135, height=240, x=200, y=400, frames_count=50).set_animation_speed(35)

sprites = pygame.sprite.Group()
sprites.add(bike, donuts)

while True:
    clock.tick(constants.FPS)

    if rpm > 300: rpm = 0
    else: rpm += 0.1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    # RPM to define
    bike.set_animation_speed(rpm)

    sprites.update()
    screen.fill(constants.WHITE)
    sprites.draw(screen)
    pygame.display.flip()
