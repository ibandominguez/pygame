import pygame
import time


class FrameSprite(pygame.sprite.Sprite):
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
            loaded_image = pygame.image.load('{}/{}.png'.format(self.directory, frame_index))
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


class Sprite(pygame.sprite.Sprite):

    def __init__(self, file_path, width, height, x, y, frames_tile, frames_total):
        pygame.sprite.Sprite.__init__(self)
        self.sheet = pygame.image.load(file_path).convert_alpha()
        # self.image = pygame.transform.scale(self.sheet, (width, height))
        self.rect = pygame.Rect(0, 0, width, height)
        self.animation = []
        self.frames_tile = frames_tile
        self.frames_total = frames_total
        self.time_ref = self.get_milis()
        self.milis_counter = 0
        self.current_animation_index = 0
        self.frames_per_second = 0
        self.setup_animations(width, height)

    def get_milis(self):
        return time.time() * 1000

    def set_animation_speed(self, speed):
        self.frames_per_second = speed
        return self

    def setup_animations(self, width, height):
        counter = 0
        for y in range(self.frames_tile[1]):
            for x in range(self.frames_tile[0]):
                if counter < self.frames_total:
                    self.animation.append(self.get_image(width * x, height * y, width, height))
                counter += 1
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
            if self.frames_per_second > 30: incrementer = int(self.frames_per_second / 30)
            else: incrementer = 1
            if self.current_animation_index + incrementer >= len(self.animation) - 1: self.current_animation_index = (self.current_animation_index + incrementer) - len(self.animation) - 1
            else: self.current_animation_index += incrementer
            self.milis_counter = 0
        else:
            self.milis_counter += self.get_milis() - self.time_ref

        self.time_ref = self.get_milis()
        if self.current_animation_index < len(self.animation): self.image = self.animation[self.current_animation_index]
