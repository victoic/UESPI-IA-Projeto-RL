from entities import Agent, Map
from ai.ai import AI
import random, json, os, time, math

class Match:
    NEW_EXP_EVERY = 10
    NUM_ADD_EXP = 15
    MAX_TURN = 60
    NUM_BLOCKS = 5

    ACTIONS = [
        "MOVE RIGHT", "MOVE DOWN-RIGHT", "MOVE DOWN", "MOVE DOWN-LEFT", "MOVE LEFT", "MOVE TOP-LEFT", "MOVE TOP", "MOVE TOP-RIGHT", 
        "ATTACK",
        "IDLE"
    ]

    def __init__(self, team_size: int, team_0_ai, team_1_ai, 
                 print_log: bool = False, presentation: bool = False,
                 train: bool = False, keep_log: bool = False, 
                 sleep_time: float = 0.005) -> None:
        self.print_log = print_log
        self.presentation = presentation
        self.keep_log = keep_log
        self.sleep_time = sleep_time

        self.map = Map()

        self.ais: list[AI] = [team_0_ai, team_1_ai]

        self.turn_actions: dict = {}
        self.log = {}
        self.turn = 0
        if self.print_log: print(f"Preparing map of size {self.map.height}, {self.map.width}.")

        for team in range(2):
            if self.print_log: print(f"Preparing team {team+1}.")
            # generate 10 random blocks for each team's side
            for i in range(Match.NUM_BLOCKS):
                failed = True
                while failed:
                    pos = self.generate_init_pos(team)
                    failed = not self.map.add_block(pos)
                    if self.print_log: print(f"Tried adding block to position {pos} | Failed: {failed}")
                if self.print_log: print(f"Added block to position {pos}")
            
            # generate {team_size} agents for each team's side
            for a in range(team_size):
                failed = True
                while failed:
                    pos = self.generate_init_pos(team)
                    failed = not self.map.add_agent(Agent(team, pos, print_log=self.print_log))
                    if failed: Agent.CUR_ID -= 1
                    if self.print_log: print(f"Tried adding agent to {pos} | Failed: {failed}")
                if self.print_log: print(f"Added agent to position {pos}")

            self.generate_exp()

    def generate_init_pos(self, team):
        min_w = int(team * self.map.width / 2)
        max_w = int(min_w + (self.map.width / 2))
        min_h = 0
        max_h = self.map.height
        return (random.randint(min_h, max_h), 
                random.randint(min_w, max_w))
    
    def generate_exp(self):
        for i in range(Match.NUM_ADD_EXP):
            self.map.generate_exp()
    
    def play_turn(self):
        speeds = sorted(list(self.map.id_by_speed.keys()), reverse=True)
        for speed in speeds:
            for id in sorted(self.map.id_by_speed[speed]):
                pos = self.map.pos_by_id[id]
                agent = self.map.agents[pos]
                if agent.life <= 0: continue;
                data = self.map.get_view(agent.pos)
                
                action = self.ais[agent.team].get_action(agent, self.map.get_view(agent.pos))
                action = self.ais[agent.team].clip_action(action)
                if self.print_log: print(f"Agent {agent.ID} (POSITION {agent.pos}) makes action {Match.ACTIONS[action]} ({action})")
                if (action <= 7):
                    self.map.agent_move(agent.ID, action)
                elif (action == 8):
                    self.map.agent_attack(agent.ID)
                self.turn_actions[agent.ID] = action
            
            self.log[self.turn] = self.turn_actions
            self.turn_actions
            self.turn_actions = {}
        self.turn += 1

    def __str__(self):
        s = f"{self.ais}"
        s += str(self.map)
        for agent in self.map.list_agents:
            s += f"Agent {agent.ID} - ({agent.pos}), "
        s += f"\nReward (Team 0): {self.ais[0].get_reward(self.map.list_agents, math.inf)}"
        s += f"\nReward (Team 1): {self.ais[1].get_reward(self.map.list_agents, math.inf)}"
        return s

    def play(self):
        while(self.turn < Match.MAX_TURN):
            if self.presentation: print(self)
            if self.print_log: print(f"START OF TURN {self.turn}")
            self.play_turn()
            self.map.clear_dead()
            if self.turn % Match.NEW_EXP_EVERY == 0:
                self.generate_exp()

            if self.print_log: print(f"END OF TURN {self.turn}")
            if self.presentation: time.sleep(self.sleep_time)
            if self.presentation: os.system('cls' if os.name == 'nt' else 'clear')
            if self.map.total_life()[0] <= 0 or self.map.total_life()[1] <= 0:
                break
        
        if self.presentation: print(self)

        if self.keep_log:
            with open("log.json", "w") as f:
                json.dump(self.log, f)