from tkinter import *
from robot import Robot
from tkinter.filedialog import asksaveasfilename, askopenfilename
from environment import Environment
from wall import Wall


def tksleep(self, time: float) -> None:
    self.after(int(time * 1000), self.quit)
    self.mainloop()


Misc.tksleep = tksleep


class GUI(Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry(f"1280x640")
        self.configure(bg='white')
        self.mazeCanvas = None

        self.filename = None
        self.environment = None
        self.robot = None
        self.switchFrame(HomepageFrame)

        self.visited = []
        self.frontier = []
        self.path = []

    def switchFrame(self, Frame):
        self.unbind("<ButtonRelease-1>")
        Frame(self, bg="white", width=1280, height=150).place(x=0, y=0)

    def drawMaze(self):
        self.clearMaze()
        if self.environment:
            self.squareSize = 50  # calculate the good size here
            self.mazeCanvas = Canvas(self, bg='white', width=self.squareSize * self.environment.column + 1,
                                     height=self.squareSize * self.environment.row + 1,
                                     borderwidth=0, highlightthickness=0, name="maze")
            self.mazeCanvas.place(x=50, y=150)
            self.mazeCanvas.delete("all")
            lineX = 0
            lineY = 0
            for i in range(self.environment.row + 1):
                self.mazeCanvas.create_line(0, lineY, self.squareSize * self.environment.column, lineY, fill="black",
                                            width=1)
                lineY += self.squareSize
            for j in range(self.environment.column + 1):
                self.mazeCanvas.create_line(lineX, 0, lineX, self.squareSize * self.environment.row, fill="black",
                                            width=1)
                lineX += self.squareSize

            if self.frontier:
                for location in self.frontier:
                    x, y = location[0] * self.squareSize + 1, location[1] * self.squareSize + 1
                    self.mazeCanvas.create_rectangle(x, y, x + self.squareSize - 2, y + self.squareSize - 2,
                                                     fill="#ADD8E6")

            if self.visited:
                for location in self.visited:
                    x, y = location[0] * self.squareSize + 1, location[1] * self.squareSize + 1
                    self.mazeCanvas.create_rectangle(x, y, x + self.squareSize - 2, y + self.squareSize - 2,
                                                     fill="#241571")


            if self.path:
                for path in self.path:
                    x, y = path[0] * self.squareSize + 1, path[1] * self.squareSize + 1
                    self.mazeCanvas.create_rectangle(x, y, x + self.squareSize - 2, y + self.squareSize - 2,
                                                     fill="yellow")

            if self.environment.goals:
                for goal in self.environment.goals:
                    x, y = goal[0] * self.squareSize + 1, goal[1] * self.squareSize + 1
                    self.mazeCanvas.create_rectangle(x, y, x + self.squareSize - 2, y + self.squareSize - 2,
                                                     fill="green")
            if self.environment.walls:
                for wall in self.environment.walls:
                    x, y = wall.x * self.squareSize + 1, wall.y * self.squareSize + 1
                    self.mazeCanvas.create_rectangle(x, y, x + (self.squareSize * wall.width) - 2,
                                                     y + (self.squareSize * wall.height) - 2,
                                                     fill="black")
            if self.environment.start:
                x, y = self.environment.start[0] * self.squareSize + 1, self.environment.start[1] * self.squareSize + 1
                self.mazeCanvas.create_rectangle(x, y, x + self.squareSize - 2, y + self.squareSize - 2, fill="red")
            self.drawing = self.after(50, self.drawMaze)
        else:
            raise Exception("Haven't imported file")

    def clearMaze(self):
        if self.mazeCanvas:
            if self.drawing is not None:
                self.after_cancel(self.drawing)
                self.drawing = None
            self.mazeCanvas.delete("all")


class HomepageFrame(Frame):
    def __init__(self, controller, **kwargs):
        super().__init__(master=controller, **kwargs)
        self.controller = controller
        Label(controller, text="Search Algorithm Visualizer", fg='black', bg='white').place(x=0, y=0)
        Button(controller, text='Create Maze', command=self.createMaze, bg='white', fg='black',
               highlightbackground='white').place(x=0, y=40)

        Button(controller, text='Import Maze', command=self.importMaze, bg='white', fg='black',
               highlightbackground='white').place(x=150, y=40)

    def importMaze(self):
        self.controller.switchFrame(ImportFrame)

    def createMaze(self):
        self.controller.switchFrame(SelectMazeSizeFrame)


class ImportFrame(Frame):
    def __init__(self, controller, **kwargs):
        super().__init__(master=controller, **kwargs)
        self.controller = controller
        self.controller.filename = self.importEnvironment()
        self.controller.drawMaze()
        print(self.controller.environment)
        Label(self, text="Maze Imported", fg='black', bg='white').place(x=0, y=0)
        # Button(self, text='Edit', command=self.edit, bg='white', fg='black',
        #        highlightbackground='white').place(x = 40, y = 40)
        Button(self, text='Search', command=self.goSearchFrame, bg='white', fg='black',
               highlightbackground='white').place(x=100, y=40)

    def importEnvironment(self):
        filename = askopenfilename()
        try:
            self.controller.environment = Robot.parseFile(filename)
        except:
            raise Exception("Cannot import the file")
        return filename

    def goSearchFrame(self):
        self.controller.switchFrame(SearchFrame)


class SearchFrame(Frame):
    def __init__(self, controller, **kwargs):
        super().__init__(master=controller, **kwargs)
        self.controller = controller
        if not self.controller.filename is None and self.controller.environment is not None:
            Label(self, text="Search Visualizer", fg='black', bg='white').place(x=0, y=0)
            # Button(self, text='Homepage', command=self.go_homepage, bg='white', fg='black',
            #        highlightbackground='white').place(x=50, y=40)
            self.algorithm = StringVar()
            Radiobutton(controller,
                        text="Breadth-First Search",
                        variable=self.algorithm,
                        command=self.search,
                        value="BFS").place(x=40, y=80)

            Radiobutton(controller,
                        text="Depth-First Search",
                        variable=self.algorithm,
                        command=self.search,
                        value="DFS").place(x=200, y=80)
            Radiobutton(controller,
                        text="Greedy Best-First Search",
                        variable=self.algorithm,
                        command=self.search,
                        value="GBFS").place(x=360, y=80)
            Radiobutton(controller,
                        text="A* Search",
                        variable=self.algorithm,
                        command=self.search,
                        value="AS").place(x=560, y=80)
            Radiobutton(controller,
                        text="Bidirectional Search (Custom Uninformed Search)",
                        variable=self.algorithm,
                        command=self.search,
                        value="CUS1").place(x=660, y=80)
            Radiobutton(controller,
                        text="IDA Search (Custom Informed Search)",
                        variable=self.algorithm,
                        command=self.search,
                        value="CUS2").place(x=1000, y=80)
            self.controller.drawMaze()

    def search(self):
        self.controller.path = []
        self.controller.visited = []
        self.controller.frontier = []
        method = self.algorithm.get()
        self.controller.robot = Robot(self.controller.filename)
        generator = self.controller.robot.solve(method)
        for result in generator:
            if not result["finish"]:
                self.controller.visited = result["visited"]
                print(self.controller.visited)
                self.controller.frontier = result["frontier"]
            else:
                if result["success"]:
                    self.controller.path = result["path"]
            self.controller.tksleep(0.01)


class SelectMazeSizeFrame(Frame):
    def __init__(self, controller, **kwargs):
        super().__init__(master=controller, **kwargs)
        self.controller = controller
        self.rowVar = IntVar()
        self.columnVar = IntVar()
        self.controller.environment = Environment()
        Label(controller, text="Row", fg='black', bg='white', font=("calibre", 20)).place(x=0, y=20)
        Entry(controller, textvariable=self.rowVar, fg='black', insertbackground='black',
              bg='white').place(x=100, y=20)
        Label(controller, text="Column", fg='black', bg='white', font=("calibre", 20)).place(x=0, y=50)
        Entry(controller, textvariable=self.columnVar, fg='black', insertbackground='black',
              bg='white').place(x=100, y=50)
        Button(controller, text='Confirm Size', command=self.confirmSize, bg='white', fg='black',
               highlightbackground='white').place(x=0, y=100)

    def confirmSize(self):
        self.controller.environment.row = self.rowVar.get()
        self.controller.environment.column = self.columnVar.get()
        self.controller.drawMaze()
        self.controller.switchFrame(SelectStartPointFrame)


class SelectStartPointFrame(Frame):
    def __init__(self, controller, **kwargs):
        super().__init__(master=controller, **kwargs)
        self.controller = controller
        controller.bind("<ButtonRelease-1>", self.selectStartPoint)
        Label(controller, text="Select Initial Point", fg='black', bg='white').place(x=0, y=0)
        Button(controller, text='Confirm Start Point', command=self.confirmStartPoint, bg='white', fg='black',
               highlightbackground='white').place(x=0, y=40)

    def selectStartPoint(self, event):
        if str(event.widget) == ".maze":
            mouse_x, mouse_y = event.x, event.y
            row = mouse_y // self.controller.squareSize
            column = mouse_x // self.controller.squareSize
            self.controller.environment.start = [column, row]

    def confirmStartPoint(self):
        self.controller.switchFrame(SelectGoalsFrame)


class SelectGoalsFrame(Frame):
    def __init__(self, controller, **kwargs):
        super().__init__(master=controller, **kwargs)
        controller.bind("<ButtonRelease-1>", self.selectGoals)
        self.controller = controller
        self.controller.environment.goals = []
        Label(controller, text="Select Goals", fg='black', bg='white').place(x=0, y=0)
        Button(controller, text='Confirm Goals', command=self.confirmGoals, bg='white', fg='black',
               highlightbackground='white').place(x=0, y=40)

    def selectGoals(self, event):
        if str(event.widget) == ".maze":
            mouse_x, mouse_y = event.x, event.y
            row = mouse_y // self.controller.squareSize
            column = mouse_x // self.controller.squareSize
            if [column, row] in self.controller.environment.goals:
                self.controller.environment.goals.remove([column, row])
            elif [column, row] != self.controller.environment.start:
                self.controller.environment.goals.append([column, row])
            else:
                print("Point already occupied")

    def confirmGoals(self):
        self.controller.switchFrame(SelectWallFrame)


class SelectWallFrame(Frame):
    def __init__(self, controller, **kwargs):
        super().__init__(master=controller, **kwargs)
        controller.bind("<ButtonRelease-1>", self.selectWalls)
        self.controller = controller
        self.controller.environment.walls = []
        Label(controller, text="Select Walls", fg='black', bg='white').place(x=0, y=0)
        Button(controller, text='Save', command=self.confirmWalls, bg='white',
               fg='black',
               highlightbackground='white').place(x=0, y=40)

    def selectWalls(self, event):
        if str(event.widget) == ".maze":
            mouse_x, mouse_y = event.x, event.y
            row = mouse_y // self.controller.squareSize
            column = mouse_x // self.controller.squareSize
            newWall = Wall(column, row, 1, 1)
            if newWall in self.controller.environment.walls:
                self.controller.environment.walls.remove(newWall)
            elif [newWall.x, newWall.y] != self.controller.environment.start and [newWall.x,
                                                                                  newWall.y] not in self.controller.environment.goals:
                self.controller.environment.walls.append(newWall)
            else:
                print("Point already occupied")

    def confirmWalls(self):
        self.controller.switchFrame(ExportFrame)


class ExportFrame(Frame):
    def __init__(self, controller, **kwargs):
        super().__init__(master=controller, **kwargs)
        self.controller = controller
        try:
            self.export()
        except:
            raise Exception("Can't export maze")
        Label(controller,
              text="The maze has been successfully saved. Go to homepage to import the maze file and start searching",
              fg='black', bg='white').place(x=0, y=0)
        Button(controller, text='Homepage', command=self.returnHomepage, bg='white',
               fg='black',
               highlightbackground='white').place(x=0, y=40)

    def returnHomepage(self):
        self.controller.clearMaze()
        self.controller.switchFrame(HomepageFrame)

    def export(self):
        with open(asksaveasfilename(initialfile='maze.txt',
                                    defaultextension=".txt", filetypes=[("Text Documents", "*.txt")]), "w") as file:
            row = self.controller.environment.row
            column = self.controller.environment.column
            file.write(f"[{row},{column}]\n")
            start = self.controller.environment.start
            file.write(f"({start[0]},{start[1]})\n")
            goals = self.controller.environment.goals
            for index in range(len(goals)):
                goal = goals[index]
                file.write(f"({goal[0]},{goal[1]})")
                if index != len(goals) - 1:
                    file.write(" | ")
            file.write("\n")
            walls = self.controller.environment.walls
            for index in range(len(walls)):
                wall = walls[index]
                file.write(f"({wall.x},{wall.y},{wall.width},{wall.height})")
                if index != len(walls) - 1:
                    file.write("\n")


gui = GUI()
gui.mainloop()
