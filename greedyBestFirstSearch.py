from informedSearch import InformedSearch
from node import Node
import bisect


class GreedyBestFirstSearch(InformedSearch):
    def __init__(self, environment):
        super().__init__(environment)
        self.frontier = []

    def getHeuristicValue(self, node):
        """"
        f(n) = h(n) = Manhattan distance
        """
        location = node.location
        values = [abs(location[0] - goal[0]) + abs(location[1] - goal[1]) for goal in self.environment.goals] # Manhattan distance
        return min(values)

    def search(self):
        startNode = Node(location=self.environment.start, parent=None, direction="", cost=0)
        self.frontier.append(startNode)
        self.numberOfNodes += 1
        self.visited.append(startNode.location) # mark the start node as visited
        success = False
        while self.frontier:
            node = self.frontier.pop(0)
            if self.environment.isGoal(node.location):
                success = True
                break # stop the program when a solution is found
            yield {"finish": False, "success": False, "visited": self.visited, "frontier": [node.location for node in self.frontier]}

            self.expand(node) # explore children nodes

        if success:
            yield {"finish": True,"success": True, "path": self.getPath(node), "direction" : self.getDirection(node), "numberOfNodes": self.numberOfNodes}
            return
        else:
            yield {"finish": True,"success": False, "message": "No solution found"}
            return

    def expand(self, node):
        successors = self.environment.getSuccessors(node.location) # get its neighbour nodes
        for direction, location in successors.items():
            if location not in self.visited: # skip the successor if it is visited
                self.visited.append(location)
                newNode = Node(parent=node, location=location, direction=direction, cost=node.cost + 1)
                bisect.insort_right(a=self.frontier, x=newNode,
                                    key=self.getHeuristicValue) # insert the successor into the frontier and sort the list based on the heuristic value
                self.numberOfNodes += 1




