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
show_donuts_ticks = 0
game_controller = Controller()

"""
Graphics, texts, sprites
"""
sign = pygame.image.load('./assets/sign.png').convert_alpha()
background = pygame.image.load('./assets/background.png').convert_alpha()
debug_text = pygame.font.SysFont(pygame.font.get_default_font(), 20)
road = Sprite(file_path='./assets/road.png', width=270, height=480, x=constants.WIDTH / 2, y=495, frames_count=34)
bike = Sprite(file_path='./assets/bike.png', width=108, height=192, x=constants.WIDTH / 2, y=constants.HEIGHT, frames_count=50)
donuts = Sprite(file_path='./assets/donuts.png', width=135, height=240, x=constants.WIDTH / 2, y=constants.HEIGHT, frames_count=50)

sprites = pygame.sprite.Group()
sprites.add(road, bike, donuts)


while running:
    clock.tick(constants.FPS)

    """
    KeyControl
    """
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and rpm < 500: rpm += 1
    if keys[pygame.K_DOWN] and rpm > 0: rpm -= 1

    """
    Game Logic, based on timing and playing
    """
    if game_controller.is_standing_by() and rpm > 0:
        game_controller.start()
    elif game_controller.is_playing():
        if game_controller.get_time() % 10 == 0: show_donuts_ticks += 5
        if show_donuts_ticks > 0:
            donuts.set_animation_speed(35)
            show_donuts_ticks -= 1
        else:
            donuts.set_animation_speed(0)
    elif game_controller.is_resuming():
        if rpm > 0: rpm -= 1
    elif game_controller.is_finished():
        rpm = 0
        game_controller.end()
        donuts.set_animation_speed(0)
        show_donuts_ticks = 0

    """
    Handle Pygame Events
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    """
    Screen updates
    Sprites actions
    """
    road.set_animation_speed(rpm)
    bike.set_animation_speed(rpm)

    screen.fill((73, 61, 116))
    screen.blit(background, ((constants.WIDTH / 2) - 244, 0))
    screen.blit(sign, (0, 150))
    screen.blit(pygame.transform.flip(sign, True, False), (constants.WIDTH - 128, 150))
    screen.blit(debug_text.render("{} rpm".format(rpm), False, pygame.Color('white')), (60, 198))
    screen.blit(debug_text.render(str(game_controller.GAME_DURATION - game_controller.get_time()) if game_controller.is_playing() else game_controller.get_state(), False, pygame.Color('white')), (constants.WIDTH - 100, 198))

    sprites.update()
    sprites.draw(screen)
    pygame.display.flip()


pygame.quit()
