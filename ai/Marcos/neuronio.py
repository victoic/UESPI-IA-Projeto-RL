# @title Neuronio
import math
import random

class Neuronio:
    def __init__(self, quantidadeConexoes: int, codigoFuncaoAtivacao: int):

        self._pesos = [random.uniform(-1, 1) for _ in range(quantidadeConexoes)]
        self._valorVies = random.uniform(-1, 1)
        self._entrada = []  # Lista de entradas recebidas pelo neurônio
        self._quantidadeConexoes = quantidadeConexoes  # Quantidade de neurônios conectados à entrada
        self._saida = None  # Saída do neurônio após a função de ativação

        self._codigoFuncaoAtivacao = codigoFuncaoAtivacao  # Indica qual função será usada -relu ou -sigmoid [1 - relu; 2 sigmoid]

    def relu(self, x: float) -> float:
        return max(0, x)  # Retorna o valor máximo entre 0 e X dentro da rede

    def sigmoid(self, x: float) -> float:
        return 1 / (1 + math.exp(-x))  # Retorna um valor entre 0 e 1

    def setEntrada(self, entrada: list[float]) -> None:
        self._entrada = entrada
        """
        Descrição: Recebe as entradas que o neurônio deve processar
        Funcionalidade: Recebe uma lista de float e armazena em _entrada
        """

    def realizarFeedForward(self) -> None:
        """
        Descrição: Calcula o valor de saída do neurônio
        Funcionalidade:
            - Calcula a soma ponderada das entradas multiplicadas pelos pesos
            - Adiciona o valor viés à soma
            - Aplica a função de ativação
        """
        soma = 0

        # print("Isto deve aparecer somenete 2 vezes")
        # print (self._quantidadeConexoes)
        # print (self._entrada)
        # print (self._pesos)

        for i in range(self._quantidadeConexoes):
            soma += self._pesos[i] * self._entrada[i]
        soma += self._valorVies

        if self._codigoFuncaoAtivacao == 1:
            self._saida = self.relu(soma)  # Aplica a função e salva em _saida
        elif self._codigoFuncaoAtivacao == 2:
            self._saida = self.sigmoid(soma)
        else:
            self._saida = self.relu(soma)  # Default

    def getSaida(self) -> float:
        return self._saida  # Retorna o valor da saída do neurônio

    def setPesos(self, pesos: list[float]) -> None:
        """
        Descrição: Define os pesos do neurônio
        Funcionalidade: Recebe uma lista de pesos que definem quais são os pesos do neurônio
        """
        self._pesos = pesos

    def getPesos(self) -> list[float]:
        return self._pesos  # Retorna os pesos do neurônio

    def getQuantidadeConexoes(self) -> int:
        return self._quantidadeConexoes  # Retorna a quantidade de entradas

    def setValorVies(self, valorVies: float) -> None:
        """
        Descrição: Define o valor da bias/viés do neurônio
        Funcionalidade: Permite ajustar o viés conforme necessário
        """
        self._valorVies = valorVies

    def getValorVies(self) -> float:
        return self._valorVies  # Retorna o valor viés