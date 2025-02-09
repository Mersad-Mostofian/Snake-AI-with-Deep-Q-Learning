import numpy as np
import random
import datetime
import pygame

class Snake:
    def __init__(self, id, color,window_size, grid_size):
        self.id = id
        self.color = color
        self.head_pos = [random.randint(1, (window_size[0] // grid_size) - 1) * grid_size,
                         random.randint(1, (window_size[1] // grid_size) - 1) * grid_size]
        self.body = [[self.head_pos.copy()[0]-grid_size, self.head_pos.copy()[1]-grid_size], self.head_pos.copy()]
        self.length = 1
        self.score = 0
        self.direction = random.choice(['U','R','D','L'])
        self.window_size = window_size
        self.grid_size = grid_size

        print(f'[{datetime.datetime.now()}] ---> Snake with id-{self.id} is Create!')
    
    def __del__(self):
        print(f'[{datetime.datetime.now()}] ---> Snake with id-{self.id} is dead!')

    def get_move(self, movement_key, food_pos):
        next_head_pos = None
        next_direction = None

        if (movement_key == pygame.K_d and self.direction == 'R') or \
        (movement_key == pygame.K_a and self.direction == 'L') or \
        (movement_key == pygame.K_w and self.direction == 'U') or \
        (movement_key == pygame.K_s and self.direction == 'D'):
            next_direction = self.direction
        elif (movement_key == pygame.K_d and self.direction == 'L') or \
            (movement_key == pygame.K_a and self.direction == 'R') or \
            (movement_key == pygame.K_w and self.direction == 'D') or \
            (movement_key == pygame.K_s and self.direction == 'U'):
            next_direction = self.direction
        else:
        
            if movement_key == pygame.K_d and self.direction != 'L':
                next_direction = 'R'
                next_head_pos = [self.head_pos[0] + self.grid_size, self.head_pos[1]]
            elif movement_key == pygame.K_a and self.direction != 'R':
                next_direction = 'L'
                next_head_pos = [self.head_pos[0] - self.grid_size, self.head_pos[1]]
            elif movement_key == pygame.K_w and self.direction != 'D':
                next_direction = 'U'
                next_head_pos = [self.head_pos[0], self.head_pos[1] - self.grid_size]
            elif movement_key == pygame.K_s and self.direction != 'U':
                next_direction = 'D'
                next_head_pos = [self.head_pos[0], self.head_pos[1] + self.grid_size]

        food_eaten = False
        if next_direction:
            
            if next_head_pos is None:
                
                if self.direction == 'R':
                    next_head_pos = [self.head_pos[0] + self.grid_size, self.head_pos[1]]
                elif self.direction == 'L':
                    next_head_pos = [self.head_pos[0] - self.grid_size, self.head_pos[1]]
                elif self.direction == 'U':
                    next_head_pos = [self.head_pos[0], self.head_pos[1] - self.grid_size]
                elif self.direction == 'D':
                    next_head_pos = [self.head_pos[0], self.head_pos[1] + self.grid_size]

            next_head_pos[0] %= self.window_size[0]
            next_head_pos[1] %= self.window_size[1]

            self.head_pos = next_head_pos
            self.body.append(self.head_pos.copy())

            food_eaten = self.eat_food(food_pos)
            if not food_eaten:
                self.body.pop(0)
            else:
                self.length += 1
                self.score += 1

            self.direction = next_direction

        return food_eaten

    def eat_food(self, food_pos):
        return self.head_pos == food_pos

    def game_over(self):
        return self.body.count(self.head_pos) > 1
    
    def get_score(self):
        return self.score


    def get_reward(self, food_pos):
        reward = -0.1  

        if self.game_over():
            reward -= 10.0

        if self.eat_food(food_pos):
            reward += 10.0

        old_distance = abs(self.body[-2][0] - food_pos[0]) + abs(self.body[-2][1] - food_pos[1])
        new_distance = abs(self.head_pos[0] - food_pos[0]) + abs(self.head_pos[1] - food_pos[1])

        if new_distance < old_distance:
            reward += 2.0  
        else:
            reward -= 2.0

        return reward

    def get_state(self, food_pos):
        head_x, head_y = self.head_pos
        food_x, food_y = food_pos

        wall_left = (head_x - self.grid_size) < 0
        wall_right = (head_x + self.grid_size) >= self.window_size[0]
        wall_top = (head_y - self.grid_size) < 0
        wall_bottom = (head_y + self.grid_size) >= self.window_size[1]

        body_left = [head_x - self.grid_size, head_y] in self.body
        body_right = [head_x + self.grid_size, head_y] in self.body
        body_top = [head_x, head_y - self.grid_size] in self.body
        body_bottom = [head_x, head_y + self.grid_size] in self.body

     
        food_left = food_x < head_x
        food_right = food_x > head_x
        food_top = food_y < head_y
        food_bottom = food_y > head_y

        moving_left = self.direction == 'L'
        moving_right = self.direction == 'R'
        moving_up = self.direction == 'U'
        moving_down = self.direction == 'D'

        return np.array([
            wall_left, wall_right, wall_top, wall_bottom,
            body_left, body_right, body_top, body_bottom,
            food_left, food_right, food_top, food_bottom,
            moving_left, moving_right, moving_up, moving_down
        ], dtype=int)