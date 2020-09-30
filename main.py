import pygame
import random
from math import floor
from Pipe import Pipe


def draw_floor():
    global floor_x
    floor_x -= 2
    screen.blit(floor_surface, (floor_x, screen_h - floor_h))


def game_over():
    pygame.quit()


pygame.init()
pygame.display.set_caption('FlappyBird')
clock = pygame.time.Clock()

screen_w = 288
screen_h = 512
screen = pygame.display.set_mode((screen_w, screen_h))

# loading game images
bg_surface = pygame.image.load('img/background-day.png').convert()
floor_surface = pygame.image.load('img/floor.png').convert()
bottom_pipe_surface = pygame.image.load('img/pipe-green.png').convert()
top_pipe_surface = pygame.transform.rotate(bottom_pipe_surface, 180)
# bird images
bird_downflap = pygame.image.load('img/bluebird-downflap.png').convert()
bird_midflap = pygame.image.load('img/bluebird-midflap.png').convert()
bird_upflap = pygame.image.load('img/bluebird-upflap.png').convert()
bird_frames = [bird_downflap, bird_midflap, bird_upflap]

bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center=(50, screen_h/2))

# game variables
game_active = True
bird_yvelocity = 0
gravity = 0.15
pipes = []
pipe_pos = [200, 275, 350]

floor_x = 0
floor_w = 336
floor_h = 112

BIRDFLAP = pygame.USEREVENT
pygame.time.set_timer(BIRDFLAP, 100)

SPAWNPIPE = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWNPIPE, 1500)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            break
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_yvelocity = -4
            elif event.key == pygame.K_SPACE and not game_active:
                game_active = True
                bird_rect.center = (50, screen_h/2)
                bird_yvelocity = 0
                pipes.clear()
        if event.type == BIRDFLAP and game_active:
            bird_index += 1
            if bird_index >= len(bird_frames):
                bird_index = 0
            bird_surface = bird_frames[bird_index]
            bird_rect = bird_surface.get_rect(center=(50, bird_rect.centery))

        if event.type == SPAWNPIPE and game_active:
            rdm_pipe_pos = random.choice(pipe_pos)
            bottom_pipe = Pipe(bottom_pipe_surface, midtop=(500, rdm_pipe_pos))
            top_pipe = Pipe(top_pipe_surface, midbottom=(500, rdm_pipe_pos - 150))
            pipes.extend([bottom_pipe, top_pipe])

    # background
    screen.blit(bg_surface, (0, 0))

    if game_active:
        # bird
        bird_yvelocity += gravity
        bird_rect.centery += bird_yvelocity
        if bird_rect.top <= -50 or bird_rect.bottom >= screen_h - floor_h:
            game_active = False

        rotated_bird = pygame.transform.rotate(bird_surface, -bird_yvelocity * 5)
        screen.blit(rotated_bird, bird_rect)

        # pipes
        for pipe in pipes:
            pipe.move()
            if pipe.rect.right <= 0:
                pipes.remove(pipe)
            if pipe.rect.colliderect(bird_rect):
                game_active = False
                pipes.remove(pipe)
            pipe.draw(screen)
    else:
        pass
    # floor
    draw_floor()
    if floor_x + floor_w < screen_w:
        floor_x = 0

    pygame.display.update()
    clock.tick(120)
