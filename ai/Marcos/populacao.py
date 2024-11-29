# @title Populacao


from ai.Marcos.individuos import Individuo


class Populacao:
    def __init__(self) -> None:
        """
        Objetivo: Inicializar uma nova população.
        Funcionalidade: Cria uma lista vazia para armazenar os indivíduos e inicializa a quantidade de indivíduos como 0.
        """
        self._individuos = []
        self._quantidadeIndividuos = 0

    def getQuantidadeIndividuos(self) -> int:
        """
        Objetivo: Obter a quantidade de indivíduos na população.
        Funcionalidade: Retorna o número de indivíduos atualmente na população.
        """
        return self._quantidadeIndividuos

    def getQuantidadeGenesIndividuo(self, individuo: int) -> int:
        """
        Objetivo: Obter a quantidade de genes de **um** indivíduo específico.
        Funcionalidade: Retorna a quantidade de genes do indivíduo no índice especificado.
        """
        return self._individuos[individuo]._gene.getQuantidadeGenes()

    def setGenesIndividuo(self, individuo: int, indice: int, gene: float) -> None:
        """
        Objetivo: Definir o valor de um gene específico de um indivíduo.
        Funcionalidade: Atribui o valor fornecido ao gene no índice especificado do indivíduo especificado.
        """
        self._individuos[individuo].setGene(indice, gene)

    def getGenesIndividuo(self, individuo: int, indice: int) -> float:
        """
        Objetivo: Obter o valor de um gene específico de um indivíduo.
        Funcionalidade: Retorna o valor do gene no índice especificado do indivíduo especificado.
        """
        return self._individuos[individuo].getGene(indice)

    def setAptidaoIndividuo(self, individuo: int, aptidao: float) -> None:
        """
        Objetivo: Definir a aptidão de um indivíduo.
        Funcionalidade: Atribui o valor fornecido à aptidão do indivíduo especificado.
        """
        self._individuos[individuo].setAptidao(aptidao)

    def getAptidaoIndividuo(self, individuo: int) -> float:
        """
        Objetivo: Obter a aptidão de um indivíduo.
        Funcionalidade: Retorna o valor da aptidão do indivíduo especificado.
        """
        return self._individuos[individuo].getAptidao()

    def ordenarIndividuosCrescente(self) -> None:
        """
        Objetivo: Ordenar os indivíduos por aptidão em ordem crescente.
        Funcionalidade: Ordena a lista de indivíduos com base na aptidão de cada um, em ordem crescente.
        """
        self._individuos.sort(key=lambda x: x.getAptidao() if x.getAptidao() is not None else float('-inf'))

    def ordenarIndividuosDecrescente(self) -> None:
        """
        Objetivo: Ordenar os indivíduos por aptidão em ordem decrescente.
        Funcionalidade: Ordena a lista de indivíduos com base na aptidão de cada um, em ordem decrescente.
        """
        self._individuos.sort(key=lambda x: x.getAptidao(), reverse=True)

    def inserirIndividuo(self, individuo: 'Individuo') -> None:
        """
        Objetivo: Inserir um novo indivíduo na população.
        Funcionalidade: Adiciona o indivíduo fornecido à lista de indivíduos e incrementa a quantidade de indivíduos.
        """
        self._individuos.append(individuo)
        self._quantidadeIndividuos += 1

    def removerIndividuo(self, individuo: 'Individuo') -> None:
        """
        Objetivo: Remover um indivíduo da população.
        Funcionalidade: Remove o indivíduo fornecido da lista de indivíduos e decrementa a quantidade de indivíduos.
        """
        self._individuos.remove(individuo)
        self._quantidadeIndividuos -= 1

    def getIndiceIndividuoMenorAptidao(self) -> int:
        """
        Objetivo: Obter o índice do indivíduo com a menor aptidão.
        Funcionalidade: Retorna o índice do indivíduo com a menor aptidão na população.
        """
        return self._individuos.index(min(self._individuos, key=lambda x: x.getAptidao()))

    def getIndiceIndividuoMaiorAptidao(self) -> int:
        """
        Objetivo: Obter o índice do indivíduo com a maior aptidão.
        Funcionalidade: Retorna o índice do indivíduo com a maior aptidão na população.
        """
        return self._individuos.index(max(self._individuos, key=lambda x: x.getAptidao()))

    def getCloneIndividuo(self, individuo: int) -> 'Individuo':
        """
        Objetivo: Obter um clone de um indivíduo específico.
        Funcionalidade: Retorna um clone do indivíduo no índice especificado.
        """
        return self._individuos[individuo].getClone()

    def getClone(self) -> 'Populacao':
        """
        Objetivo: Criar um clone da população atual.
        Funcionalidade: Cria uma nova instância de `Populacao`, clona todos os indivíduos da população atual e os insere na nova população, e retorna a nova população.
        """
        populacao = Populacao()
        for individuo in self._individuos:
            populacao.inserirIndividuo(individuo.getClone())
        return populacao