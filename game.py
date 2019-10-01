import pygame

WIDTH = 400
HEIGHT = 400
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()


class Player(pygame.sprite.Sprite):

    def __init__(self, width, height, frames_count):
        pygame.sprite.Sprite.__init__(self)
        sheet = pygame.image.load('assets/bike-output.png').convert_alpha()
        self.image = pygame.transform.scale(sheet, (width, height))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2   #center of rectangle
        self.rect.bottom = HEIGHT  #pixels up from the bottom

        self.index = 0

        sprite_sheet = SpriteSheet('assets/bike-output.png')
        self.animation = []

        for i in range(frames_count - 1):
            self.animation.append(sprite_sheet.get_image(width * i, 0, width, height))

    def update(self):
        if self.index < len(self.animation) - 1:
            self.index = self.index + 1
        else:
            self.index = 0

        self.image = self.animation[self.index]


class SpriteSheet(object):
    def __init__(self, file_name):
        # You have to call `convert_alpha`, so that the background of
        # the surface is transparent.
        self.sprite_sheet = pygame.image.load(file_name).convert_alpha()

    def get_image(self, x, y, width, height):
        # Use a transparent surface as the base image (pass pygame.SRCALPHA).
        image = pygame.Surface([width, height], pygame.SRCALPHA)
        image.blit(self.sprite_sheet, (0,0), (x, y, width, height))
        return image


all_sprites = pygame.sprite.Group()
player = Player(135, 115, 25)
all_sprites.add(player)

running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update()
    screen.fill(WHITE)
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()
