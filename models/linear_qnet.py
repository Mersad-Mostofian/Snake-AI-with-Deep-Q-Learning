import tensorflow as tf


def linear_qnet(input_shape, hidden_size, action_nums) -> tf.keras.Model:
    inputs = tf.keras.layers.Input(shape=input_shape, name="input_layer")
    hidden = tf.keras.layers.Dense(hidden_size, activation="relu", name="hidden_layer")(inputs)
    action = tf.keras.layers.Dense(action_nums, activation="linear", name="output_layer")(hidden)
    return tf.keras.Model(inputs=inputs, outputs=action)
