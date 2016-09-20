# Pygame template - skeleton for a new pygame project
import pygame
import random
from os import path

img_dir = path.join(path.dirname(__file__), 'img')

WIDTH = 480
HEIGHT = 600
FPS = 60

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255,0)

# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shumup! ")
clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (50,38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.image_orig = player_img
        self.image = self.image_orig.copy()
        self.radius = 20
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT / 2
        self.speedx = 0
        self.rot = 0
        self.rot_speed = random.randrange(-8,8)



    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.rot = (self.rot + self.rot_speed) % 360
            self.image = pygame.transform.rotate(self.image_orig, self.rot)
        if keystate[pygame.K_RIGHT]:
            self.rot = (self.rot + self.rot_speed) % 360
            self.image = pygame.transform.rotate(self.image_orig, self.rot)
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = meteor_img
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width *.80 /2)
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100,-40)
        self.speedy = random.randrange(1,8)
        self.speedx = random.randrange(-3,3)
        self.rot = 0
        self.rot_speed = random.randrange(-8,8)
        self.last_update = pygame.time.get_ticks()

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            self.image = pygame.transform.rotate(self.image_orig, self.rot)


    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.top > HEIGHT + 20 or self.rect.bottom > HEIGHT + 20 :
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100,-40)
            self.speedy = random.randrange(1,8)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10,20))
        self.image = laser_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y +=self.speedy
        #kill if it moves off the screen
        if self.rect.bottom < 0:
            self.kill()

#Load all game graphics
background = pygame.image.load(path.join(img_dir,"bluestar.png")).convert()
background_rect = background.get_rect()
player_img = pygame.image.load(path.join(img_dir,"playerShip2_blue.png")).convert()
meteor_img = pygame.image.load(path.join(img_dir,"enemyBlack1.png")).convert()
laser_img = pygame.image.load(path.join(img_dir,"laserBlue16.png")).convert()

all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player =Player()
all_sprites.add(player)
for i in range(8):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

# Game loop
running = True
while running:
    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
    # Update
    all_sprites.update()
   #checks if bullets collide with mob
    hits = pygame.sprite.groupcollide(mobs, bullets, True,True)
   #Loop to generate just as many new mobs as were the ones killed
    for hit in hits:
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)

    #check if mob collibe with player
    hits = pygame.sprite.spritecollide(player,mobs, True, pygame.sprite.collide_circle)
    if hits:
        running = True

    # Draw / render
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()
