from abc import ABC, abstractmethod  # abstract base class


class SearchAlgorithm(ABC):
    """
    The abstract class for all search algorithms
    """
    def __init__(self, environment):
        self.environment = environment  # the environment and its configuration (initial location, goals, walls)
        self.visited = []  # visited nodes (column first and then row)

    @abstractmethod
    def search(self):
        """"
        This function will be implemented by the children classes
        """
        pass

    @abstractmethod
    def expand(self, node):
        """"
        This function will be implemented by the children classes
        """
        pass

    def getDirection(self, node):
        """
        Takes a node and return a sequence of moves to get to that node from the start node
        """
        if node is None:
            return ""
        else:
            parentPath = self.getDirection(node.parent)
            seperator = "; " if parentPath != "" else ""
            return parentPath + seperator + node.direction



    def getPath(self, node):
        if node is None:
            return []
        else:
            return self.getPath(node.parent) + [node.location]
