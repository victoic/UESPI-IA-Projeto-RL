class Agent:
    CUR_ID = 0
    RANGE = 10
    MAX_STRENGTH = 5
    MAX_LIFE = 10
    LEVEL_UP = 3
    DIRECTIONS = [
        (0, 1), (1,1),       # RIGHT, DOWN-RIGHT
        (1, 0), (1, -1),     # DOWN, DOWN-LEFT
        (0, -1), (-1, -1),   # LEFT, TOP-LEFT
        (-1, 0), (-1, 1)     # TOP, TOP-RIGHT
    ]
    
    def __init__(self, team: int, pos: tuple[int], print_log: bool = False):
        self.print_log = print_log
        
        self.ID = Agent.CUR_ID
        Agent.CUR_ID += 1
        self.team = team
        self.pos = pos
        
        self.life = Agent.MAX_LIFE

        self.level = 0
        self.exp = 0
        self.total_exp = 0
        self.needed_exp = Agent.LEVEL_UP

        self.attack_range = 1
        self.strength = 1
        self.speed = 1

        self.last_action = 9

    def move(self, new_pos: tuple[int]):
        if self.print_log: print(f"Agent {self.ID} moved from {self.pos} to {new_pos}")
        self.pos = new_pos

    def take_hit(self, strength):
        self.life -= strength
        if self.print_log: print(f"\tAgent {self.ID} takes {strength} damage. CURRENT: {self.life}")

    def get_exp(self, exp):
        if self.print_log: print(f"Agent {self.ID} got {exp} exp points.")
        self.exp += exp
        self.total_exp += exp
        if self.exp >= self.needed_exp:
            self.exp - self.needed_exp
            self.needed_exp += Agent.LEVEL_UP
            self.level += 1

            if self.print_log: print(f"\tLEVEL UP: {self.level}")
        
            if self.level % 3 == 0:
                self.speed += 1
                if self.print_log: print(f"\tSpeed increased to {self.speed}")
            elif self.level % 2 == 0:
                self.attack_range = min(self.attack_range+1, Agent.RANGE)
                if self.print_log: print(f"\tAttack range increased to {self.attack_range}")
            else:
                self.strength = min(self.strength+1, Agent.MAX_STRENGTH)
                if self.print_log: print(f"\tStrength increased to {self.strength}")
            