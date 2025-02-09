import pygame
import os
import sys

sys.path.append(os.path.abspath("./classes"))

from snake import *

WINDOW_SIZE = [800, 600]
GRID_SIZE = 20

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

def generate_food_position():
    while True:
        food_pos = [
            random.randint(0, (WINDOW_SIZE[0] // GRID_SIZE) - 1) * GRID_SIZE,
            random.randint(0, (WINDOW_SIZE[1] // GRID_SIZE) - 1) * GRID_SIZE
        ]
        if food_pos not in snake.body:
            return food_pos
        


pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption('Snake')
clock = pygame.time.Clock()

try:
    font = pygame.font.Font('./sewer.ttf', 32)
except FileNotFoundError:
    font = pygame.font.SysFont(None, 32)


snake = Snake(1, random.choice([GREEN, BLUE, WHITE]), WINDOW_SIZE, GRID_SIZE)

food_pos = generate_food_position()

running = True
last_key = None
while running:

    screen.fill(BLACK)
    text = font.render(f'Score: {snake.get_score()}', True, WHITE, BLACK)
    textRect = text.get_rect()
    textRect.topleft = (10, 10)
    screen.blit(text, textRect)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            last_key = event.key
    food_eaten = snake.get_move(last_key, food_pos)
    if food_eaten:
        food_pos = generate_food_position()
    if snake.game_over():
        game_over_text = font.render('Game Over', True, RED, BLACK)
        game_over_rect = game_over_text.get_rect()
        game_over_rect.center = (WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2)
        screen.blit(game_over_text, game_over_rect)
        pygame.display.flip()
        pygame.time.wait(3000)
        running = False

    for segment in snake.body:
        pygame.draw.rect(screen, snake.color, (*segment, GRID_SIZE, GRID_SIZE))

    pygame.draw.rect(screen, RED, (*food_pos, GRID_SIZE, GRID_SIZE))

    pygame.display.flip()
    clock.tick(4)

pygame.quit()