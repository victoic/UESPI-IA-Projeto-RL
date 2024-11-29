# @title Genes
class Genes:
  def __init__(self, quantidadeGenes:int) -> None:
    self._gene = [0.0] * quantidadeGenes  # Inicializa a lista de genes com zeros
    self._quantidadeGene = quantidadeGenes

  def setGene(self, indice : int, gene : float) -> None:
    self._gene[indice] = gene

  def getGene(self, indice : int) -> float:
    return self._gene[indice]

  def getGenes_genes(self) -> list[float]:
    return self._gene

  def getQuantidadeGenes(self) -> int:
    return self._quantidadeGene

  def getClone(self) -> 'Genes':
        genes = Genes(self._quantidadeGene)
        genes._gene = self._gene.copy()
        return genes