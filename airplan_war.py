# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
from sys import exit
import random

SCREEN_WIDTH = 480
SCREEN_HEIGHT = 800
# Initialize the game
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display. set_caption('Airplane Wars') 
# Load the background map
background = pygame.image.load('resources/image/background.png')

# Load the picture of the plane
plane_img = pygame.image.load('resources/image/shoot.png')
# Select the position of the plane in the big picture, generate subsurface, and then initialize the position of the plane.
player_rect = pygame.Rect(0, 99, 102, 126)
player = plane_img.subsurface(player_rect)
player_pos = [200, 600]


# Player
class Player (pygame.sprite.Sprite):
    def __init__(self, plane_img, player_rect, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = [] # List of pictures of player object wizard
        for i in range(len(player_rect)):
            self.image.append(plane_img.subsurface(player_rect[i]).convert_alpha())
            self.rect = player_rect[0] # Initialize the rectangle where the picture is located
            self.rect.topleft = init_pos # Initialize the upper left corner coordinates of the rectangle
            self.speed = 8 # Initialize the player speed, here is a definite value.
            self.img_index = 0 # Player Wizard Image Index
            self.bullets = pygame.sprite.Group() # Collection of bullets fired by the player's aircraft
            self.is_hit = False # Is the player hit?

    def moveUp(self):
        if self.rect.top <= 0:
            self.rect.top = 0
        else:
            self.rect.top -= self.speed
    
    def moveDown(self):
        if self.rect.top >= SCREEN_HEIGHT - self.rect.height:
            self.rect.top = SCREEN_HEIGHT - self.rect.height
        else:
            self.rect.top += self.speed
    
    def moveLeft(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        else:
            self.rect.left -= self.speed
    
    def moveRight(self):
        if self.rect.left >= SCREEN_WIDTH - self.rect.width:
            self.rect.left = SCREEN_WIDTH - self.rect.width
        else:
            self.rect.left += self.speed

    def shoot(self, bullet_img):
        bullet = Bullet (bullet_img, self.rect.midtop)
        self.bullets.add (bullet)

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_img, enemy_down_imgs, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.rect.topleft = init_pos
        self.down_imgs = enemy_down_imgs
        self.speed = 2
        self.down_index = 0

    def move(self):
        self.rect.top += self.speed

# Bullet
class Bullet(pygame.sprite.Sprite):
    def __init__(self, bullet_img, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.midbottom = init_pos
        self.speed = 10 
    def move(self):
        self.rect.top -= self.speed


# Définir les paramètres liés au joueur
player_rect = []
player_rect.append(pygame.Rect(0, 99, 102, 126)) # Zone d'image du sprite du joueur
player_rect.append(pygame.Rect(165, 360, 102, 126))
player_rect.append(pygame.Rect(165, 234, 102, 126)) # Zone d'image du sprite d'explosion du joueur
player_rect.append(pygame.Rect(330, 624, 102, 126))
player_rect.append(pygame.Rect(330, 498, 102, 126))
player_rect.append(pygame.Rect(432, 624, 102, 126))
player_pos = [200, 600]
player = Player(plane_img, player_rect, player_pos)

player_down_index = 16

# Définir les paramètres liés à la surface utilisés par l'objet avion ennemi
enemy1_rect = pygame.Rect(534, 612, 57, 43)
enemy1_img = plane_img.subsurface(enemy1_rect)
enemies1 = pygame.sprite.Group()
enemy_frequency = 0

enemy1_down_sound = pygame.mixer.Sound('resources/sound/enemy1_down.wav')
enemy1_down_sound.set_volume(0.3)
enemy1_down_imgs = []
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(267, 347, 57, 43)))
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(873, 697, 57, 43)))
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(267, 296, 57, 43)))
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(930, 697, 57, 43)))
# Stockez des avions détruits pour le rendu d'animations de sprites d'épaves
enemies_down = pygame.sprite.Group()


bullet_sound = pygame.mixer.Sound('resources/sound/bullet.wav')
bullet_sound.set_volume(0.3)

game_over = pygame.image.load('resources/image/gameover.png')
game_over_sound = pygame.mixer.Sound('resources/sound/game_over.wav')
game_over_sound.set_volume(0.3)

# Définir les paramètres liés à la surface utilisés par l'objet puce (bullets)
bullet_rect = pygame.Rect(1004, 987, 9, 21)
bullet_img = plane_img.subsurface(bullet_rect)
shoot_frequency = 0

clock = pygame.time.Clock()
running = True
while running:

    # Contrôlez la fréquence d'images maximale du jeu
    clock.tick(45)

    # Draw the background
    screen.fill(0)
    screen.blit(background, (0, 0))

    # dessiner l'avion du joueur
    if not player.is_hit:
        screen.blit(player.image[player.img_index], player.rect)
        # Changer l'index de l'image pour animer l'avion
        player.img_index = shoot_frequency // 8
    else:
        player.img_index = player_down_index // 8
        screen.blit(player.image[player.img_index], player.rect)
        player_down_index += 1
        if player_down_index > 47:
            running = False

    # Faire apparaître des avions ennemis : 
    if enemy_frequency % 50 == 0:
        enemy1_pos = [random.randint(0, SCREEN_WIDTH -enemy1_rect.width), 0]
        enemy1 = Enemy(enemy1_img,
                enemy1_down_imgs, #Ajouter ceci car on a modifie la classe Enemy
                enemy1_pos)
        enemies1.add(enemy1)
    enemy_frequency += 1
    if enemy_frequency >= 100:
        enemy_frequency = 0

    # Déplacez l'avion ennemi, s'il dépasse la plage de la fenêtre, supprimez-le
    for enemy in enemies1:
        enemy.move()
        # Déterminez si le joueur a été touché
        if pygame.sprite.collide_circle(enemy, player):
            enemies_down.add(enemy)
            enemies1.remove(enemy)
            player.is_hit = True
            game_over_sound.play()
            break
    enemies1.draw(screen)

    # Ajoutez l'objet avion ennemi touché au groupe d'avions ennemis détruits, utilisé pour rendre l'animation de destruction
    enemies1_down = pygame.sprite.groupcollide(enemies1, player.bullets, 1, 1)
    for enemy_down in enemies1_down:
        enemies_down.add(enemy_down)

    # Dessinez l'animation de l'épave
    for enemy_down in enemies_down:
        if enemy_down.down_index == 0:
            enemy1_down_sound.play()
        if enemy_down.down_index > 7:
            enemies_down.remove(enemy_down)
            # score += 1000
            continue
        screen.blit(enemy_down.down_imgs[enemy_down.down_index // 2], enemy_down.rect)
        enemy_down.down_index += 1

    # Contrôler la fréquence des tirs de balles et des balles de feu
    if shoot_frequency % 15 == 0:
        bullet_sound.play()
        player.shoot(bullet_img)
    shoot_frequency += 1
    if shoot_frequency >= 15:
        shoot_frequency = 0

    # Draw the bullets
    player.bullets.draw(screen)

    # Déplacer la puce, la supprimer si elle dépasse le cadre de la fenêtre
    for bullet in player.bullets:
        bullet.move()
        if bullet.rect.bottom < 0:
            player.bullets.remove(bullet)

    # Update the screen
    pygame.display.update()

    # Process game exits
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # Monitor keyboard events
        key_pressed = pygame.key.get_pressed()
        if key_pressed[K_w] or key_pressed[K_UP]:
            player.moveUp()
        if key_pressed[K_s] or key_pressed[K_DOWN]:
            player.moveDown()
        if key_pressed[K_a] or key_pressed[K_LEFT]:
            player.moveLeft()
        if key_pressed[K_d] or key_pressed[K_RIGHT]:
            player.moveRight()

screen.blit(game_over, (0, 0))

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    pygame.display.update()
