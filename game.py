#!/usr/bin/env python

import os
import math
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
meters = 0
meter_counter = 0
kmh = 0
running = True
show_donuts_ticks = 0
donuts_delivered = 0
game_controller = Controller(game_duration=constants.GAME_DURATION, game_resuming=constants.GAME_RESUMING)

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
    rpm = rpm if rpm <= 500 else 500
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

""" Sprite Sheets """
intro = Sprite(file_path=os.getcwd() + '/assets/intro.png', width=constants.WIDTH, height=constants.HEIGHT, x=0, y=0, frames_tile=(6, 12), frames_total=72).set_animation_speed(30)
road = Sprite(file_path=os.getcwd() + '/assets/road.png', width=constants.WIDTH, height=constants.HEIGHT, x=0, y=0, frames_tile=(17, 2), frames_total=34)
bike = Sprite(file_path=os.getcwd() + '/assets/bike.png', width=constants.WIDTH, height=constants.HEIGHT, x=0, y=0, frames_tile=(5, 10), frames_total=50)
donuts = Sprite(file_path=os.getcwd() + '/assets/donuts.png', width=constants.WIDTH, height=constants.HEIGHT, x=0, y=0, frames_tile=(5, 10), frames_total=50)

intro_sprites = pygame.sprite.OrderedUpdates()
intro_sprites.add(intro)

sprites = pygame.sprite.OrderedUpdates()
sprites.add(road, bike, donuts)

""" Images """
background = pygame.image.load(os.getcwd() + '/assets/background.png').convert_alpha()
sign = pygame.image.load(os.getcwd() + '/assets/sign.png').convert_alpha()
resuming = pygame.image.load(os.getcwd() + '/assets/resuming.png').convert_alpha()

""" Text """
countdown_text = pygame.font.SysFont(pygame.font.get_default_font(), 100)
debug_text = pygame.font.SysFont(pygame.font.get_default_font(), 18)
resuming_text = pygame.font.SysFont(pygame.font.get_default_font(), 60)


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
    if game_controller.is_standing_by():
        if rpm > 0: game_controller.start()
        else:
            intro_sprites.update()
            intro_sprites.draw(screen)
    elif game_controller.is_playing():
        # Calculations
        if game_controller.every_seconds(1):
            ms = round(((0.35 * 2 * math.pi * rpm) / 60), 2)
            kmh = round(ms * 3.6, 2)
            meters = round(meters + ms, 2)
            meter_counter += ms

            # Donuts logics
            if meter_counter > 10:
                meter_counter = 0
                donuts_delivered += 10
                show_donuts_ticks += 5
            if show_donuts_ticks > 0:
                donuts.set_animation_speed(30)
                show_donuts_ticks -= 1
            else:
                donuts.set_animation_speed(0)

        # Screen filling
        screen.blit(background, (0, 0))
        screen.blit(sign, (0, constants.HEIGHT * 0.30))
        screen.blit(pygame.transform.flip(sign, True, False), (constants.WIDTH - 128, constants.HEIGHT * 0.30))
        screen.blit(debug_text.render("{} kmh".format(kmh), False, pygame.Color('white')), (55, constants.HEIGHT * 0.30 + 48))
        screen.blit(debug_text.render("{} donuts".format(donuts_delivered), False, pygame.Color('white')), (constants.WIDTH - 105, constants.HEIGHT * 0.30 + 48))

        # Speed updating
        road.set_animation_speed(rpm)
        bike.set_animation_speed(rpm)

        # Sprites drawing
        sprites.update()
        sprites.draw(screen)

        # Show countdown on game end
        if game_controller.game_duration - game_controller.get_time() <= 5:
            screen.blit(
                countdown_text.render(str(game_controller.game_duration - game_controller.get_time()), False, (255, 255, 255)),
                (constants.WIDTH / 2 - 25, constants.HEIGHT / 2 - 25)
            )
    elif game_controller.is_resuming():
        screen.blit(resuming, (0, 0))
        screen.blit(
            resuming_text.render("{} donuts".format(donuts_delivered), False, (255, 255, 255)),
            (constants.WIDTH * 0.31, constants.HEIGHT * 0.70)
        )
    elif game_controller.is_finished():
        rpm = 0
        meters = 0
        meter_counter = 0
        kmh = 0
        show_donuts_ticks = 0
        donuts_delivered = 0
        donuts.set_animation_speed(0)
        game_controller.end()

    """
    Handle Pygame Events
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()


pygame.quit()
