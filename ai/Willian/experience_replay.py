from collections import deque
import random

class ReplayMemory():

  def __init__(self, maxlen, seed = None) -> None:
    self.memory = deque([], maxlen=maxlen)

    # Optional seed for reproducibility
    if seed is not None:
      random.seed(seed)

  def append(self, transition):
    self.memory.append(transition)

  def sample(self, sample_size = 1):
    return random.sample(self.memory, sample_size)

  def __len__(self):
    return len(self.memory)