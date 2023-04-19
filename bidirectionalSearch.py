from searchAlgorithm import SearchAlgorithm
from queue import Queue
from node import Node


class BidirectionalSearch(SearchAlgorithm):
    def __init__(self, environment):
        super().__init__(environment)
        self.srcVisited = [[False for i in range(self.environment.column)] for j in range(self.environment.row)]
        self.desVisited = [[False for i in range(self.environment.column)] for j in range(self.environment.row)]
        self.srcParent = [[None for i in range(self.environment.column)] for j in range(self.environment.row)]
        self.desParent = [[None for i in range(self.environment.column)] for j in range(self.environment.row)]
        self.srcFrontier = Queue()
        self.desFrontier = Queue()
    def getIntersectingNode(self):
        for i in range(self.environment.row):
            for j in range(self.environment.column):
                if self.srcVisited[i][j] and self.desVisited[i][j]:
                    return [j, i]
        return -1

    def getVisited(self):
        visited = []
        for i in range(self.environment.row):
            for j in range(self.environment.column):
                if self.srcVisited[i][j] or self.desVisited[i][j]:
                    visited.append([j,i])
        return visited

    def search(self):
        startNode = Node(location=self.environment.start, parent=None, direction="", cost = 0)
        endNode = Node(location=self.environment.goals[0], parent=None, direction="", cost = 0)
        self.srcFrontier.put(startNode)
        self.desFrontier.put(endNode)
        self.srcVisited[startNode.location[1]][startNode.location[0]] = True
        self.desVisited[endNode.location[1]][endNode.location[0]] = True
        success = False
        while not self.srcFrontier.empty() and not self.desFrontier.empty():
            srcNode = self.srcFrontier.get()
            desNode = self.desFrontier.get()
            intersection = self.getIntersectingNode()
            if intersection != -1:
                success = True
                break
            yield {"finish": False, "success": False, "visited": self.getVisited(), "frontier": [node.location for node in self.srcFrontier.queue] + [node.location for node in self.desFrontier.queue]}

            self.expand(srcNode, "forward")
            self.expand(desNode, "backward")
        if success:
            yield {"finish": True,"success": True, "path" : self.getPath(intersection), "direction" : self.getDirection(intersection), "numberOfNodes":len(self.getPath(intersection)) -1 }
            return
        else:
            yield {"finish": True,"success": False, "message": "No solution"}
            return


    def getPathSource(self, location):
        if location is None:
            return []
        else:
            return self.getPathSource(self.srcParent[location[1]][location[0]]) + [location]

    def getPathDes(self, location):
        if location is None:
            return []
        else:
            return [location] + self.getPathDes(self.desParent[location[1]][location[0]])

    def getPath(self, intersection):
        return self.getPathSource(self.srcParent[intersection[1]][intersection[0]]) \
               + [intersection] \
               + self.getPathDes(self.desParent[intersection[1]][intersection[0]])

    def getDirection(self, intersection):
        path = self.getPath(intersection)
        direction = ""
        for i in range(len(path) - 1):
            location = path[i]
            nextLocation = path[i + 1]
            if location[0] == nextLocation[0] and location[1] == nextLocation[1] - 1:
                direction += "down; "
            elif location[0] == nextLocation[0] and location[1] == nextLocation[1] + 1:
                direction += "up; "
            elif location[1] == nextLocation[1] and location[0] == nextLocation[0] + 1:
                direction += "left; "
            elif location[1] == nextLocation[1] and location[0] == nextLocation[0] - 1:
                direction += "right; "
            else:
                raise Exception("Cannot calculate the direction to the next move")
        return direction

    def expand(self, node, direction):
        successors = self.environment.getSuccessors(node.location)
        if direction == "forward":
            for action, location in successors.items():
                if not self.srcVisited[location[1]][location[0]]:
                    self.srcFrontier.put(Node(location=location, parent=node, direction=action, cost = node.cost + 1))
                    self.srcVisited[location[1]][location[0]] = True
                    self.srcParent[location[1]][location[0]] = node.location
        elif direction == "backward":
            for action, location in successors.items():
                if not self.desVisited[location[1]][location[0]]:
                    self.desFrontier.put(Node(location=location, parent=node, direction=action, cost = node.cost + 1))
                    self.desVisited[location[1]][location[0]] = True
                    self.desParent[location[1]][location[0]] = node.location


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
    bfs = BidirectionalSearch(env)
    bfs.search()
