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
pygame.mouse.set_visible(0)

"""
Specific size: pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
Full screen: pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
Monitor size: pygame.display.set_mode((monitor.current_w, monitor.current_h))
"""
if constants.FULLSCREEN:
    monitor = pygame.display.Info()
    constants.WIDTH = monitor.current_w
    constants.HEIGHT = monitor.current_h
    screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT), pygame.FULLSCREEN)
else:
    screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))

highest_score = 0
counter = 0
start = 0
end = 0
timeDeath=0
timeDeathFlag=0
timeDeathStart=0
timeDeathEnd=0
clock = pygame.time.Clock()
rpm = 0
meters = 0
meter_counter = 0
kmh = 0
rpmTime = 1
timeDeath = 0
running = True
show_donuts_ticks = 0
donuts_delivered = 0
show_record = False
game_controller = Controller(game_duration=constants.GAME_DURATION, game_resuming=constants.GAME_RESUMING)

"""
Scaled image helper
"""
def get_image_scaled(path, width, height):
    img = pygame.image.load(path).convert_alpha()
    return pygame.transform.scale(img, (width, height))

"""
Sensor setup
Only in RPI
"""
def calculate(channel):
    global counter
    global rpm
    global start
    global end
    global timeDeathFlag
    
    timeDeathFlag=0
    print ("rpm Time:"+str(timeDeath) + " " +"RPM:" + str(rpm))
    counter = counter + 1
    end = time.time()  
    rpm = int((1.0 / (end - start)) * 60.0)
    rpm = rpm if rpm <= 800 else 800
    start = time.time()
    #print (rpm)

try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(2, GPIO.IN)
    GPIO.setup(3, GPIO.OUT)
    GPIO.output(3, False)
    GPIO.add_event_detect(2, GPIO.RISING, callback=calculate, bouncetime=60)
except Exception as e:
    print('RPI module not found, Sensor not initialized')

""" Sprite Sheets """
intro = Sprite(directory=os.getcwd() + '/assets/intro', width=constants.WIDTH, height=constants.HEIGHT, total_frames=72).set_animation_speed(35)
road = Sprite(directory=os.getcwd() + '/assets/road', width=constants.WIDTH, height=constants.HEIGHT, total_frames=34)
bike = Sprite(directory=os.getcwd() + '/assets/bike', width=constants.WIDTH, height=constants.HEIGHT, total_frames=50)
donuts = Sprite(directory=os.getcwd() + '/assets/donuts', width=constants.WIDTH, height=constants.HEIGHT, total_frames=50)

intro_sprites = pygame.sprite.OrderedUpdates()
intro_sprites.add(intro)

sprites = pygame.sprite.OrderedUpdates()
sprites.add(road, bike, donuts)

""" Images """
background = get_image_scaled(os.getcwd() + '/assets/background.png', constants.WIDTH, constants.HEIGHT)
sign = pygame.image.load(os.getcwd() + '/assets/sign.png').convert_alpha()
resuming = get_image_scaled(os.getcwd() + '/assets/resuming.png', constants.WIDTH, constants.HEIGHT)

""" Text """
countdown_text = pygame.font.Font(os.getcwd() + '/assets/donuts.ttf', 120)
debug_text = pygame.font.Font(os.getcwd() + '/assets/donuts.ttf', 18)
resuming_text = pygame.font.Font(os.getcwd() + '/assets/donuts.ttf', 50)
score_text = pygame.font.Font(os.getcwd() + '/assets/donuts.ttf', 30)

if __name__ == "__main__":
    while running:
        clock.tick(constants.FPS)
   
        """
        Handle Pygame Events
        """
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    running = False
            if event.type == pygame.QUIT:
                running = False

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
        
            timeDeathEnd=time.time()
            timeDeath=timeDeathEnd-timeDeathStart
            
            if timeDeathFlag == 0:
                timeDeathStart=time.time()
                timeDeathFlag = 1
            
            if timeDeath > constants.DEATH_TIME_LIMIT:
                rpm=0
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
                    donuts.set_animation_speed(40)
                    show_donuts_ticks -= 1
                else:
                    donuts.set_animation_speed(0)

            # Screen filling
            screen.blit(background, (0, 0))
            screen.blit(sign, (0, constants.HEIGHT * 0.30))
            screen.blit(pygame.transform.flip(sign, True, False), (constants.WIDTH - 128, constants.HEIGHT * 0.30))
            screen.blit(debug_text.render("{} kmh".format(kmh), False, pygame.Color('white')), (50, constants.HEIGHT * 0.30 + 45))
            screen.blit(debug_text.render("{} donuts".format(donuts_delivered), False, pygame.Color('white')), (constants.WIDTH - 110, constants.HEIGHT * 0.30 + 45))

            # Speed updating
            road.set_animation_speed(rpm)
            bike.set_animation_speed(rpm)

            # Sprites drawing
            sprites.update()
            sprites.draw(screen)

            # Show highest_score
            if highest_score > 0:
                screen.blit(
                    score_text.render("1ST - {} DONUTS".format(highest_score), False, (137, 0, 27)),
                    (constants.WIDTH * 0.35, constants.HEIGHT * 0.15)
                )

            # Show countdown on game end
            if game_controller.game_duration - game_controller.get_time() <= 5:
                screen.blit(
                    countdown_text.render(str(game_controller.game_duration - game_controller.get_time()), False, (43, 25, 91)),
                    (constants.WIDTH / 2 - 30, constants.HEIGHT / 2 - 100)
                )
        elif game_controller.is_resuming():
            if donuts_delivered > highest_score: show_record = True

            if show_record:
                highest_score = donuts_delivered
                text = "RECORD!  {} DONUTS".format(donuts_delivered)
            else:
                text = "        {} DONUTS".format(donuts_delivered)

            screen.blit(resuming, (0, 0))
            screen.blit(
                resuming_text.render(text, False, (137, 0, 27)),
                (constants.WIDTH * 0.20, constants.HEIGHT * 0.70)
            )
        elif game_controller.is_finished():
            rpm = 0
            meters = 0
            meter_counter = 0
            kmh = 0
            show_donuts_ticks = 0
            donuts_delivered = 0
            show_record = False
            donuts.set_animation_speed(0)
            game_controller.end()

        pygame.display.flip()


    pygame.quit()

