import pygame
import constants

from sprite import Sprite

pygame.init()
pygame.display.set_caption(constants.TITLE)

"""
Specific size: pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
Full screen: pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
Monitor size: pygame.display.set_mode((monitor.current_w, monitor.current_h))
"""
monitor = pygame.display.Info()
screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
clock = pygame.time.Clock()
rpm = 0
running = True

background = pygame.image.load('assets/background.png')
road = Sprite(file_path='assets/road.png', width=270, height=480, x=constants.WIDTH / 2, y=constants.HEIGHT, frames_count=35).set_animation_speed(35)
bike = Sprite(file_path='assets/bike.png', width=135, height=115, x=constants.WIDTH / 2, y=constants.HEIGHT, frames_count=25)
donuts = Sprite(file_path='assets/donuts.png', width=135, height=240, x=constants.WIDTH / 2, y=constants.HEIGHT, frames_count=50).set_animation_speed(35)

sprites = pygame.sprite.Group()
sprites.add(road, bike, donuts)

while running:
    clock.tick(constants.FPS)

    if rpm > 200: rpm = 0
    else: rpm += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    road.set_animation_speed(int(rpm))
    bike.set_animation_speed(int(rpm))

    sprites.update()
    screen.fill((73, 61, 116))
    screen.blit(background, (0, 0))

    sprites.draw(screen)
    pygame.display.flip()

pygame.quit()
