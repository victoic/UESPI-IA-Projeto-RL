# @title EstrategiaEvolutiva

import random

from ai.Marcos.individuos import Individuo
from ai.Marcos.populacao import Populacao
from ai.Marcos.redeneural import RedeNeural

class EstrategiaEvolutiva:

    def __init__(self, tamanhoPopulacao: int, quantidadeGenes: int, redeNeural: RedeNeural, problemaMinimizacao: bool = True) -> None:
        """
        Objetivo: Inicializar a estratégia evolutiva.
        Funcionalidade: Configura os parâmetros iniciais da estratégia evolutiva, incluindo o tamanho da população, quantidade de genes, rede neural, tipo de mutação, tipo de seleção, e inicializa as populações de progenitores e descendentes.
        """
        self._contadorGeracoes = 0
        self._tipoMutacao = "gaussiana"
        self._tipoSelecao = "torneio"
        self._problemaMinimizacao = problemaMinimizacao
        self._desvioPadraoMutacao = 0.1
        self._amplitudeMutacaoParcial = 0.1
        self._tamanhoPopulacao = tamanhoPopulacao
        self._quantidadeGenes = quantidadeGenes
        self._redeNeural = redeNeural
        self._populacaoProgenitores = Populacao()
        self._quantidadeProgenitores = tamanhoPopulacao // 2
        self._populacaoDescendente = Populacao()
        self._quantidadeDescendentes = tamanhoPopulacao
        self._inicializarPopulacao()

    def _inicializarPopulacao(self) -> None:
        """
        Objetivo: Inicializar a população de progenitores.
        Funcionalidade: Cria indivíduos e os insere na população de progenitores.
        """
        for _ in range(self._tamanhoPopulacao):
            individuo = Individuo(self._redeNeural, self._quantidadeGenes)
            self._populacaoProgenitores.inserirIndividuo(individuo)

    def setAptidaoIndividual(self, individuo: Individuo, aptidao: float) -> None:
        """
        Objetivo: Definir a aptidão de um indivíduo.
        Funcionalidade: Atribui o valor fornecido à aptidão do indivíduo especificado.
        """
        individuo.setAptidao(aptidao)

    def getQuantidadeDescendentes(self) -> int:
        """
        Objetivo: Obter a quantidade de descendentes.
        Funcionalidade: Retorna o número de descendentes na população.
        """
        return self._quantidadeDescendentes

    def getGenesDescendente(self, individuo: Individuo) -> float:
        """
        Objetivo: Obter os genes de um descendente.
        Funcionalidade: Retorna os genes do indivíduo especificado.
        """
        return individuo.getGene()

    def getQuantidadeGenesDescendentes(self) -> int:
        """
        Objetivo: Obter a quantidade de genes dos descendentes.
        Funcionalidade: Retorna o número de genes na população de descendentes.
        """
        return len(self._populacaoDescendente._individuos)

    def criarProximaGeracao(self) -> None:
        """
        Objetivo: Criar a próxima geração de indivíduos.
        Funcionalidade: Incrementa o contador de gerações, seleciona progenitores, realiza cruzamento, aplica mutação e une progenitores e descendentes.
        """
        self._contadorGeracoes += 1
        self._populacaoProgenitores = self.selecionarProgenitores(self._populacaoProgenitores)
        self._populacaoDescendente = self.cruzamento(self._populacaoProgenitores)
        self._populacaoDescendente = self.aplicarMutacao(self._populacaoDescendente)
        self._populacaoProgenitores = self.unirProgenitoresDescendentes(self._populacaoProgenitores, self._populacaoDescendente)

    def unirProgenitoresDescendentes(self, populacaoA: Populacao, populacaoB: Populacao) -> Populacao:
        """
        Objetivo: Unir progenitores e descendentes em uma nova população.
        Funcionalidade: Cria uma nova população contendo indivíduos de ambas as populações fornecidas.
        """
        novaPopulacao = Populacao()
        for individuo in populacaoA._individuos:
            novaPopulacao.inserirIndividuo(individuo)
        for individuo in populacaoB._individuos:
            novaPopulacao.inserirIndividuo(individuo)
        return novaPopulacao

    def selecionarProgenitores(self, populacao: Populacao) -> Populacao:
        """
        Objetivo: Selecionar progenitores para a próxima geração.
        Funcionalidade: Ordena a população por aptidão e seleciona os melhores indivíduos como progenitores.
        """
        novaPopulacao = Populacao()
        populacao.ordenarIndividuosCrescente() if self._problemaMinimizacao else populacao.ordenarIndividuosDecrescente()
        for i in range(self._quantidadeProgenitores):
            novaPopulacao.inserirIndividuo(populacao.getCloneIndividuo(i))
        return novaPopulacao

    def clonarProgenitores(self, populacao: Populacao) -> Populacao:
        """
        Objetivo: Clonar a população de progenitores.
        Funcionalidade: Retorna um clone da população de progenitores.
        """
        return populacao.getClone()

    def aplicarMutacao(self, populacao: Populacao) -> Populacao:
        """
        Objetivo: Aplicar mutação aos indivíduos da população.
        Funcionalidade: Aplica mutação gaussiana aos genes dos indivíduos com uma certa taxa de mutação.
        """
        for i in range(populacao.getQuantidadeIndividuos()):
            for j in range(populacao.getQuantidadeGenesIndividuo(i)):
                if random.random() < 0.1:  # Taxa de mutação
                    gene = populacao.getGenesIndividuo(i, j)
                    gene += random.gauss(0, self._desvioPadraoMutacao)
                    populacao.setGenesIndividuo(i, j, gene)
        return populacao

    def cruzamento(self, progenitores: Populacao) -> Populacao:
        """
        Objetivo: Realizar cruzamento entre progenitores para gerar descendentes.
        Funcionalidade: Realiza cruzamento entre pares de progenitores para criar novos indivíduos descendentes.
        """
        descendentes = Populacao()
        for i in range(0, progenitores.getQuantidadeIndividuos(), 2):
            pai1 = progenitores._individuos[i]
            pai2 = progenitores._individuos[i + 1] if i + 1 < progenitores.getQuantidadeIndividuos() else progenitores._individuos[0]
            filho1, filho2 = self._cruzarIndividuos(pai1, pai2)
            descendentes.inserirIndividuo(filho1)
            descendentes.inserirIndividuo(filho2)
        return descendentes

    def _cruzarIndividuos(self, pai1: Individuo, pai2: Individuo) -> (Individuo, Individuo): # type: ignore
        """
        Objetivo: Realizar cruzamento entre dois indivíduos.
        Funcionalidade: Cria dois novos indivíduos trocando genes entre os pais a partir de um ponto de corte.
        """
        filho1 = pai1.getClone()
        filho2 = pai2.getClone()

        if self._quantidadeGenes > 1:

            pontoCorte = random.randint(1, self._quantidadeGenes - 1)

        else:
            # Handle the case where _quantidadeGenes is too small
            # You might want to return the parents unchanged,
            # or implement a different crossover strategy for this case
            return pai1, pai2

        for i in range(pontoCorte, self._quantidadeGenes):
            genePai1 = pai1.getGene(i)
            genePai2 = pai2.getGene(i)
            filho1.setGene(i, genePai2)
            filho2.setGene(i, genePai1)

        return filho1, filho2

    def getMelhorIndividuo(self) -> Individuo:
        """
        Objetivo: Obter o melhor indivíduo da população.
        Funcionalidade: Retorna o indivíduo com a melhor aptidão na população de progenitores.
        """
        self._populacaoProgenitores.ordenarIndividuosCrescente() if self._problemaMinimizacao else self._populacaoProgenitores.ordenarIndividuosDecrescente()
        return self._populacaoProgenitores._individuos[0]

    def getContadorGeracoes(self) -> int:
        """
        Objetivo: Obter o número de gerações.
        Funcionalidade: Retorna o contador de gerações.
        """
        return self._contadorGeracoes

    def setDesvioPadraoMutacao(self, desvioPadrao: float) -> None:
        """
        Objetivo: Definir o desvio padrão da mutação.
        Funcionalidade: Atribui o valor fornecido ao desvio padrão da mutação.
        """
        self._desvioPadraoMutacao = desvioPadrao

    def setProblemaMinimizacao(self, problemaMinimizacao: bool) -> None:
        """
        Objetivo: Definir se o problema é de minimização.
        Funcionalidade: Atribui o valor fornecido ao atributo que indica se o problema é de minimização.
        """
        self._problemaMinimizacao = problemaMinimizacao