from searchAlgorithm import SearchAlgorithm
from queue import Queue
from node import Node


class BreadthFirstSearch(SearchAlgorithm):
    def __init__(self, environment):
        super().__init__(environment)
        self.frontier = Queue()

    def search(self):
        startNode = Node(location=self.environment.start, parent=None, direction="", cost = 0)
        self.frontier.put(startNode)
        self.numberOfNodes += 1
        self.visited.append(startNode.location) # mark the start node as visited
        success = False
        while not self.frontier.empty(): # stop the loop when the frontier is empty
            node = self.frontier.get()
            if self.environment.isGoal(node.location):
                success = True
                break # stop the program when a solution is found
            yield {"finish": False, "success": False, "visited": self.visited, "frontier": [node.location for node in self.frontier.queue]}
            self.expand(node) # explore the children node

        if success:
            yield {"finish": True, "success": True, "direction":self.getDirection(node), "path": self.getPath(node), "numberOfNodes": self.numberOfNodes}
            return
        else:
            yield {"finish": True, "success": False, "message": "No solution found"}
            return

    def expand(self, node):
        successors = self.environment.getSuccessors(node.location) # get the successors from the node location
        for direction, location in successors.items():
            if location not in self.visited:# skip the node if it is already visited
                newNode = Node(location=location, parent=node, direction=direction, cost = node.cost + 1)
                self.frontier.put(newNode)
                self.numberOfNodes += 1
                self.visited.append(location)



