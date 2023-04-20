from abc import ABC, abstractmethod  # abstract base class


class SearchAlgorithm(ABC):
    def __init__(self, environment):
        self.environment = environment  # the environment and its configuration (initial location, goals, walls)
        self.visited = []  # visited nodes (column first and then row)

    @abstractmethod
    def search(self):
        pass

    @abstractmethod
    def expand(self, node):
        pass

    def getDirection(self, node):
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
