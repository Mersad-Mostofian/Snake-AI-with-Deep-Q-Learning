import os, sys
sys.path.append(os.path.abspath("./classes"))
sys.path.append(os.path.abspath("./models"))
import pygame
from snake import Snake
from qTrainer import qTrainer
from linear_qnet import linear_qnet
from agent import Agent
import numpy as np
import random

WINDOW_SIZE = [400, 400]
GRID_SIZE = 20

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

weights_dir = './weights'
os.makedirs(weights_dir, exist_ok=True)


def generate_food_position():
    while True:
        food_pos = [
            random.randint(0, (WINDOW_SIZE[0] // GRID_SIZE) - 1) * GRID_SIZE,
            random.randint(0, (WINDOW_SIZE[1] // GRID_SIZE) - 1) * GRID_SIZE
        ]
        if food_pos not in snake.body:
            return food_pos

model = linear_qnet(input_shape=16, hidden_size=32, action_nums=4)
trainer = qTrainer(model)
agent = Agent(model)

latest_weights = None
if os.path.exists(weights_dir):
    weight_files = os.listdir(weights_dir)
    weight_files = [f for f in weight_files if f.endswith(".h5")]
    if weight_files:
        latest_weights = os.path.join(weights_dir, sorted(weight_files)[-1])
        model.load_weights(latest_weights)
        print(f'weights {latest_weights} loaded!')

pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption('Snake')
clock = pygame.time.Clock()

try:
    font = pygame.font.Font('./sewer.ttf', 32)
except FileNotFoundError:
    font = pygame.font.SysFont(None, 32)


apple_img = pygame.image.load("apple.png")
apple_img = pygame.transform.scale(apple_img, (GRID_SIZE, GRID_SIZE))
head_img = pygame.image.load("head.png")
head_img = pygame.transform.scale(head_img, (GRID_SIZE, GRID_SIZE))

snake = Snake(1, (0, 255, 0), WINDOW_SIZE, GRID_SIZE)
movement_keys = [pygame.K_w, pygame.K_d, pygame.K_s, pygame.K_a]

best_score = 0




for episode in range(50000):
    food_pos = generate_food_position()
    state = snake.get_state(food_pos)

    while not snake.game_over():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.fill(BLACK)
        text = font.render(f'Score: {snake.get_score()}', True, WHITE, BLACK)
        textRect = text.get_rect()
        textRect.topleft = (10, 10)
        screen.blit(text, textRect)

        text_episode = font.render(f'Episode: {episode}', True, WHITE, BLACK)
        textRect_episode = text_episode.get_rect()
        textRect_episode.topright = (185, 50)
        screen.blit(text_episode, textRect_episode)

        action = agent.get_action(state)
        food_eaten = snake.get_move(movement_keys[np.argmax(action)], food_pos)
        reward = snake.get_reward(food_pos)
        next_state = snake.get_state(food_pos)
        done = snake.game_over()

        trainer.train_step(np.array([state], dtype=np.float32),
                            np.array([action], dtype=np.float32),
                              np.array([reward], dtype=np.float32),
                                np.array([next_state], dtype=np.float32),
                                  np.array([done], dtype=np.float32))
        agent.store_exprience(state, action, reward, next_state, done)
        agent.replay(trainer)

        state = next_state

        if food_eaten:
            food_pos = generate_food_position()
        for i,segment in enumerate(snake.body):
            if i == len(snake.body)-1:
                screen.blit(head_img, (segment[0], segment[1]))
            else:
                pygame.draw.rect(screen, snake.color, (*segment, GRID_SIZE, GRID_SIZE))

        screen.blit(apple_img, (food_pos[0], food_pos[1]))

        pygame.display.flip()
        clock.tick(10000000)

    game_over_text = font.render('Game Over', True, RED, BLACK)
    game_over_rect = game_over_text.get_rect()
    game_over_rect.center = (WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2)
    screen.blit(game_over_text, game_over_rect)
    pygame.display.flip()
    pygame.time.wait(200)

    if best_score < snake.get_score():
        best_score = snake.get_score()
        model.save_weights(f'{weights_dir}/snake_weights.h5')

    agent.update_epsilon()
    snake = Snake(1, (0, 255, 0), WINDOW_SIZE, GRID_SIZE)
pygame.quit()