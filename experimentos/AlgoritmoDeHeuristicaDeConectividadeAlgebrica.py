from abc import ABCMeta, abstractmethod

class AlgoritmoDeHeuristicaDeConectividadeAlgebrica:

    __metaclass__ = ABCMeta

    def executar_algoritmo(self, grafo):
        return self._executar(grafo)

    @abstractmethod
    def _executar(self, grafo):
        raise NotImplementedError()

    @abstractmethod
    def obter_nome_do_algoritmo(self):
        raise NotImplementedError()
