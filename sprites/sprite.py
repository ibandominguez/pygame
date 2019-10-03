import pygame
import time


class Sprite(pygame.sprite.Sprite):

    def __init__(self, file_path, width, height, x, y, frames_count):
        pygame.sprite.Sprite.__init__(self)
        self.sheet = pygame.image.load(file_path).convert_alpha()
        self.image = pygame.transform.scale(self.sheet, (width, height))
        self.rect = self.image.get_rect()
        self.rect.centerx = x  # center of rectangle
        self.rect.bottom = y  #pixels up from the bottom
        self.animation = []
        self.start_frame = time.time()
        self.total_frames = frames_count
        self.frames_per_second = 10
        self.setup_animations(width, height)

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
        animation_index = int((time.time() - self.start_frame) * self.frames_per_second % self.total_frames)
        self.image = self.animation[animation_index]
