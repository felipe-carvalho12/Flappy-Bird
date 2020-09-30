import pygame
import random
from Coin import Coin
from Pipe import Pipe


def draw_floor():
    global floor_x
    floor_x -= 2
    screen.blit(floor_surface, (floor_x, screen_h - floor_h))


def render_score(game_state):
    if game_state == 'running':
        score_surface = game_main_font.render(f'Score: {round(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(screen_w/2, 30))
        screen.blit(score_surface, score_rect)
    elif game_state == 'game_over':
        go_rect = game_over_surface.get_rect(center=(screen_w/2, 120))
        screen.blit(game_over_surface, go_rect)

        score_surface = game_main_font.render(f'Score: {round(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(screen_w / 2, 220))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_main_font.render(f'High Score: {round(high_score)}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(screen_w / 2, 270))
        screen.blit(high_score_surface, high_score_rect)


pygame.mixer.pre_init(channels=1, buffer=256)
pygame.init()
pygame.display.set_caption('FlappyBird')
clock = pygame.time.Clock()
game_main_font = pygame.font.Font('04B_19.ttf', 30)

screen_w = 288
screen_h = 512
screen = pygame.display.set_mode((screen_w, screen_h))

# loading game images
bg_surface = pygame.image.load('img/background-day.png').convert()
floor_surface = pygame.image.load('img/floor.png').convert()
bottom_pipe_surface = pygame.image.load('img/pipe-green.png').convert()
top_pipe_surface = pygame.transform.rotate(bottom_pipe_surface, 180)
game_over_surface = pygame.image.load('img/gameover.png')
# coin images
coin_1 = pygame.image.load('img/coin_1.png').convert_alpha()
coin_2 = pygame.image.load('img/coin_2.png').convert_alpha()
coin_3 = pygame.image.load('img/coin_3.png').convert_alpha()
coin_4 = pygame.image.load('img/coin_4.png').convert_alpha()
coin_5 = pygame.image.load('img/coin_5.png').convert_alpha()
coin_6 = pygame.image.load('img/coin_6.png').convert_alpha()
coin_7 = pygame.image.load('img/coin_7.png').convert_alpha()
coin_8 = pygame.image.load('img/coin_8.png').convert_alpha()
coin_frames = [coin_1, coin_2, coin_3, coin_4, coin_5, coin_6, coin_7, coin_8]

coin_index = 0
coin_surface = coin_frames[coin_index]
coin_rect = coin_surface.get_rect(center=(screen_w/2, screen_h/2))
# bird images
bird_downflap = pygame.image.load('img/bluebird-downflap.png').convert()
bird_midflap = pygame.image.load('img/bluebird-midflap.png').convert()
bird_upflap = pygame.image.load('img/bluebird-upflap.png').convert()
bird_frames = [bird_downflap, bird_midflap, bird_upflap]

bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center=(50, screen_h/2))

# loading game sounds
score_sound = pygame.mixer.Sound('sounds/sfx_point.wav')
flap_sound = pygame.mixer.Sound('sounds/sfx_wing.wav')
death_sound = pygame.mixer.Sound('sounds/sfx_hit.wav')

# game variables
game_active = True
bird_yvelocity = 0
gravity = 0.15
coins = []
coin_pos = [100, 250, 300]
pipes = []
pipe_pos = [200, 275, 350]
score = 0
high_score = 0

floor_x = 0
floor_w = 336
floor_h = 112

SPAWNCOIN = pygame.USEREVENT
pygame.time.set_timer(SPAWNCOIN, 1000)

COINFLIP = pygame.USEREVENT + 1
pygame.time.set_timer(COINFLIP, 100)

BIRDFLAP = pygame.USEREVENT + 2
pygame.time.set_timer(BIRDFLAP, 100)

SPAWNPIPE = pygame.USEREVENT + 3
pygame.time.set_timer(SPAWNPIPE, 1500)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            break
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_yvelocity = -4
                flap_sound.play()
            elif event.key == pygame.K_SPACE and not game_active:
                game_active = True
                bird_rect.center = (50, screen_h/2)
                bird_yvelocity = 0
                coins.clear()
                pipes.clear()
                score = 0

        if event.type == SPAWNCOIN and game_active:
            rdm_coin_pos = random.choice(coin_pos)
            new_coin = Coin(top_pipe_surface, (400, rdm_coin_pos))
            coins.append(new_coin)

        if event.type == COINFLIP and game_active:
            coin_index += 1
            if coin_index >= len(coin_frames):
                coin_index = 1
            for coin in coins:
                coin.surface = coin_frames[coin_index]
                coin.rect = coin.surface.get_rect(center=(coin.rect.centerx, coin.rect.centery))

        if event.type == BIRDFLAP and game_active:
            bird_index += 1
            if bird_index >= len(bird_frames):
                bird_index = 0
            bird_surface = bird_frames[bird_index]
            bird_rect = bird_surface.get_rect(center=(50, bird_rect.centery))

        if event.type == SPAWNPIPE and game_active:
            rdm_pipe_pos = random.choice(pipe_pos)
            bottom_pipe = Pipe(bottom_pipe_surface, midtop=(400, rdm_pipe_pos))
            top_pipe = Pipe(top_pipe_surface, midbottom=(400, rdm_pipe_pos - 150))
            pipes.extend([bottom_pipe, top_pipe])

    # background
    screen.blit(bg_surface, (0, 0))

    if game_active:
        score += 0.1

        # coins
        for coin in coins:
            coin.move()
            if coin.rect.right <= 0:
                coins.remove(coin)
            if coin.rect.colliderect(bird_rect):
                score += 100
                score_sound.play()
                coins.remove(coin)
            coin.draw(screen)

        # bird
        bird_yvelocity += gravity
        bird_rect.centery += bird_yvelocity
        if bird_rect.top <= -50 or bird_rect.bottom >= screen_h - floor_h:
            game_active = False
            death_sound.play()
            high_score = score if score > high_score else high_score

        rotated_bird = pygame.transform.rotate(bird_surface, -bird_yvelocity * 5)
        screen.blit(rotated_bird, bird_rect)

        # pipes
        for pipe in pipes:
            pipe.move()
            if pipe.rect.right <= 0:
                pipes.remove(pipe)
            if pipe.rect.colliderect(bird_rect):
                game_active = False
                death_sound.play()
                high_score = score if score > high_score else high_score
                pipes.remove(pipe)
            pipe.draw(screen)

        render_score('running')
    else:
        render_score('game_over')
    # floor
    draw_floor()
    if floor_x + floor_w < screen_w:
        floor_x = 0

    pygame.display.update()
    clock.tick(120)
