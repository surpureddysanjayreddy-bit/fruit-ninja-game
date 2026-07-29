import pygame
import os
import random

WIDTH, HEIGHT = 800, 500
FPS = 12
WHITE = (255, 255, 255)

pygame.init()
pygame.display.set_caption('Fruit Ninja')
gameDisplay = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

BASE = os.path.dirname(os.path.abspath(__file__))
background = pygame.image.load(os.path.join(BASE, 'back.jpg'))
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
font = pygame.font.Font(os.path.join(BASE, 'comic.ttf'), 32)

fruits = ['melon', 'orange', 'pomegranate', 'guava', 'bomb']
data = {}

def img(name):
    return pygame.image.load(os.path.join(BASE, 'images', name + '.png'))

def generate_random_fruits(fruit):
    data[fruit] = {
        'img': img(fruit),
        'x': random.randint(100, 500),
        'y': HEIGHT + 50,
        'speed_x': random.randint(-10, 10),
        'speed_y': random.randint(-80, -60),
        'throw': random.random() >= 0.5,
        't': 0,
        'hit': False,
    }

for f in fruits:
    generate_random_fruits(f)

def draw_text(text, size, x, y):
    f = pygame.font.Font(os.path.join(BASE, 'comic.ttf'), size)
    surf = f.render(text, True, WHITE)
    rect = surf.get_rect(midtop=(x, y))
    gameDisplay.blit(surf, rect)

def draw_lives(x, y, lives):
    icon = img('red_lives')
    for i in range(lives):
        gameDisplay.blit(icon, (x + 35 * i, y))

def show_gameover_screen(current_score, is_initial_start):
    gameDisplay.blit(background, (0, 0))
    draw_text("FRUIT NINJA!", 64, WIDTH // 2, HEIGHT // 4)
    if not is_initial_start:
        draw_text("Score: " + str(current_score), 40, WIDTH // 2, 250)
    draw_text("Press a key to begin!", 24, WIDTH // 2, HEIGHT * 3 // 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYUP:
                waiting = False
    return True

first_round = True
game_over = True
game_running = True
score = 0
player_lives = 3

while game_running:
    if game_over:
        game_running = show_gameover_screen(score, first_round)
        first_round = False
        if not game_running:
            break
        game_over = False
        player_lives = 3
        score = 0
        data = {}
        for f in fruits:
            generate_random_fruits(f)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False

    gameDisplay.blit(background, (0, 0))
    draw_text("Score: " + str(score), 28, 70, 5)
    draw_lives(650, 5, player_lives)

    for key, value in list(data.items()):
        if value['throw']:
            value['x'] += value['speed_x']
            value['y'] += value['speed_y']
            value['speed_y'] += value['t']
            value['t'] += 1

            if value['y'] <= HEIGHT + 60:
                gameDisplay.blit(value['img'], (value['x'], value['y']))
            else:
                generate_random_fruits(key)
                continue

            mx, my = pygame.mouse.get_pos()
            if not value['hit'] and value['x'] < mx < value['x'] + 60 and value['y'] < my < value['y'] + 60:
                if key == 'bomb':
                    player_lives -= 1
                    value['img'] = img('explosion')
                    if player_lives <= 0:
                        game_over = True
                else:
                    value['img'] = img('half_' + key)
                    score += 1
                value['speed_x'] += 10
                value['hit'] = True
        else:
            generate_random_fruits(key)

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
