import pygame
from random import randint
from Pipe import Pipe


def draw_floor():
    global floor_x
    floor_x -= 1
    screen.blit(floor_surface, (floor_x, screen_h - floor_h))


pygame.init()
pygame.display.set_caption('FlappyBird')
clock = pygame.time.Clock()

screen_w = 288
screen_h = 512
screen = pygame.display.set_mode((screen_w, screen_h))

# loading game images
bg_surface = pygame.image.load('img/background-day.png').convert()
floor_surface = pygame.image.load('img/floor.png').convert()
bird_surface = pygame.image.load('img/bluebird-midflap.png').convert()
pipe_surface = pygame.image.load('img/pipe-green.png').convert()

# game variables
bird_rect = bird_surface.get_rect(center=(50, screen_h/2))
bird_speed = 0
gravity = 0.15
pipes = []

floor_x = 0
floor_w = 336
floor_h = 112

SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1500)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            break
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_speed = -6
        if event.type == SPAWNPIPE:
            pipes.append(Pipe(pipe_surface, (screen_w/2, screen_h/2)))

    screen.blit(bg_surface, (0, 0))

    # bird
    bird_speed += gravity
    bird_rect.centery += bird_speed

    # pipes
    for pipe in pipes:
        pipe.move()
        if pipe.rect.topright == 0:
            pipes.remove(pipe)
        pipe.draw(screen)

    # floor
    draw_floor()
    if floor_x + floor_w < screen_w:
        floor_x = 0

    screen.blit(bird_surface, bird_rect)
    pygame.display.update()
    clock.tick(120)
