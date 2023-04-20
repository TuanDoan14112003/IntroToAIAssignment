from searchAlgorithm import SearchAlgorithm
from abc import abstractmethod


class InformedSearch(SearchAlgorithm):
    """The abstract class for the informed search methods"""
    @abstractmethod
    def getHeuristicValue(self, node):
        pass
