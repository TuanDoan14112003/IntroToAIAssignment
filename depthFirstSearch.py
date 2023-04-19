from searchAlgorithm import SearchAlgorithm
from node import Node


class DepthFirstSearch(SearchAlgorithm):
    def __init__(self, environment):
        super().__init__(environment)
        self.frontier = []

    def search(self):
        startNode = Node(location=self.environment.start, parent=None, direction="", cost=0)
        self.frontier.append(startNode)
        success = False
        while self.frontier:
            node = self.frontier.pop()
            self.visited.append(node.location)
            if self.environment.isGoal(node.location):
                success = True
                break
            yield {"finish": False, "success": False, "visited": self.visited, "frontier": [node.location for node in self.frontier]}
            self.expand(node)

        if success:
            yield {"finish": True, "success": True, "direction":self.getDirection(node), "path": self.getPath(node), "numberOfNodes": node.cost}
            return
        else:
            yield {"finish": True,"success": False, "message": "No solution"}
            return

    def expand(self, node):
        successors = self.environment.getSuccessors(node.location)
        for direction, location in reversed(successors.items()):
            if location not in self.visited:
                newNode = Node(location=location, parent=node, direction=direction, cost =node.cost + 1)
                self.frontier.append(newNode)


if __name__ == "__main__":
    from environment import Environment
    from wall import Wall

    size = [5, 11]
    start = [0, 1]
    goal = [10, 3]
    wall1 = Wall(2, 0, 2, 2)
    wall2 = Wall(8, 0, 1, 2)
    wall3 = Wall(10, 0, 1, 1)
    wall4 = Wall(2, 3, 1, 2)
    wall5 = Wall(3, 4, 3, 1)
    wall6 = Wall(9, 3, 1, 1)
    wall7 = Wall(8, 4, 2, 1)
    env = Environment(5, 11, start, goals=[goal], walls=[wall1, wall2, wall3, wall4, wall5, wall6, wall7])
    bfs = DepthFirstSearch(env)
    bfs.search()
