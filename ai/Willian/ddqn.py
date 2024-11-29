from ai.ai import AI
import torch, torch.nn as nn
import numpy as np
import random as rd

import ai.ai
class Ddqn(AI):

  def __init__(self, team: int, state_size: int = 1089, num_actions: int = 10):
    super(Ddqn, self).__init__(team)

    self.explore_policy = False
    self.epsilon = 0
    self.epsilon_decay = 0
    self.epsilon_min = 0
    self.num_action = num_actions
    self.epsilon_history = []

    # a previous trained maximum reward {'max_health_reward': 14, 'min_health_reward': -34, 'max_experience_reward': 21, 'min_experience_reward': -31}

    self.max_health_reward = None
    self.min_health_reward = None

    # initial values based in previous experiences
    self.max_experience_reward = 31
    self.min_experience_reward = -31
    
    
    self.max_total_reward = None
    self.min_total_reward = None

    self.linear = nn.Sequential(
      nn.Linear(in_features=state_size, out_features=256),
      nn.ReLU(inplace=True),

      nn.Linear(in_features=256, out_features=128),
      nn.ReLU(inplace=True),

      nn.Linear(in_features=128, out_features=num_actions)
    )

  def get_action(self, agent, view: dict):

    """
    It does more than get the action, it memorizes the state it was 
    before the action to use that in the trainer class 
    """
    self.state = [item for data in view.values() for item in data]
    
    state = torch.tensor(self.state, dtype=torch.float32).squeeze()

    self.state = state
    
    if(self.explore_policy):
      if rd.random() < self.epsilon:
        action = rd.randint(0, self.num_action - 1)
        action = torch.tensor(action, dtype=torch.int64)
      else:
        with torch.no_grad():
          q_values = self.linear(state)
        action = q_values.squeeze().argmax()
    else:
      with torch.no_grad():
          q_values = self.linear(state)

      action = q_values.squeeze().argmax()
    return action
  
  def turn_reward(self, team: int, action: int, list_agents: list) -> None:
    return self.get_reward(agents=list_agents)
    
  def get_reward(self, agents, *args):
    """
    The reward function will be based in the enemy team total health and experience
    """

    enemy_total_health = 0
    my_total_health = 0
    enemy_total_experience = 0
    my_total_experience = 0

    for agent in agents:

      if agent.team == 0:
        my_total_health += agent.life
        my_total_experience += agent.total_exp
      else:
        enemy_total_health += agent.life
        enemy_total_experience += agent.total_exp

    reward_by_health = my_total_health - enemy_total_health
    reward_by_experience = my_total_experience - enemy_total_experience

    total_reward = reward_by_health+reward_by_experience
    # these values are used to normalize the rewards
    self.update_rewards(reward_by_experience=reward_by_experience, reward_by_health=reward_by_health, total_reward=total_reward)
    
    normalized_health_reward, normalized_experience_reward = self.normalize_rewards(reward_by_health, reward_by_experience)

    healt_reward_weight = 0.6
    experience_reward_weight = 0.4

    normalized_reward = healt_reward_weight*normalized_health_reward+experience_reward_weight*normalized_experience_reward
    


    return normalized_reward
  
  def exploration_policy(self, active, epsilon, epsilon_decay, epsilon_min):
    
    self.explore_policy = active

    self.epsilon        = epsilon 
    self.epsilon_min    = epsilon_min 
    self.epsilon_decay  = epsilon_decay 
    self.epsilon_history.append(self.epsilon)

  def decrease_exploration_rate(self):

    previous_epsilon = self.epsilon

    self.epsilon = max(previous_epsilon * self.epsilon_decay, self.epsilon_min)

    self.epsilon_history.append(self.epsilon)

  def forward(self, x):
    return self.linear(x)
  

  def update_rewards(self, reward_by_health, reward_by_experience, total_reward):
    """
    Atualiza os maiores e menores valores de recompensa para saúde e experiência.
    """
    # Atualiza os valores máximos e mínimos para health reward
    if self.max_health_reward is None or self.min_health_reward is None:
        self.max_health_reward = reward_by_health
        self.min_health_reward = reward_by_health
    else:
        self.max_health_reward = max(self.max_health_reward, reward_by_health)
        self.min_health_reward = min(self.min_health_reward, reward_by_health)

    # Atualiza os valores máximos e mínimos para experience reward
    self.max_experience_reward = max(self.max_experience_reward, reward_by_experience)
    self.min_experience_reward = min(self.min_experience_reward, reward_by_experience)

    # Atualiza os valores máximos e mínimos para total reward
    if self.max_total_reward is None or self.min_total_reward is None:
        self.max_total_reward = total_reward
        self.min_total_reward = total_reward
    else:
        self.max_total_reward = max(self.max_total_reward, total_reward)
        self.min_total_reward = min(self.min_total_reward, total_reward)

  def get_extreme_rewards(self):
    """
    Retorna os maiores e menores valores de recompensa já registrados.
    """
    return {
        "max_health_reward": self.max_health_reward,
        "min_health_reward": self.min_health_reward,
        "max_experience_reward": self.max_experience_reward,
        "min_experience_reward": self.min_experience_reward,
        "max_total_reward": self.max_total_reward,
        "min_total_reward": self.min_total_reward
    }
  
  def normalize_rewards(self, reward_by_health, reward_by_experience):
      
    # a team has 3 players, a player has maximum health of 10, thus
    # a team maximum health is 30
    max_health = 30
    normalized_health_reward = reward_by_health / max_health

    # Normalização de experiência baseada em valores dinâmicos
    max_observed_experience_reward = self.max_experience_reward
    min_observed_experience_reward = self.min_experience_reward

    normalized_experience_reward = reward_by_experience / max_observed_experience_reward

    normalized_experience_reward = 2 * (reward_by_experience - min_observed_experience_reward) / (max_observed_experience_reward - min_observed_experience_reward) - 1

    return (normalized_health_reward, normalized_experience_reward)