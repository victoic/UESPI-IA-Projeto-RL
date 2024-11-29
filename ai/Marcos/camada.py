# @title Camadas


from ai.Marcos.neuronio import Neuronio


class Camadas:
    def __init__(self):
        self._neuronios = []  # Armazena os objetos da classe Neuronio, que representam os neurônios da camada
        self._quantidadeNeuronios = 0  # Armazena o número total de neurônios nesta camada

    def adicionarNeuronio(self, neuronio: Neuronio) -> None:
        """Adiciona um neurônio à camada"""
        self._neuronios.append(neuronio)
        self._quantidadeNeuronios += 1

    def getQuantidadeNeuronios(self) -> int:
        """Retorna a quantidade de neurônios que a camada possui"""
        return self._quantidadeNeuronios

    def getPesos(self) -> list[float]:
        """
        Coleta todos os pesos desta camada
        Funcionalidade: Itera sobre todos os neurônios chamando o getPesos() e adicionando-os à lista pesos
        """
        pesos = []
        for neuronio in self._neuronios:
            pesos.extend(neuronio.getPesos())
        return pesos

    def setPesos(self, pesos: list[float]) -> None:
        """
        Define os pesos de todos os neurônios desta camada
        Funcionalidade: Para cada neurônio na camada, chama o setPesos passando a lista de pesos
        """
        for neuronio in self._neuronios:
            neuronio.setPesos(pesos)

    def getQuantidadePesos(self) -> int:
        """
        Retorna a soma total de todos os pesos dos neurônios desta camada
        Funcionalidade: Itera sobre todos os neurônios e soma a quantidade de pesos de cada um
        """
        quantidadePesos = 0
        for neuronio in self._neuronios:
            quantidadePesos += neuronio.getQuantidadeConexoes()
        return quantidadePesos

    def setValorViesses(self, viesses: list[float]) -> None:
        """
        Define o valor do viés dentro de cada neurônio
        Funcionalidade: Itera por todos os neurônios e define seu valor de viés usando a lista de vieses
        """
        for i, neuronio in enumerate(self._neuronios):
            if i < len(viesses):
                neuronio.setValorVies(viesses[i])

    def getValorViesses(self) -> list[float]:
        """
        Coleta todos os valores de viés desta camada
        Funcionalidade: Itera sobre todos os neurônios chamando o getValorVies de cada neurônio e adiciona os valores de viés à lista viesses
        """
        viesses = []
        for neuronio in self._neuronios:
            viesses.append(neuronio.getValorVies())
        return viesses

    def setEntrada(self, entrada: list[float]) -> None:
        """Define a entrada para todos os neurônios da camada"""
        for neuronio in self._neuronios:
            neuronio.setEntrada(entrada)

    def realizarFeedForward(self) -> None:
        """Realiza o processo de feedforward para todos os neurônios da camada"""
        for neuronio in self._neuronios:
            neuronio.realizarFeedForward()

    def getSaidas(self) -> list[float]:
        """Retorna as saídas de todos os neurônios da camada"""
        saidas = []
        for neuronio in self._neuronios:
            saidas.append(neuronio.getSaida())
        return saidas

    def getPesosNeuronio(self, indice: int) -> list[float]:
        """Retorna os pesos de um neurônio específico"""
        if 0 <= indice < self._quantidadeNeuronios:
            return self._neuronios[indice].getPesos()
        return []

    def getQuantidadeConexoesNeuronios(self, indice: int) -> int:
        """Retorna a quantidade de conexões de um neurônio específico"""
        if 0 <= indice < self._quantidadeNeuronios:
            return self._neuronios[indice].getQuantidadeConexoes()
        return 0

    def getViessesNeuronio(self, indice: int) -> float:
        """Retorna o valor de viés de um neurônio específico"""
        if 0 <= indice < self._quantidadeNeuronios:
            return self._neuronios[indice].getValorVies()
        return 0.0