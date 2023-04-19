from environment import Environment
from wall import Wall
from breadthFirstSearch import BreadthFirstSearch
from depthFirstSearch import DepthFirstSearch
from greedyBestFirstSearch import GreedyBestFirstSearch
from aStarSearch import AStarSearch
from bidirectionalSearch import BidirectionalSearch
from depthFirstSearch import DepthFirstSearch
from IDASearch import  IterativeDeepeningAStarSearch


class Robot:
    @staticmethod
    def parseFile(filename):
        with open(filename, 'r') as file:
            mazeSize = file.readline().strip('][ \n').split(',')
            mazeSize = [int(i) for i in mazeSize]  # convert string to integer
            initialLocation = [int(i) for i in file.readline().strip('() \n').split(',')]
            goalStates = file.readline().strip().split(' | ')
            goalStates = [state.strip(') (').split(',') for state in goalStates]
            goalStates = [[int(x) for x in state] for state in goalStates]
            walls = []
            for line in file.readlines():
                if not line.isspace():
                    newWall = [int(i) for i in line.strip('() \n').split(',')]
                    walls.append(Wall(*newWall))

            environment = Environment(row = mazeSize[0],column=mazeSize[1],start=initialLocation,goals=goalStates,walls=walls)
            return environment

    def __init__(self, filename):
        self.environment = Robot.parseFile(filename)
        self.searchMethod = None

    def solve(self, method):
        if method == "DFS":
            self.searchMethod = DepthFirstSearch(self.environment)
        elif method == "BFS":
            self.searchMethod = BreadthFirstSearch(self.environment)
        elif method == "GBFS":
            self.searchMethod = GreedyBestFirstSearch(self.environment)
        elif method == "AS":
            self.searchMethod = AStarSearch(self.environment)
        elif method == "CUS1":
            self.searchMethod = BidirectionalSearch(self.environment)
        elif method == "CUS2":
            self.searchMethod = IterativeDeepeningAStarSearch(self.environment)
        else:
            raise "There is no such search"
        return self.searchMethod.search()

