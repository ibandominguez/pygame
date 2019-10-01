import pygame

WIDTH = 1000
HEIGHT = 700
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()


class Player(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        width = 25
        height = 25
        sheet = pygame.image.load('assets/bike.png').convert_alpha()
        self.image = pygame.transform.scale(sheet, (270, 230))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2 - 480   #center of rectangle
        self.rect.bottom = HEIGHT - 5  #pixels up from the bottom
        self.speedx = 0
        self.speedy = 0
        self.walkingright = []
        self.walkingleft = []
        self.walkingup = []
        self.walkingdown = []
        self.direction = 'R'

        sprite_sheet = SpriteSheet('assets/bike.png')
        #Facing Down
        # Start at x = 0. Pass 48 as the third and
        # fourth argument (width and height).
        image = sprite_sheet.get_image(0,0,48,48)
        self.walkingdown.append(image)
        image = sprite_sheet.get_image(48,0,48,48)
        self.walkingdown.append(image)
        image = sprite_sheet.get_image(96,0,48,48)
        self.walkingdown.append(image)
        image = sprite_sheet.get_image(144,0,48,48)
        self.walkingdown.append(image)

        #Facing Up
        image = sprite_sheet.get_image(0,144,48,48)
        self.walkingup.append(image)
        image = sprite_sheet.get_image(48,144,48,48)
        self.walkingup.append(image)
        image = sprite_sheet.get_image(96,144,48,48)
        self.walkingup.append(image)
        image = sprite_sheet.get_image(144,144,48,48)
        self.walkingup.append(image)

        #Facing Right
        image = sprite_sheet.get_image(0,96,48,48)
        self.walkingright.append(image)
        image = sprite_sheet.get_image(48,96,48,48)
        self.walkingright.append(image)
        image = sprite_sheet.get_image(96,96,48,48)
        self.walkingright.append(image)
        image = sprite_sheet.get_image(144,96,48,48)
        self.walkingright.append(image)

        #Facing Left
        image = sprite_sheet.get_image(0,48,48,48)
        self.walkingleft.append(image)
        image = sprite_sheet.get_image(48,48,48,48)
        self.walkingleft.append(image)
        image = sprite_sheet.get_image(96,48,48,48)
        self.walkingleft.append(image)
        image = sprite_sheet.get_image(144,48,48,48)
        self.walkingleft.append(image)

    def update(self):
        pos_x = self.rect.x
        # You also need the y position for the vertical movement.
        pos_y = self.rect.y
        if self.direction == "R":
            frame = (pos_x // 30) % len(self.walkingright)
            self.image = self.walkingright[frame]
        if self.direction == "L":
            frame = (pos_x // 30) % len(self.walkingleft)
            self.image = self.walkingleft[frame]
        if self.direction == "U":
            frame = (pos_y // 30) % len(self.walkingup)
            self.image = self.walkingup[frame]
        if self.direction == "D":
            frame = (pos_y // 30) % len(self.walkingdown)
            self.image = self.walkingdown[frame]

        self.speedx = 0 #Need these to make sure
        self.speedy = 0 #Sprite stops moving on keyup
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -5
            self.direction = 'L'
        if keystate[pygame.K_RIGHT]:
            self.speedx = 5
            self.direction = 'R'
        if keystate[pygame.K_UP]:
            self.speedy = -5
            self.direction = 'U'
        if keystate[pygame.K_DOWN]:
            self.speedy = 5
            self.direction = 'D'
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        #Set Walls for Width and Height
        if self.rect.right > WIDTH:
            self.rect.rect = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT


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
player = Player()
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
