# 🐍 Snake AI with Deep Q-Learning 🚀

This project develops a Snake game using **Deep Q-Learning**. An agent 🤖 is trained using artificial neural networks (MLP) to play the game autonomously and achieve higher scores.

## 📌 Prerequisites

To run this project, install the following dependencies:

```bash
pip install numpy pygame tensorflow
```

## 📂 Project Structure

```
./
│── classes/
│   ├── agent.py       # 🧠 Reinforcement learning agent implementation
│   ├── qTrainer.py    # 🎯 Trainer for updating the Q-Learning model
│   ├── snake.py       # 🐍 Snake game implementation
│── models/
│   ├── linear_qnet.py # 🏗️ Neural network model for Q-value prediction
│── weights/           # 💾 Directory for storing trained model weights
│── main.py            # 🎮 Run the classic Snake game
│── train_main.py      # 🏋️ Run Snake with reinforcement learning
│── README.md          # 📜 Project documentation
```

## 🎮 Running the Classic Snake Game

To play the game manually using the WASD keys, run:

```bash
python main.py
```

## 🏆 Training the Reinforcement Learning Model

To train the model and observe the agent's learning progress, run:

```bash
python train_main.py
```

⚠️ **Note:** Training may take a long time ⏳, as the model is trained for **50,000 episodes**.

---

## 🧠 How Reinforcement Learning Works in This Project

### 📌 State Representation:
- 📍 Snake head position
- 🍏 Food position relative to the snake
- 🚧 Obstacles (walls and snake's body)
- 🧭 Current movement direction

### 🏗️ Neural Network Model:
- 🔹 One hidden layer with **32 neurons** and **ReLU activation**
- 🎯 Output consists of four values representing actions: **left, right, up, and down**

### 🎲 Action Selection Policy:
- 🎲 **Exploration**: The agent moves randomly in the early training phase.
- 🎯 **Exploitation**: The agent uses Q-values to make decisions after training.
- 📉 The **epsilon** value decreases gradually to encourage optimal decision-making.

### 🏋️ Trainer:
- 🔄 Q-Learning is applied using the **Bellman equation** update.
- 📏 **Mean Squared Error (MSE)** is used as the loss function to minimize Q-value differences.

---

## 🚀 Performance Improvements

✅ Increasing memory size in the agent to store more experiences  
✅ Implementing **Double Q-Learning** to reduce Q-value estimation errors  
✅ Adjusting the **gamma** value to emphasize future rewards  
✅ Evaluating model performance after training  

---


