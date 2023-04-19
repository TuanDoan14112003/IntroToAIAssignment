from searchAlgorithm import SearchAlgorithm
from abc import abstractmethod


class InformedSearch(SearchAlgorithm):
    @abstractmethod
    def getHeuristicValue(self, node):
        pass
