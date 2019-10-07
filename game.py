import pygame
import constants

from controller import Controller
from sprite import Sprite

pygame.init()
pygame.font.init()
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
game_controller = Controller()

"""
Graphics, texts, sprites
"""
background = pygame.image.load('assets/background.png')
debug_text = pygame.font.SysFont('Roboto', 30)
road = Sprite(file_path='assets/road.png', width=270, height=480, x=constants.WIDTH / 2, y=550, frames_count=35).set_animation_speed(35)
bike = Sprite(file_path='assets/bike.png', width=135, height=115, x=constants.WIDTH / 2, y=constants.HEIGHT, frames_count=25)
donuts = Sprite(file_path='assets/donuts.png', width=135, height=240, x=constants.WIDTH / 2, y=constants.HEIGHT, frames_count=50).set_animation_speed(35)

sprites = pygame.sprite.Group()
sprites.add(road, bike, donuts)

while running:
    clock.tick(constants.FPS)

    if rpm > 200: rpm = 0
    else: rpm += 0.5

    """
    Game Logic, based on timing and playing
    """
    if game_controller.is_standing_by():
        pass
    elif game_controller.is_playing():
        pass
    elif game_controller.is_resuming():
        pass

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    road.set_animation_speed(int(rpm))
    bike.set_animation_speed(int(rpm))

    sprites.update()
    screen.fill((73, 61, 116))
    screen.blit(background, ((constants.WIDTH / 2) - 216, 0))
    screen.blit(debug_text.render(str(rpm), False, (0, 0, 0)), (15, 15))

    sprites.draw(screen)
    pygame.display.flip()

pygame.quit()
