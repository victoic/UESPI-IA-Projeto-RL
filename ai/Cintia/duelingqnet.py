# @title DuelingDeepQNetwork
# dueling.py

import torch
import torch.nn as nn
import torch.optim as optim
import random
import math

from ai.ai import AI
from entities.map import Map

class DuelingQNetwork(nn.Module):
    def __init__(self, state_size: int = 1089, action_size: int = 10):
        super(DuelingQNetwork, self).__init__()


        # Feature layer
        self.feature_layer = nn.Sequential(
            nn.Linear(state_size, 128),  # Assuming 128 features, adjust if needed
            nn.ReLU(),
            nn.Linear(128, 128),  # Another layer for more complexity
            nn.ReLU()
        )

        # Value stream
        self.value_stream = nn.Sequential(
            nn.Linear(128, 64),  # Adjust output size if needed
            nn.ReLU(),
            nn.Linear(64, 1)  # Outputting a single value
        )

        # Advantage stream
        self.advantage_stream = nn.Sequential(
            nn.Linear(128, 64),  # Adjust output size if needed
            nn.ReLU(),
            nn.Linear(64, action_size)  # Outputting advantages for each action
        )

    def forward(self, x):
        pass

class DuelingQNetworkAI(AI):
    def __init__(self, team: int, state_size: int = 1089) -> None:
        super().__init__(team)
        self.buffer_size = 1000  # Defina o tamanho do buffer
        self.criterion = nn.MSELoss()
        self.team = team
        #self.map = map
        self.gamma = 0.99
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.memory = []
        self.batch_size = 32
        self.tau = 0.005
        self.rewards = {}

        # Calcula o tamanho do estado com base no mapa e nas informações do agente
        #state_size = map.MAX_WIDTH * map.MAX_HEIGHT * 6

        self.model = nn.Sequential(
            nn.Linear(state_size, 128),
            nn.ReLU(),
            nn.Linear(128, 128),
            nn.ReLU()
        )

        self.value_stream = nn.Sequential(
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 1)
        )

        self.advantage_stream = nn.Sequential(
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 9)  # 9 ações possíveis
        )

        self.target_model = nn.Sequential(
            nn.Linear(state_size, 128),
            nn.ReLU(),
            nn.Linear(128, 128),
            nn.ReLU()
        )

        self.target_value_stream = nn.Sequential(
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 1)
        )

        self.target_advantage_stream = nn.Sequential(
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 9) # 9 ações possíveis
        )

        for target_param, param in zip(self.target_model.parameters(), self.model.parameters()):
            target_param.data.copy_(param.data)
        for target_param, param in zip(self.target_value_stream.parameters(), self.value_stream.parameters()):
            target_param.data.copy_(param.data)
        for target_param, param in zip(self.target_advantage_stream.parameters(), self.advantage_stream.parameters()):
            target_param.data.copy_(param.data)

        self.optimizer = optim.Adam(self.model.parameters(), lr=self.learning_rate)

    #seleciona a ação que o agente vai tomar em um determinado turno
    def get_action(self, agent, view: dict):
        #state = self.process_view(view)
        state = torch.tensor([item for data in view.values() for item in data], dtype=torch.float32).squeeze()
        
        if random.random() < self.epsilon:
            return random.randint(0, 9)
        else:
            with torch.no_grad():
                qvals = self.model(state)
            return torch.argmax(qvals).item()

    #converte a visão do agente em um tensor que vai ser passado como entrada para a rede neural
    def process_view(self, view: dict):
        state = torch.zeros(5, self.map.height, self.map.width)
        for pos, cell in view.items():
            x, y = pos
            if 0 <= x < self.map.height and 0 <= y < self.map.width:
                if cell[2] == 1:
                    state[0, x, y] = 1  # Out of bounds
                elif cell[4] == 1:
                    state[1, x, y] = 1  # Block
                elif cell[5] == 1:
                    if cell[7] == self.team:
                        state[2, x, y] = 1  # Friendly agent
                    else:
                        state[3, x, y] = 1  # Enemy agent
                elif cell[3] == 1:
                    state[4, x, y] = 1  # Empty
        return state.view(1, -1)

    #armazena a experi~encia na memoria de repetição
    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))
        if len(self.memory) > self.buffer_size:
            self.memory.pop(0)

    #realiza o treinamento na rede neural usando as experiências armazenadas
    def replay(self, batch_size):
        if len(self.memory) < batch_size:
            return
        batch = random.sample(self.memory, batch_size)
        states, actions, rewards, next_states, dones = zip(*batch)

        states = torch.cat(states)
        actions = torch.tensor(actions, dtype=torch.int64)
        rewards = torch.tensor(rewards, dtype=torch.float32)
        next_states = torch.cat(next_states)
        dones = torch.tensor(dones, dtype=torch.bool)

        current_q_values = self.model(states).gather(1, actions.unsqueeze(1))
        next_q_values = self.target_model(next_states).max(1)[0].detach()
        target_q_values = rewards + self.gamma * next_q_values * (~dones)

        loss = self.criterion(current_q_values, target_q_values.unsqueeze(1))
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        self.learn_step_counter += 1
        if self.learn_step_counter % self.update_target_frequency == 0:
            self.target_model.load_state_dict(self.model.state_dict())

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay


    #calcula a recompensa
    def turn_reward(self, team: int, ID: int, previous_pos: tuple, action: int, list_agents: list) -> None:
        agent = next((a for a in list_agents if a.ID == ID), None)
        if agent is None:
            return

        reward = 0

        # Recompensa por se aproximar de inimigos
        closest_enemy_dist = float('inf')
        for other_agent in list_agents:
            if other_agent.team != team:
                dist = math.sqrt((previous_pos[0] - other_agent.pos[0])**2 + (previous_pos[1] - other_agent.pos[1])**2)
                if dist < closest_enemy_dist:
                    closest_enemy_dist = dist

        # Recompensa por atacar um inimigo e causar dano
        if action == 8:
            for other_agent in list_agents:
                if other_agent.team != team and math.dist(agent.pos, other_agent.pos) <= agent.attack_range:
                    reward += 2

        # Penalidade por atacar um aliado ou um espaço vazio
        if action == 8 and reward < 2:
            reward -= 1

        # Recompensa por obter experiência
        if action <= 7 and agent.pos in self.map.exp:
            reward += 1

        # Recompensa por movimento
        if agent.pos != previous_pos and action <= 7:
            reward += 0.5

        # Penalidade por ficar parado (idle)
        if action == 9:
            reward -= 0.5

        # Penalidade por morte
        if agent.life <= 0:
            reward -= 2

        # Atualizar a vida anterior do time inimigo
        self.previous_enemy_life = self.map.total_life()[1 - team]

        print(f"Agent {ID} - Reward: {reward}, Action: {action}, Life: {agent.life}")

        # Armazenar a experiência na memória de repetição
        current_state = self.process_view(self.map.get_view(previous_pos))
        next_state = self.process_view(self.map.get_view(agent.pos))
        done = agent.life <= 0

        self.remember(current_state, action, reward, next_state, done)

        # Treinar o modelo com repetição
        self.replay(batch_size=32)

    #calcula a recompensa total do agente ao final do episódio
    def get_reward(self, agents, *args):
        total_reward = 0
        if isinstance(agents, dict):  # Check if agents is a dictionary
            for agent in agents.values():
                if agent.team == self.team:
                    total_reward += agent.life
        elif isinstance(agents, list):  # Check if agents is a list
            for agent in agents:
                if agent.team == self.team:
                    total_reward += agent.life
        return total_reward
