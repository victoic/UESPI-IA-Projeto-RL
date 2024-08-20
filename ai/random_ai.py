from ai.ai import AI
import random

class RandomAI(AI):
    def get_action(self, agent, view: dict):
        """ 
            Parameters:
                view: data from each cell inside the agents rage of view
            Return:
                action: which contains what action agent takes, value range from
                0 to 9, 0-7 are move actions in corresponding direction, 8 is attack,
                and 9 is idle.
        """
        return random.randint(0, 9)
    
    def turn_reward(self, team: int, action: int, list_agents: list) -> None:
        pass
    
    def get_reward(self, agents: dict, *args):
        return 0

class DumbAI(AI):
    def get_action(self, agent, view: dict):
        """ 
            Parameters:
                view: data from each cell inside the agents rage of view
            Return:
                action: which contains what action agent takes, value range from
                0 to 9, 0-7 are move actions in corresponding direction, 8 is attack,
                and 9 is idle.
        """
        enemies_pos = []
        enemies_dist = []
        for pos in view:
            cell = view[pos]
            if cell[-2] > -1 and cell[-2] != agent.team:
                enemies_pos.append((cell[0], cell[1]))
                dist = ((agent.pos[0] - cell[0])**2 + (agent.pos[1] - cell[1])**2)**(1/2)
                enemies_dist.append(dist)
        
        prob = random.random()
        action = 9
        if prob <= 0.9:
            if len(enemies_dist) > 0:
                i = enemies_dist.index(min(enemies_dist))
                delta_pos = (enemies_pos[i][0] - agent.pos[0], enemies_pos[i][1] - agent.pos[1])
                if abs(delta_pos[0]) <= agent.attack_range and abs(delta_pos[1]) <= agent.attack_range:
                    action = 8
                else:
                    direction = [0, 0]
                    if delta_pos[0] != 0:
                        direction[0] = delta_pos[0]/abs(delta_pos[0])
                    if delta_pos[1] != 0:
                        direction[1] = delta_pos[1]/abs(delta_pos[1])
                    direction = tuple(direction)
                    
                    action = agent.DIRECTIONS.index(direction)
            else:
                action = random.randint(0, 7)
        return action
    
    def turn_reward(self, team: int, action: int, list_agents: list) -> None:
        pass
    
    def get_reward(self, agents: dict, *args):
        return 0