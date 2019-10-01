import pygame


class Bike(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
        self.image = pygame.image.load("./assets/bike.png").convert_alpha()
