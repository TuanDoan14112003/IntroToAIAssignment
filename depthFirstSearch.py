from searchAlgorithm import SearchAlgorithm
from node import Node


class DepthFirstSearch(SearchAlgorithm):
    def __init__(self, environment):
        super().__init__(environment)
        self.frontier = [] # a stack data structure

    def search(self):
        startNode = Node(location=self.environment.start, parent=None, direction="", cost=0)
        self.frontier.append(startNode)
        self.numberOfNodes += 1
        success = False
        while self.frontier:
            node = self.frontier.pop() # remove the top of the stack
            self.visited.append(node.location) # mark the node as visited
            if self.environment.isGoal(node.location):
                success = True
                break # stop the loop when a solution is found
            yield {"finish": False, "success": False, "visited": self.visited, "frontier": [node.location for node in self.frontier]}
            self.expand(node) # explore the children nodes

        if success:
            yield {"finish": True, "success": True, "direction":self.getDirection(node), "path": self.getPath(node), "numberOfNodes": self.numberOfNodes}
            return
        else:
            yield {"finish": True,"success": False, "message": "No solution found"}
            return

    def expand(self, node):
        successors = self.environment.getSuccessors(node.location) # explore the successor as visited
        for direction, location in reversed(successors.items()):
            if location not in self.visited: # skip the successor if it is already visited
                newNode = Node(location=location, parent=node, direction=direction, cost =node.cost + 1)
                self.frontier.append(newNode)
                self.numberOfNodes += 1

