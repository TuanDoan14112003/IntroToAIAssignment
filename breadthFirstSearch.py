from searchAlgorithm import SearchAlgorithm
from queue import Queue
from node import Node


# QUAN TRONG: LOCATION LA LIST, KHONG PHAI TUPLE, SUA FILE PARSER
class BreadthFirstSearch(SearchAlgorithm):
    def __init__(self, environment):
        super().__init__(environment)
        self.frontier = Queue()

    def search(self):
        startNode = Node(location=self.environment.start, parent=None, direction="", cost = 0)
        self.frontier.put(startNode)
        self.visited.append(startNode.location)
        success = False
        while not self.frontier.empty():
            node = self.frontier.get()
            if self.environment.isGoal(node.location):
                success = True
                break
            yield {"finish": False, "success": False, "visited": self.visited, "frontier": [node.location for node in self.frontier.queue]}
            self.expand(node)

        if success:
            yield {"finish": True, "success": True, "direction":self.getDirection(node), "path": self.getPath(node), "numberOfNodes": node.cost}
            return
        else:
            yield {"finish": True, "success": False, "message": "No solution found"}
            return

    def expand(self, node):
        successors = self.environment.getSuccessors(node.location)
        for direction, location in successors.items():
            if location not in self.visited:
                newNode = Node(location=location, parent=node, direction=direction, cost = node.cost + 1)
                self.frontier.put(newNode)
                self.visited.append(location)


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
    bfs = BreadthFirstSearch(env)
    bfs.search()
