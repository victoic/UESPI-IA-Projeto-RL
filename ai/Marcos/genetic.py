from entities import Match
import numpy as np
import pygad.torchga, torch

from entities.agent import Agent
from ai.ai import AI
from ai.Marcos.camada import Camadas
from ai.Marcos.estrategia import EstrategiaEvolutiva
from ai.Marcos.neuronio import Neuronio
from ai.Marcos.redeneural import RedeNeural

class Genetic(AI):
    def __init__(self, team: int) -> None:
        super(Genetic, self).__init__(team)
        self.rede_neural = RedeNeural()
        self.fitness_history = []

        camada_entrada = Camadas()
        for _ in range(9):
            neuronio = Neuronio(9, 1)  # 3 conexões, ReLU
            camada_entrada.adicionarNeuronio(neuronio)
        self.rede_neural.adicionarCamada(camada_entrada)


        camada_oculta = Camadas()
        for _ in range(18):
            neuronio = Neuronio(9, 2)
            camada_oculta.adicionarNeuronio(neuronio)
        self.rede_neural.adicionarCamada(camada_oculta)


        camada_saida = Camadas()
        for _ in range(9):
            neuronio = Neuronio(18, 2)
            camada_saida.adicionarNeuronio(neuronio)
        self.rede_neural.adicionarCamada(camada_saida)

        self.estrategia = None # Será inicializada durante o treinamento

        self.vidas_dos_agentes = {} # Vou usar isso pra salvar a vida dos agentes

    def get_action(self, agent, view: dict):

        """
        Processa a visão do agente e decide a ação a ser tomada.

        Parameters:
            agent: O agente que está tomando a ação.
            view: Um dicionário representando a visão do agente.

        Returns:
            A ação a ser tomada pelo agente.
        """
        entradas = self.processar_visao(view)

        #print(f"Entradas/ Estado do jogo: {entradas}")

        self.rede_neural.setEntrada(entradas)
        self.rede_neural.realizarFeedForward()
        saida = self.rede_neural.getSaida()
        acao = self.decidir_acao_com_base_na_saida(saida)
        # print(f"Ação do agente {agent.ID}: {acao}")
        # print(f"Agente {agent.ID} (Vida: {agent.life}) - Ação: {acao}")

        return 0 if acao is None else acao

    def turn_reward(self, team: int, ID: int, previous_pos: tuple, action: int, list_agents: list['Agent']) -> None:
        """
        Calcula a aptidao do agente com base na recompensa obtida.

        Parameters:
            team: O time do agente.
            ID: O ID do agente.
            previous_pos: A posição anterior do agente.
            action: A ação executada pelo agente.
        """
        agent = None

        for agent_obj in list_agents:
            if agent_obj.ID == ID:
                agent = agent_obj
                break

        if not Match.game_over:

            # print("\n")
            # print("LOGCAT --- Aqui estou verificando os dados que chegam em turn_reward")

            self.vidas_dos_agentes.update({agent.ID: agent.life for agent in list_agents})
            # Armazena o fitness na lista fitness_history
            if agent is not None and ID in self.vidas_dos_agentes: # Only proceed if agent was found
            # Calculate fitness if agent is in self.vidas_dos_agentes
                agent.fitness = self.calculate_fitness(ID, previous_pos, action, list_agents, self.vidas_dos_agentes.get(ID, 0))

                if agent.life <= 0 and ID in self.vidas_dos_agentes:
                    # Agent died, apply death penalty to fitness
                    agent.fitness -= 100
                    del self.vidas_dos_agentes[ID]
                else:
                    # Store or update current agent life
                    self.vidas_dos_agentes[ID] = agent.life

                self.fitness_history.append(agent.fitness)
                self.fitness_history = self.fitness_history[-10:]


            #     print(f"Vida dos agentes{agent.life}")
            # print("LOGCAT --- Fim da apresentacao")
            # print("\n")


        if Match.game_over:


            team_0_life = sum([self.vidas_dos_agentes.get(agent.ID, 0) for agent in list_agents if agent.team == 0])
            team_1_life = sum([self.vidas_dos_agentes.get(agent.ID, 0) for agent in list_agents if agent.team == 1])

            # print("\n")
            # print("###########################FLAG################################")

            # print(f"time0 {team_0_life}")
            # print(f"time1 {team_1_life}")
            # #for agent in list_agents:
            #    #print(f"Vida =  {self.vidas_dos_agentes[agent.ID]}: Agente = {agent.ID}")

            # print("LOGCAT ###########################FLAG################################")
            # print("\n")


            if team_0_life > 0 and team_1_life <= 0:
            # Time 0 venceu

                reward = 1 if team == 0 else -1  # Recompensa positiva para o time 0, negativa para o time 1
            elif team_1_life > 0 and team_0_life <= 0:
                # Time 1 venceu
                print("-------------------TIME 1 VENCEU-------------------")
                reward = 1 if team == 1 else -1  # Recompensa positiva para o time 1, negativa para o time 0
            else:
                # Empate
                print("@@@@@@@@@@@@@@@@@DEU FOI EMPATE@@@@@@@@@@@@@@@@@@@")
                reward = 0  # Recompensa neutra para ambos os times

            for agent in list_agents:

                if agent.team == team and agent.ID == ID:
                    # Implementação da lógica de recompensa
                    reward = 0
                    if action == 8:  # Ação de ataque
                        reward += 10  # Recompensa por atacar
                    # ... outras condições de recompensa ...
                    agent.fitness += reward  # Atualiza a aptidão do agente
                    break

            print(f"Agente {agent.ID} (Time {agent.team}) - Ação: {action} - Recompensa: {reward}")


            # Reset a flag game_over para a próxima partida
            Match.game_over = False


    def calculate_fitness(self, ID, previous_pos, action, list_agents, initial_life):
            # Verifique se o ID está dentro do intervalo válido
            if ID < 0 or ID >= len(list_agents):
                raise IndexError(f"ID {ID} está fora do intervalo válido da lista de agentes.")

            # Obter o agente específico da lista de agentes usando o ID
            agent = list_agents[ID]
            
            fitness = 0

            # Recompensa por vida restante
            fitness += agent.life * 10

            # Penalidade por dano recebido
            damage_taken = initial_life - agent.life
            fitness -= damage_taken

            # Penalidade por ações indesejadas (exemplo: mover para uma posição anterior)
            if agent.position == previous_pos:
                fitness -= 5

            # Recompensa por ações desejadas (exemplo: mover para uma nova posição)
            if agent.position != previous_pos:
                fitness += 5

            # Recompensa por ações específicas (exemplo: atacar, coletar itens, etc.)
            if action == 'attack':
                fitness += 10
            elif action == 'collect_item':
                fitness += 15

            # Certifique-se de que a aptidão não seja negativa
            if fitness < 0:
                fitness = 0

            return fitness



    def get_reward(self, agents: dict, *args):
        """
        Calcula a recompensa total com base no desempenho geral.

        Parameters:
            agents: Um dicionário de agentes no ambiente.

        Returns:
            A recompensa total.
        """

        if isinstance(agents, dict):
            agents = list(agents.values())

        team_0_life = sum(agent.life for agent in agents if agent.team == 0)
        team_1_life = sum(agent.life for agent in agents if agent.team == 1)

        #print(f"Aptidão do time 0: {team_0_life}")  # Imprima a aptidão total do time 0
        #print(f"Aptidão do time 1: {team_1_life}")  # Imprima a aptidão total do time 1

        # Calcula a diferença de vida entre os times
        diff_life = team_0_life - team_1_life

        # Retorna a diferença como recompensa
        return diff_life if diff_life < 0 else 0



    def getQuantidadePesos(self) -> int:
        """
        Retorna a quantidade total de pesos na rede neural.

        Returns:
            A quantidade total de pesos.
        """
        return self.rede_neural.getQuantidadePesos()

    def setPesos(self, pesos: list[float]) -> None:
        """
        Define os pesos da rede neural.

        Parameters:
            pesos: Uma lista de pesos.
        """
        self.rede_neural.setPesos(pesos)

    def state_dict(self):
        """
        Retorna o estado do modelo como um dicionário.

        Returns:
            O estado do modelo.
        """
        return self.rede_neural.state_dict()

    def load_state_dict(self, state_dict):
        """
        Carrega o estado do modelo a partir de um dicionário.

        Parameters:
            state_dict: O estado do modelo.
        """
        self.rede_neural.load_state_dict(state_dict)

    def processar_visao(self, view: dict) -> list[float]:
        """
        Processa a visão do agente e converte em uma lista de entradas para a rede neural.

        Parameters:
            view: Um dicionário representando a visão do agente.

        Returns:
            Uma lista de entradas para a rede neural.
        """
        # Implementação do processamento da visão
        entradas = []
        for key, value in view.items():
            entradas.extend(value)
        return entradas

    def decidir_acao_com_base_na_saida(self, saida: list[float]) -> int:
        """
        Decide a ação a ser tomada com base na saída da rede neural.

        Parameters:
            saida: A saída da rede neural.

        Returns:
            A ação a ser tomada.
        """

        #abordagem probabilística que leve em conta os valores de saída da rede neural.

        #print(f"Saída da rede neural: {saida}")
        # Calcula as probabilidades usando softmax
        probs = np.exp(saida) / np.sum(np.exp(saida))

        # Seleciona uma ação aleatoriamente com base nas probabilidades
        acao = np.random.choice(len(saida), p=probs)
        return acao

    def treinar(self, generations: int, population_size: int, other):
        """
        Treina a rede neural usando estratégias evolutivas.

        Parameters:
            generations: Número de gerações para o treinamento.
            population_size: Tamanho da população para as estratégias evolutivas.
        """
        self.other_ai = other
        quantidade_genes = self.getQuantidadePesos()
        self.estrategia = EstrategiaEvolutiva(population_size, quantidade_genes, self.rede_neural)
        cont = 0

        for generation in range(generations):

            self.vidas_dos_agentes.clear()

            for individuo in self.estrategia._populacaoProgenitores._individuos:
                # Defina os pesos do modelo com os genes do indivíduo


                self.setPesos(individuo.getGenes_individuo().getClone().getGenes_genes())

                # Avalie a aptidão do indivíduo jogando uma partida
                match = Match(3, self, other, presentation=False, sleep_time=0.01, print_log=False)
                match.play(callback=self.turn_callback)
                Agent.CUR_ID = 0

                # Calcule a aptidão (exemplo simples: soma das vidas restantes dos agentes)
                fitness = self.get_reward(match.map.list_agents, generation)
                self.estrategia.setAptidaoIndividual(individuo, fitness)

                for agent in match.map.list_agents:
                    if agent.ID in self.vidas_dos_agentes:
                        agent.life = self.vidas_dos_agentes[agent.ID]

            self.estrategia.criarProximaGeracao()
            melhor_individuo = self.estrategia.getMelhorIndividuo()
            print(f"Geração {cont + 1}: Melhor Aptidão = {melhor_individuo.getAptidao()}")
            cont = cont + 1

        melhor_individuo = self.estrategia.getMelhorIndividuo()
        self.setPesos(melhor_individuo.getGenes_individuo().getClone().getGenes_genes())
        torch.save(self.state_dict(), "model_state.pth")

    def turn_callback(self, team: int, ID: int, previous_pos: tuple, action: int, list_agents: list[Agent]):
         if team == 0:
            # Atualiza self.vidas_dos_agentes com os valores de vida atuais dos agentes
            self.turn_reward(team, ID, previous_pos, action, list_agents)
            #self.vidas_dos_agentes.update({agent.ID: agent.life for agent in list_agents})

    def save_model(self, file_path: str):
        """
        Salva o modelo em um arquivo.
        """
        state_dict = self.rede_neural.state_dict()
        torch.save(state_dict, file_path)
        print(f"Modelo salvo em {file_path}")

    def load_model(self, file_path: str):
        """
        Carrega o modelo de um arquivo.
        """
        state_dict = torch.load(file_path)
        self.rede_neural.load_state_dict(state_dict)
        print(f"Modelo carregado de {file_path}")
