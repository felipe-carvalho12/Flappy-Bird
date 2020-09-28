import pygame

pygame.init()
# screen set up
pygame.display.set_caption('FlappyBird')
icon = pygame.image.load('img/icon.png')
pygame.display.set_icon(icon)

screen_w = 1
screen_h = 1
screen = pygame.display.set_mode((screen_w, screen_h))
background_img = pygame.image.load('img/menu.png')
