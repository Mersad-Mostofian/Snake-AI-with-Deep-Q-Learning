import random
import numpy as np
from collections import deque

class Agent:
    def __init__(self, model, epsilon=1.0, epsilon_decay=0.995, epsilon_min=0.01, memory_size=5000):
        self.model = model
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min
        self.memory = deque(maxlen=memory_size)

    def store_exprience(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))


    
    def replay(self, trainer, batch_size=64):
        if len(self.memory) < batch_size:
            return  

        batch = random.sample(self.memory, batch_size)
        states, actions, rewards, next_states, dones = zip(*batch)

        trainer.train_step(
            np.array(states, dtype=np.float32),
            np.array(actions, dtype=np.float32),
            np.array(rewards, dtype=np.float32),
            np.array(next_states, dtype=np.float32),
            np.array(dones, dtype=np.float32)
        )
        
    def get_action(self, state):
        if random.uniform(0, 1) < self.epsilon:
            action_index = random.randint(0, 3)
        else:
            Qval = self.model.predict(np.array([state]))[0]
            Qval += np.random.randn(4) * 0.1 
            action_index = np.argmax(Qval)

        action = np.zeros(4)
        action[action_index] = 1.0
        return action

    def update_epsilon(self):
        self.epsilon = max(self.epsilon * self.epsilon_decay, self.epsilon_min)


