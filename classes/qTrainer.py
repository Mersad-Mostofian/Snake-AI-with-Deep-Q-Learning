import tensorflow as tf
import tensorflow.keras as keras
import os, sys
import numpy as np

sys.path.append(os.path.abspath("../models"))
from linear_qnet import linear_qnet

class qTrainer():
    def __init__(self, model, learning_rate=0.001, gamma=0.99):
        self.model = model
        self.learning_rate = learning_rate
        self.gamma = gamma
        self.optimizer = keras.optimizers.Adam(learning_rate=self.learning_rate)
        self.loss = keras.losses.MeanSquaredError()


    @tf.function
    def train_step(self, state, action, reward, next_state, done):
        reward = tf.cast(reward, tf.float32)
        
        future_rewards = tf.reduce_max(self.model(next_state), axis=1)
        Qval = reward + tf.math.multiply(self.gamma, future_rewards)
        Qval = tf.math.multiply(Qval, (1.0 - done))

        masks = action

        with tf.GradientTape() as tape:
            q_values = self.model(state)

            q_action = tf.reduce_sum(tf.multiply(q_values, masks), axis=1)
            loss = self.loss(Qval, q_action)

        grads = tape.gradient(loss, self.model.trainable_variables)
        self.optimizer.apply_gradients(zip(grads, self.model.trainable_variables))
