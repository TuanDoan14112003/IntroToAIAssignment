class Node:
    def __init__(self, location, parent, direction, cost=0):
        self.cost = cost
        self.location = location
        self.parent = parent
        self.direction = direction

    def __str__(self):
        return str(self.location)
