from abc import ABC, abstractmethod
import torch, torch.nn as nn

class AI(nn.Module, ABC):
    def __init__(self, team: int) -> None:
        super(AI, self).__init__()
        self.team = team

    @abstractmethod
    def get_action(self, view: dict):
        """ 
            Parameters:
                view: data from each cell inside the agents rage of view
            Return:
                action: which contains what action agent takes, value range from
                0 to 9, 0-7 are move actions in corresponding direction, 8 is attack,
                and 9 is idle.
        """
        pass
    
    @abstractmethod
    def get_reward(self, agents: dict, *args):
        """
            This function must calculate how to reward a tem of agents based on
            the actions taken after training iteration.
            Think of it as an equation on what benefits the overall goals of your
            agents and what are impediments to those goals.
            Example: Total life of my team - total life of enemy team
            Parameters:
                agents: dictionary with agents by position
            Return:
                reward value for training the AI
        """
        pass

    def clip_action(self, action: tuple):
        """
            Clips the first value of the action into recognizeable action
            0-7 - Move
            8   - Attack
            9   - Idle
        """
        return min(max(action, 0), 9)