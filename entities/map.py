import random
from entities import Agent
class Map:
    MAX_WIDTH = 80
    MAX_HEIGHT = 40
    def __init__(self) -> None:
        self.list_agents = []
        self.agents: dict = {}
        self.blocks: dict = {}
        self.exp: dict = {}
        
        self.pos_by_id: dict = {}
        self.id_by_speed: dict = {}
        
        self.width: int = random.randint(self.MAX_WIDTH//2, self.MAX_WIDTH)
        self.height: int = random.randint(self.MAX_HEIGHT//2, self.MAX_HEIGHT)

    def is_occupied(self, pos: tuple[int]):
        return tuple(pos) in self.agents or tuple(pos) in self.blocks

    def add_agent(self, agent: Agent):
        x, y = agent.pos
        if self.is_inbounds(agent.pos) and not self.is_occupied(agent.pos):
            self.agents[agent.pos] = agent
            self.pos_by_id[agent.ID] = agent.pos
            if not agent.speed in self.id_by_speed:
                self.id_by_speed[agent.speed] = []
            self.id_by_speed[agent.speed].append(agent.ID)
            self.list_agents.append(agent)
            return True
        return False
    
    def add_block(self, pos: tuple[int]):
        x, y = pos
        if self.is_inbounds(pos) and not self.is_occupied(pos):
            self.blocks[pos] = True
            return True
        return False

    def is_inbounds(self, pos: tuple[int]):
        return pos[0] >= 0 and pos[0] < self.height and \
                pos[1] >= 0 and pos[1] < self.width

    def agent_move(self, ID: int, direction: int):
        assert ID in self.pos_by_id
        old_pos = self.pos_by_id[ID]
        new_pos = (old_pos[0] + Agent.DIRECTIONS[direction][0],
                    old_pos[1] + Agent.DIRECTIONS[direction][1])
        if not self.is_occupied(new_pos) and self.is_inbounds(new_pos):
            self.pos_by_id[ID] = new_pos
            
            self.agents[new_pos] = self.agents[old_pos]
            self.agents[new_pos].move(new_pos)
            
            del self.agents[old_pos]
            agent = self.agents[new_pos]

            # if agent moves into exp place
            if new_pos in self.exp:
                # we store its current speed, in case it changes
                agent_speed = agent.speed
                # we add the experience to the agent
                agent.get_exp(self.exp[new_pos])
                # remove the exp
                del self.exp[new_pos]
                # if the agent's speed chagend
                if agent.speed != agent_speed:
                    # we get the index where the agent's ID was stored in self.id_by_speed
                    index = self.id_by_speed[agent_speed].index(self.agents[new_pos].ID)
                    # and delete that index
                    del self.id_by_speed[agent_speed][index]
                    # check if the speed is already an index, if not create it
                    if not self.agents[new_pos].speed in self.id_by_speed:
                        self.id_by_speed[self.agents[new_pos].speed] = []
                    # add the agent's ID to is new place in self.id_by_index
                    self.id_by_speed[self.agents[new_pos].speed].append(self.agents[new_pos].ID)

    def agent_attack(self, ID: int):
        assert ID in self.pos_by_id
        pos = self.pos_by_id[ID]
        agent: Agent = self.agents[pos]
        for dx in range(-agent.attack_range, agent.attack_range+1):
            for dy in range(-agent.attack_range, agent.attack_range+1):
                new_pos = (pos[0] + dx, pos[1] + dy)
                if new_pos in self.agents:
                    neighbor = self.agents[new_pos]
                    if agent.team != neighbor.team:
                        neighbor.take_hit(agent.strength)

    def clear_dead(self):
        to_eliminate = []
        for pos in self.agents:
            agent = self.agents[pos]
            if agent.life <= 0:
                to_eliminate.append(agent)
        
        for agent in to_eliminate:
            index = self.id_by_speed[agent.speed].index(agent.ID)
            del self.id_by_speed[agent.speed][index]
            del self.pos_by_id[agent.ID]
            del self.agents[agent.pos]
                

    def get_pos_data(self, pos: tuple[int]):
        # data list: x, y, is_out_of_bounds, is_empty, is_block,
        #            is_agent, agent_id, agent_team, agent_life
        data = [pos[0], pos[1], 0, 1, 0, 0, -1, -1, -1]
        if not self.is_inbounds(pos):
            data[2] = 1
        if pos in self.blocks:
            data[3] = 0
            data[4] = 1
        elif pos in self.agents:
            data[3] = 0
            data[5] = 1
            data[6] = self.agents[pos].ID
            data[7] = self.agents[pos].team
            data[8] = self.agents[pos].life
        return data

    def get_view(self, pos: tuple[int]):
        RANGE = Agent.RANGE
        data: dict = {}
        c_i = 0
        for i in range(pos[0]-RANGE, pos[0]+RANGE+1):
            c_j = 0
            c_i +=1
            for j in range(pos[1]-RANGE, pos[1]+RANGE+1):
                c_j +=1
                data[(i,j)] = self.get_pos_data((i, j))
        return data
    
    def generate_exp(self):
        x = random.randint(0, self.height)
        y = random.randint(0, self.width)
        
        while self.is_occupied((x, y)):
            x = random.randint(0, self.height)
            y = random.randint(0, self.width)

        if (x,y) in self.exp:
            self.exp[(x, y)] += 1
        else:
            self.exp[(x, y)] = 1

    def total_life(self):
        teams = [0, 0]
        for agent_pos in self.agents:
            agent = self.agents[agent_pos]
            teams[agent.team] += agent.life
        return teams

    def __str__(self) -> str:
        s = ""
        for i in range(self.height):
            for j in range(self.width):
                if tuple([i,j]) in self.agents:
                    s += str(self.agents[(i, j)].ID)+" "
                elif tuple([i,j]) in self.blocks:
                    s += "* "
                elif tuple([i,j]) in self.exp:
                    s += "e "
                else:
                    s += "- "
            s += "\n"
        for i, team_life in enumerate(self.total_life()):
            s += f"Team {i} life: {team_life}\n"
        return s