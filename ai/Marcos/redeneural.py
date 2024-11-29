# @title RedeNeural


import torch
from ai.Marcos.camada import Camadas


class RedeNeural:
    def __init__(self):
        self._camadas = []  # Lista de camadas na rede neural
        self._quantidadeNeuroniosCamadasIntermediarias = []  # Array de inteiros
        self._quantidadeNeuroniosCamadaSaida = None  # Inteiro
        self._quantidadeCamadasIntermediarias = None  # Inteiro
        self._quantidadeCamadas = 0  # Inteiro

        self.fc1 = torch.nn.Linear(9, 18)
        self.fc2 = torch.nn.Linear(18, 9)


    def state_dict(self):
        """
        Retorna o dicionário de estado do modelo RedeNeural.
        """
        # Crie um dicionário contendo os parâmetros do modelo
        state = {
            'fc1.weight': self.fc1.weight,
            'fc1.bias': self.fc1.bias,
            'fc2.weight': self.fc2.weight,
            'fc2.bias': self.fc2.bias,
            # Adicione outros parâmetros aqui se sua rede tiver mais camadas
        }
        return state


    def load_state_dict(self, state_dict):
        """
        Carrega o dicionário de estado no modelo RedeNeural.
        """
        # Carregue os parâmetros do dicionário de estado
        self.fc1.weight = state_dict['fc1.weight']
        self.fc1.bias = state_dict['fc1.bias']
        self.fc2.weight = state_dict['fc2.weight']
        self.fc2.bias = state_dict['fc2.bias']
        # Carregue outros parâmetros aqui se sua rede tiver mais camadas

    def adicionarCamada(self, camada: Camadas) -> None:
        """Adiciona uma camada à rede neural"""
        self._camadas.append(camada)
        self._quantidadeCamadas += 1

    def getQuantidadeCamadas(self) -> int:
        return self._quantidadeCamadas

    def getQuantidadeNeuroniosCamadas(self) -> int:
        return sum(camada.getQuantidadeNeuronios() for camada in self._camadas)

    def setPesos(self, pesos: list[float]) -> None:
        for camada in self._camadas:
            camada.setPesos(pesos)

    def getPesos(self) -> list[float]:
        pesos = []
        for camada in self._camadas:
            pesos.extend(camada.getPesos())
        return pesos

    def getQuantidadePesos(self) -> int:
        return sum(camada.getQuantidadePesos() for camada in self._camadas)

    def setViesses(self, viesses: list[float]) -> None:
        for camada in self._camadas:
            camada.setValorViesses(viesses)

    def getViesses(self) -> list[float]:
        viesses = []
        for camada in self._camadas:
            viesses.extend(camada.getValorViesses())
        return viesses

    def getQuantidadeViesses(self) -> int:
        return sum(len(camada.getValorViesses()) for camada in self._camadas)

    def setEntrada(self, entrada: list[float]) -> None:
        if self._camadas:
            self._camadas[0].setEntrada(entrada)

    def realizarFeedForward(self) -> None:
        for i, camada in enumerate(self._camadas):
            camada.realizarFeedForward()
            if i < len(self._camadas) - 1:
                self._camadas[i + 1].setEntrada(camada.getSaidas())

    def getSaida(self) -> list[float]:
        if self._camadas:
            return self._camadas[-1].getSaidas()
        return []

    def setEntradaNeuronioCamada(self, camada_idx: int, neuronio_idx: int, entrada: list[float]) -> None:
        self._camadas[camada_idx]._neuronios[neuronio_idx].setEntrada(entrada)

    def getQuantidadeConexoesNeuroniosCamada(self, camada_idx: int, neuronio_idx: int) -> int:
        return self._camadas[camada_idx].getQuantidadeConexoesNeuronios(neuronio_idx)

    def getPesoNeuronioCamada(self, camada_idx: int, neuronio_idx: int, peso_idx: int) -> float:
        return self._camadas[camada_idx].getPesosNeuronio(neuronio_idx)[peso_idx]

    def getSaidaNeuronioCamada(self, camada_idx: int, neuronio_idx: int) -> float:
        return self._camadas[camada_idx]._neuronios[neuronio_idx].getSaida()

    def salvaEmArquivo(self, caminho: str) -> None:
        pass