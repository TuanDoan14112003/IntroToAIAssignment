class Environment:
    def __init__(self, row=None, column=None, start=None, goals=None, walls=None):
        self.row = row
        self.column = column

        self.start = start
        self.goals = goals
        self.walls = walls

    def isGoal(self, location):
        return location in self.goals

    def isWall(self, location):
        result = False
        for wall in self.walls:
            if wall.x <= location[0] < wall.x + wall.width and wall.y <= location[1] < wall.y + wall.height:
                result = True
                break
        return result

    def getSuccessors(self, location):
        moves = {}
        up = [location[0], location[1] - 1]
        if up[1] >= 0 and not self.isWall(up):
            moves["up"] = up

        left = [location[0] - 1, location[1]]
        if left[0] >= 0 and not self.isWall(left):
            moves["left"] = left

        down = [location[0], location[1] + 1]
        if down[1] < self.row and not self.isWall(down):
            moves["down"] = down

        right = [location[0] + 1, location[1]]
        if right[0] < self.column and not self.isWall(right):
            moves["right"] = right

        return moves
