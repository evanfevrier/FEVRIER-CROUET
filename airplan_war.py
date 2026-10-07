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


# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_img, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.rect.topleft = init_pos
        self.speed = 2
        self.down_index = 0

    def move (self):
        self.rect.top += self.speed


# Définir les paramètres liés à la surface utilisés par l'objet avion ennemi
enemy1_rect = pygame.Rect(534, 612, 57, 43)
enemy1_img = plane_img.subsurface(enemy1_rect)
enemies1 = pygame.sprite.Group()
enemy_frequency = 0


clock = pygame.time.Clock()
running = True
while running:

    # Contrôlez la fréquence d'images maximale du jeu
    clock.tick(45)

    # Draw the background
    screen.fill (0)
    screen.blit (background, (0, 0))

    # Draw an airplane
    screen.blit (player, player_pos)

    # Faire apparaître des avions ennemis : 
    if enemy_frequency % 50 == 0:
        enemy1_pos = [random.randint(0, SCREEN_WIDTH -enemy1_rect.width), 0]
        enemy1 = Enemy(enemy1_img, enemy1_pos)
        enemies1.add(enemy1)
    enemy_frequency += 1
    if enemy_frequency >= 100:
        enemy_frequency = 0

    # Déplacez l'avion ennemi, s'il dépasse la plage de la fenêtre, supprimez-le
    for enemy in enemies1:
        enemy.move()
        if enemy.rect.top > SCREEN_HEIGHT:
            enemies1.remove(enemy)
    enemies1.draw(screen)

    # Update the screen
    pygame.display.update()

    # Process game exits
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # Monitor keyboard events
        key_pressed = pygame.key.get_pressed()
        if key_pressed[K_UP]:
            player_pos[1] -= 3
        if key_pressed[ K_DOWN]:
            player_pos[1] += 3
        if key_pressed[K_LEFT]:
            player_pos[0] -= 3
        if key_pressed[K_RIGHT]:
            player_pos[0] += 3
