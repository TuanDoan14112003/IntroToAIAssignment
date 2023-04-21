from informedSearch import InformedSearch
from node import Node
import bisect


class AStarSearch(InformedSearch):
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
        startNode = Node(location=self.environment.start, parent=None, direction="", cost=0)
        self.frontier.append(startNode)
        self.numberOfNodes += 1
        success = False
        while self.frontier:
            node = self.frontier.pop(0)
            self.visited.append(node) # mark the node as visited
            if self.environment.isGoal(node.location):
                success = True
                break # stop the loop when a solution is found
            yield {"finish": False, "success": False, "visited": [node.location for node in self.visited],
                   "frontier": [node.location for node in self.frontier]}
            self.expand(node)

        if success:
            yield {"finish": True, "success": True, "path": self.getPath(node), "direction": self.getDirection(node),
                   "numberOfNodes": self.numberOfNodes}
            return
        else:
            yield {"finish": True, "success": False, "message": "No solution found"}
            return

    def expand(self, node):
        successors = self.environment.getSuccessors(node.location)
        for direction, location in successors.items():
            successor = Node(location=location, parent=node, direction=direction, cost=node.cost + 1)
            skip = False

            # skip the node if there already exists a node in the visited list with a lower heuristic value
            for visitedNode in self.visited:
                if visitedNode.location == successor.location and self.getHeuristicValue(
                        visitedNode) <= self.getHeuristicValue(successor):
                    skip = True
                    break

            # skip the node if there already exists a node in the frontier list with a lower heuristic value
            for frontierNode in self.frontier:
                if frontierNode.location == successor.location and self.getHeuristicValue(
                        frontierNode) <= self.getHeuristicValue(successor):
                    skip = True
                    break

            if skip:
                continue

            # insert the successor into the frontier and sort the list based on the heuristic value
            bisect.insort_right(a=self.frontier,
                                x=successor,
                                key=self.getHeuristicValue)
            self.numberOfNodes += 1

# test
if __name__ == "__main__":
    from environment import Environment
    from wall import Wall

    size = [5, 11]
    start = [0, 1]
    goal = [7, 0]
    wall1 = Wall(1, 0, 1, 5)
    wall2 = Wall(8, 0, 1, 2)
    wall3 = Wall(10, 0, 1, 1)
    wall4 = Wall(2, 3, 1, 2)
    wall5 = Wall(3, 4, 3, 1)
    wall6 = Wall(9, 3, 1, 1)
    wall7 = Wall(8, 4, 2, 1)
    env = Environment(5, 11, start, goals=[goal], walls=[wall1, wall2, wall3, wall4, wall5, wall6, wall7])
    bfs = AStarSearch(env)
    bfs.search()
