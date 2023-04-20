from searchAlgorithm import SearchAlgorithm
from node import Node

class IterativeDeepeningAStarSearch(SearchAlgorithm):
    def __init__(self, environment):
        super().__init__(environment)
        self.frontier = []

    def getHeuristicValue(self, node):
        """
        f(n) = h(n) + g(n)
        """
        location = node.location
        values = [abs(location[0] - goal[0]) + abs(location[1] - goal[1]) for goal in self.environment.goals]
        return min(values) + node.cost

    def search(self):
        success = False
        threshold = None # the threshold number
        while True:
            node = None
            prunedNodes = []
            self.visited = []
            start = Node(location=self.environment.start,parent=None,direction="",cost=0)
            self.frontier.append(start)
            if threshold is None:
                threshold = self.getHeuristicValue(start) # initialize the threshold number to start's heuristic value
            while self.frontier:
                node = self.frontier.pop()
                self.visited.append(node)
                if self.environment.isGoal(node.location):
                    success = True
                    break # stop the program if a solution is found
                if self.getHeuristicValue(node) > threshold:
                    prunedNodes.append(node)
                    continue
                yield {"finish": False, "success": False, "visited": [node.location for node in self.visited],
                       "frontier": [node.location for node in self.frontier]}

                self.expand(node)
            if success:
                yield {"finish": True, "success": True,"path" : self.getPath(node),"direction" : self.getDirection(node), "numberOfNodes": node.cost}
                return
            elif not prunedNodes: # if both the frontier and pruned list are empty then there is no solution
                yield {"finish": True, "success": False, "message": "No solution found"}
                return
            else: # if the pruned list is not empty then update the threshold to the smallest value in pruned list
                threshold = self.getHeuristicValue(prunedNodes[0])
                for node in prunedNodes:
                    if self.getHeuristicValue(node) <= threshold:
                        threshold = self.getHeuristicValue(node)



    def expand(self,node):
        successors = self.environment.getSuccessors(node.location)
        for direction, location in reversed(successors.items()):
            successor = Node(location=location, parent=node, direction=direction, cost=node.cost + 1)

            skip = False

            for visitedNode in self.visited: # skip the node if there already exists a node in the visited list with a lower heuristic value
                if visitedNode.location == successor.location and self.getHeuristicValue(visitedNode) <= self.getHeuristicValue(successor):
                    skip = True
                    break

            for frontierNode in self.frontier: # skip the node if there already exists a node in the frontier list with a lower heuristic value
                if frontierNode.location == successor.location and self.getHeuristicValue(frontierNode) <= self.getHeuristicValue(successor):
                    skip = True
                    break

            if skip:
                continue

            self.frontier.append(Node(location=location, direction=direction, parent=node, cost=node.cost + 1))

if __name__ == "__main__":
    from environment import Environment
    from wall import Wall

    size = [5, 11]
    start = [0, 1]
    goal = [7, 0]
    wall1 = Wall(2, 0, 2, 2)
    wall2 = Wall(8, 0, 1, 2)
    wall3 = Wall(10, 0, 1, 1)
    wall4 = Wall(2, 3, 1, 2)
    wall5 = Wall(3, 4, 3, 1)
    wall6 = Wall(9, 3, 1, 1)
    wall7 = Wall(8, 4, 2, 1)
    env = Environment(5, 11, start, goals=[goal], walls=[wall1, wall2, wall3, wall4, wall5, wall6, wall7])
    bfs = IterativeDeepeningAStarSearch(env)
    bfs.search()


