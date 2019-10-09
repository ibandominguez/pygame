import os
import time
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
counter = 0
start = 0
end = 0
monitor = pygame.display.Info()
screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
clock = pygame.time.Clock()
rpm = 0
running = True
show_donuts_ticks = 0
game_controller = Controller()

"""
Sensor setup
Only in RPI
"""
def calculate(channel):
    global counter
    global rpm
    global start
    global end

    counter = counter + 1
    end = time.time()
    rpm = int((1.0 / (end - start)) * 60.0)
    start = time.time()

try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(2, GPIO.IN)
    GPIO.setup(3, GPIO.OUT)
    GPIO.output(3, False)
    GPIO.add_event_detect(2, GPIO.RISING, callback=calculate, bouncetime=30)
except Exception as e:
    print('RPI module not found, Sensor not initialized')

"""
Graphics, texts, sprites
"""
sign = pygame.image.load(os.getcwd() + '/assets/sign.png').convert_alpha()
background = pygame.image.load(os.getcwd() + '/assets/background.png').convert_alpha()
debug_text = pygame.font.SysFont(pygame.font.get_default_font(), 20)
road = Sprite(file_path=os.getcwd() + '/assets/road.png', width=constants.WIDTH, height=constants.HEIGHT, x=0, y=0, frames_tile=(17, 2), frames_total=34)
bike = Sprite(file_path=os.getcwd() + '/assets/bike.png', width=constants.WIDTH, height=constants.HEIGHT, x=0, y=0, frames_tile=(5, 10), frames_total=50)
donuts = Sprite(file_path=os.getcwd() + '/assets/donuts.png', width=constants.WIDTH, height=constants.HEIGHT, x=0, y=0, frames_tile=(5, 10), frames_total=50)
scoreboard = pygame.image.load(os.getcwd() + '/assets/scoreboard.png').convert_alpha()

sprites = pygame.sprite.Group()
if os.uname()[4][:3] == 'arm': sprites.add(donuts, bike, road) # rpi
else: sprites.add(road, bike, donuts) # Laptod

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
        donuts.set_animation_speed(0)
        show_donuts_ticks = 0
    elif game_controller.is_finished():
        rpm = 0
        game_controller.end()

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
    screen.blit(background, (0, 0))
    screen.blit(sign, (0, 250))
    screen.blit(pygame.transform.flip(sign, True, False), (constants.WIDTH - 128, 250))
    screen.blit(debug_text.render("{} rpm".format(rpm), False, pygame.Color('white')), (60, 298))
    screen.blit(debug_text.render(str(game_controller.GAME_DURATION - game_controller.get_time()) if game_controller.is_playing() else game_controller.get_state(), False, pygame.Color('white')), (constants.WIDTH - 100, 298))

    sprites.update()
    sprites.draw(screen)

    if game_controller.is_resuming():
        scoreboard_pos = ((constants.WIDTH / 2) - (scoreboard.get_rect().size[0] / 2), constants.HEIGHT + 15 - scoreboard.get_rect().size[1])
        screen.blit(scoreboard, scoreboard_pos)
        screen.blit(debug_text.render("[==> Enhorabuena! 75 donuts en 0,5 kms! <==]", False, (255, 185, 8)), (scoreboard_pos[0] + 20, scoreboard_pos[1] + 20))
        screen.blit(debug_text.render("# 1: 525 Donuts y 1,3 kms recorridos!", False, (255, 185, 8)), (scoreboard_pos[0] + 20, scoreboard_pos[1] + 60))
        screen.blit(debug_text.render("# 2: 425 Donuts y 1,2 kms recorridos!", False, (255, 185, 8)), (scoreboard_pos[0] + 20, scoreboard_pos[1] + 90))
        screen.blit(debug_text.render("# 3: 325 Donuts y 1,1 kms recorridos!", False, (255, 185, 8)), (scoreboard_pos[0] + 20, scoreboard_pos[1] + 120))
        screen.blit(debug_text.render("# 4: 225 Donuts y 1,0 kms recorridos!", False, (255, 185, 8)), (scoreboard_pos[0] + 20, scoreboard_pos[1] + 150))
        screen.blit(debug_text.render("# 5: 125 Donuts y 0,9 kms recorridos!", False, (255, 185, 8)), (scoreboard_pos[0] + 20, scoreboard_pos[1] + 180))

    pygame.display.flip()


pygame.quit()
