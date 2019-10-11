import pygame
import time


class Sprite(pygame.sprite.Sprite):
    def __init__(self, directory, width, height, total_frames):
        pygame.sprite.Sprite.__init__(self)
        self.directory = directory
        self.width = width
        self.height = height
        self.total_frames = total_frames
        self.images = []
        self.setup_animations()
        self.index = 0
        self.image = self.images[self.index]
        self.rect = pygame.Rect(0, 0, width, height)
        self.time_ref = self.get_milis()
        self.milis_counter = 0
        self.current_animation_index = 0
        self.speed = 0

    def get_milis(self):
        return time.time() * 1000

    def set_animation_speed(self, speed):
        self.speed = speed
        return self

    def setup_animations(self):
        for frame_index in range(self.total_frames):
            loaded_image = pygame.image.load('{}/{}.png'.format(self.directory, frame_index)).convert_alpha()
            scaled_image = pygame.transform.scale(loaded_image, (self.width, self.height))
            self.images.append(scaled_image)

    def update(self):
        if self.speed == 0:
            self.image = self.images[0]
            return

        if self.milis_counter > (1000 / self.speed):
            if self.speed > 30: incrementer = int(self.speed / 30)
            else: incrementer = 1
            if self.index + incrementer >= len(self.images) - 1: self.index = (self.index + incrementer) - len(self.images) - 1
            else: self.index += incrementer
            self.milis_counter = 0
        else:
            self.milis_counter += self.get_milis() - self.time_ref

        self.time_ref = self.get_milis()
        if self.index < len(self.images): self.image = self.images[self.index]
