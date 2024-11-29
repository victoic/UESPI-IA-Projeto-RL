from ai import *
from entities import Match, Map, Agent

import pygad.torchga, torch

import argparse, importlib, os, math

class Tester:
    def __init__(self, model, other, iters: int = 10_000) -> None:
        self.model: torch.nn.Module = model
        self.other = other
        self.iterations = iters
    
    def test(self):
        results = []
        for i in range(self.iterations):
            print(f'Evaluating - Iteration {i}/{self.iterations}', end='\r')
            m = Match(3, model0, model1, presentation=False, sleep_time=0) 
            results.append(m.play())
        print(f'Evaluating - Iteration {i+1}/{self.iterations}')
        print(f'Victories:\t{results.count(1)}\t({results.count(1)/len(results)*100}%)')
        print(f'Defeats:\t{results.count(-1)}\t{results.count(-1)/len(results)*100}%)')
        print(f'Draws:\t{results.count(0)}\t{results.count(0)/len(results)*100}%)')

class Trainer:
    def __init__(self, model, other) -> None:
        self.model: torch.nn.Module = model
        self.other = other
        # This could be used for dynamic changes in training
        self.best_fitness = -math.inf

    def train(self, generations: int, parents: int):
        torch_ga = pygad.torchga.TorchGA(self.model, num_solutions=10)

        # Number of generations to train for
        num_generations = generations
        # Number of solutions to be selected as parents
        num_parents_mating = parents
        # We define the initial population/chromossomes/genes to be 
        # the initial weight of our model, this could be changed
        # to either use pygad.GA initialization methods, or, to 
        # initilize the weights before using it as initial population
        initial_population = torch_ga.population_weights

        # Create the Genetic Algorithm instance
        ga_instance = pygad.GA(num_generations=num_generations,
                            num_parents_mating=num_parents_mating,
                            initial_population=initial_population,
                            fitness_func=self.fitness,
                            on_generation=self.callback_generation
                            #parallel_processing=['thread', 4],
                            )
        # And finally run training
        ga_instance.run()
        torch.save(self.model.state_dict(), "last.pt")
        m = Match(3, self.model, self.other, presentation=True,
                  sleep_time=0.5)
        m.play(self.turn_callback)
        
    def train(self, generations: int, parents: int):
        torch_ga = pygad.torchga.TorchGA(self.model, num_solutions=10)

        # Number of generations to train for
        num_generations = generations
        # Number of solutions to be selected as parents
        num_parents_mating = parents
        # We define the initial population/chromossomes/genes to be 
        # the initial weight of our model, this could be changed
        # to either use pygad.GA initialization methods, or, to 
        # initilize the weights before using it as initial population
        initial_population = torch_ga.population_weights

        # Create the Genetic Algorithm instance
        ga_instance = pygad.GA(num_generations=num_generations,
                            num_parents_mating=num_parents_mating,
                            initial_population=initial_population,
                            fitness_func=self.fitness,
                            on_generation=self.callback_generation
                            #parallel_processing=['thread', 4],
                            )
        # And finally run training
        ga_instance.run()
        torch.save(self.model.state_dict(), "last.pt")
        m = Match(3, self.model, self.other, presentation=True,
                  sleep_time=0.5)
        m.play(self.turn_callback)
    
    def fitness(self, ga_instance: pygad.GA, solution, sol_idx):
        model_weights_dict = pygad.torchga.model_weights_as_dict(model=self.model,
                                                    weights_vector=solution)
        self.model.load_state_dict(model_weights_dict)
        
        m = Match(3, self.model, self.other, presentation=False, sleep_time=0.01, print_log=False)
        m.play(callback=self.turn_callback)
        Agent.CUR_ID = 0
        
        solution_fitness = self.model.get_reward(m.map.list_agents, ga_instance.generations_completed)
        return solution_fitness

    def turn_callback(self, team: int, ID: int, previous_pos: tuple, action: int, list_agents: list[Agent]):
        if team == 0:
            self.model.turn_reward(team, ID, previous_pos, action, list_agents)
    
    def callback_generation(self, ga_instance: pygad.GA):
        """
        Method called after each generation
        Parameters:
            ga_instante (pygad.GA): instance of Genetic Algorithm training
        Returns:
            None | str: if returns "stop" training is halted
        """
        # Right now this display our generation and fitness
        print("Generation = {generation}".format(generation=ga_instance.generations_completed))
        print("Fitness    = {fitness}".format(fitness=ga_instance.best_solution()[1]))
        
        # But we could do so much more!
        model_weights_dict = pygad.torchga.model_weights_as_dict(model=self.model,
                                                    weights_vector=ga_instance.best_solution()[0])
        if ga_instance.best_solution()[1] > self.best_fitness:
            self.best_fitness = ga_instance.best_solution()[1]
            torch.save(model_weights_dict, f"model_{ga_instance.generations_completed}.pt")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                    prog='AI Project',
                    description='A project of unsupervised learning, for the AI class of UESPI-Floriano'
                    )
    parser.add_argument('-t', '--train', action='store_true')
    parser.add_argument('-gens', '--generations', type=int, default=1000)
    parser.add_argument('-pars', '--parents', type=int, default=5)

    parser.add_argument('-p', '--presentation', action='store_true')
    parser.add_argument('-s', '--sleep', type=float, default=0.005)

    parser.add_argument('-e', '--evaluate', action='store_true')
    parser.add_argument('-ei', '--eval_iters', type=int, default=10000)
    
    parser.add_argument('-t0m', '--team_0_module', type=str, default='random_ai')
    parser.add_argument('-t0c', '--team_0_class', type=str, default='RandomAI')
    parser.add_argument('-l0', '--load_0', type=str, default=None)
    parser.add_argument('-k0', '--key_0', type=str, default=None, help='Key for loading with dictionary.')
    
    parser.add_argument('-t1m', '--team_1_module', type=str, default='random_ai')
    parser.add_argument('-t1c', '--team_1_class', type=str, default='RandomAI')
    parser.add_argument('-l1', '--load_1', type=str, default=None)
    parser.add_argument('-k1', '--key_1', type=str, default=None, help='Key for loading with dictionary.')

    parser.add_argument('-mw', '--max_width', type=int, default=80)
    parser.add_argument('-mh', '--max_height', type=int, default=40)

    args = parser.parse_args()

    Map.MAX_WIDTH = args.max_width
    Map.MAX_HEIGHT = args.max_height

    class0 = getattr(importlib.import_module(f"ai.{args.team_0_module}", "ai"), args.team_0_class)
    model0: torch.nn.Module = class0(0)
    print(args)
    if not args.load_0 is None and os.path.isfile(args.load_0):
        state_dict = torch.load(args.load_0)
        if not args.key_0 is None: model0.load_state_dict(state_dict[args.key_0])
        else: model0.load_state_dict(state_dict)
    
    class1 = getattr(importlib.import_module(f"ai.{args.team_1_module}", "ai"), args.team_1_class)
    model1: torch.nn.Module = class1(1)
    if not args.load_1 is None and os.path.isfile(args.load_1):
        state_dict = torch.load(args.load_1)
        if not args.key_1 is None: model1.load_state_dict(state_dict[args.key_1])
        else: model1.load_state_dict(state_dict)
    
    if args.train: 
        t = Trainer(model0, model1)
        t.train(args.generations, args.parents)
    elif args.presentation:
        m = Match(3, model0, model1, presentation=args.presentation, sleep_time=args.sleep) 
        m.play()
    elif args.evaluate:
        t = Tester(model0, model1, iters=args.eval_iters)
        t.test()