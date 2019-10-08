import pygame
import time


class Sprite(pygame.sprite.Sprite):

    def __init__(self, file_path, width, height, x, y, frames_count):
        pygame.sprite.Sprite.__init__(self)
        self.sheet = pygame.image.load(file_path).convert_alpha()
        self.image = pygame.transform.scale(self.sheet, (width, height))
        self.rect = self.image.get_rect()
        self.rect.centerx = x  # center of rectangle
        self.rect.bottom = y  # pixels up from the bottom
        self.animation = []
        self.total_frames = frames_count
        self.time_ref = time.time()
        self.milis_counter = 0
        self.current_animation_index = 0
        self.frames_per_second = 100
        self.setup_animations(width, height)

    def get_milis(self):
        return time.time() * 1000

    def set_animation_speed(self, speed):
        self.frames_per_second = speed
        return self

    def setup_animations(self, width, height):
        for i in range(self.total_frames):
            self.animation.append(self.get_image(width * i, 0, width, height))
        self.image = self.animation[0]

    def get_image(self, x, y, width, height):
        image = pygame.Surface([width, height], pygame.SRCALPHA)
        image.blit(self.sheet, (0, 0), (x, y, width, height))
        return image

    def update(self):
        if self.frames_per_second == 0:
            self.image = self.animation[0]
            return

        if self.milis_counter > (1000 / self.frames_per_second):
            if self.current_animation_index >= len(self.animation) - 1: self.current_animation_index = 0
            else: self.current_animation_index += 1
            self.milis_counter = 0
        else:
            self.milis_counter += self.get_milis() - self.time_ref

        self.time_ref = self.get_milis()
        self.image = self.animation[self.current_animation_index]
