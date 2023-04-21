from tkinter import *
from robot import Robot
from tkinter.filedialog import asksaveasfilename, askopenfilename
from environment import Environment
from wall import Wall


def delay(self, time):
    """
    Delay program for a period of time (Source:https://stackoverflow.com/questions/10393886/tkinter-and-time-sleep)
    """
    self.after(int(time * 1000), self.quit)
    self.mainloop()


Misc.tksleep = delay


class GUI(Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry(f"1280x900")
        self.configure(bg='white')
        self.title("Search Algorithm Visualizer by Anh Tuan Doan")
        self.mazeCanvas = None
        self.font = ("calibre",15)
        self.filename = None
        self.environment = None
        self.robot = None
        self.switchFrame(HomepageFrame)

        self.visited = []
        self.frontier = []
        self.path = []

    def switchFrame(self, Frame):
        """
        Switch to another frame
        """
        self.unbind("<ButtonRelease-1>") # unbind the button release event
        Frame(self, bg="white", width=1280, height=200).place(x=0, y=0)

    def drawMaze(self):
        """
        Draw the maze configuration
        """
        self.clearMaze()

        if self.environment:
            self.squareSize = int(min(1280//self.environment.column,900//self.environment.row) / 2)  # calculate the square size according the row and column
            self.mazeCanvas = Canvas(self, bg='white', width=self.squareSize * self.environment.column + 1,
                                     height=self.squareSize * self.environment.row + 1,
                                     borderwidth=0, highlightthickness=0, name="maze")
            self.mazeCanvas.place(x=40, y=200)
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
        """
        Clear the maze
        """
        if self.mazeCanvas:
            if self.drawing is not None:
                self.after_cancel(self.drawing)
                self.drawing = None
            self.mazeCanvas.delete("all")


class HomepageFrame(Frame):
    """
    The homepage of the application. Has 2 button: Create maze and Import maze
    """
    def __init__(self, controller, **kwargs):
        super().__init__(master=controller, **kwargs)
        self.controller = controller
        Label(controller, text="Search Algorithm Visualizer", fg='black', bg='white', font=("calibre", 30)).place(x=450,
                                                                                                                  y=0)
        Label(controller, text="by Anh Tuan Doan", fg='black', bg='white', font=("calibre", 15)).place(x=650, y=60)
        Button(controller, text='Create Maze', command=self.createMaze, bg='white', fg='black',
               highlightbackground='white', height=2, width=15, font=self.controller.font).place(x=430, y=120)
        Button(controller, text='Import Maze', command=self.importMaze, bg='white', fg='black',
               highlightbackground='white', height=2, width=15,  font=self.controller.font).place(x=650, y=120)

    def importMaze(self):
        self.controller.switchFrame(ImportFrame)

    def createMaze(self):
        self.controller.switchFrame(SelectMazeSizeFrame)


class ImportFrame(Frame):
    """The import page that allows the user to import an existing maze configuration"""
    def __init__(self, controller, **kwargs):
        super().__init__(master=controller, **kwargs)
        self.controller = controller
        self.controller.filename = self.importEnvironment()
        self.controller.drawMaze()
        Label(controller, text="The maze has been imported, click on the search button to find the solution",
              fg='black', bg='white', font=self.controller.font).place(x=40, y=20)
        Button(controller, text='Search', command=self.goSearchFrame, bg='white', fg='black',
               highlightbackground='white', height=2, width=15,  font=self.controller.font).place(x=40, y=60)

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
    """The search page that allows the user to see the searching process in real-time"""
    def __init__(self, controller, **kwargs):
        super().__init__(master=controller, **kwargs)
        self.controller = controller
        if not self.controller.filename is None and self.controller.environment is not None:
            Label(controller, text="Select one of the algorithms to start searching", fg='black', bg='white',
                  font=self.controller.font).place(x=40, y=20)
            self.algorithm = StringVar()
            self.controller = controller
            Radiobutton(controller,
                        text="Breadth-First Search",
                        variable=self.algorithm,
                        command=self.search,
                        value="BFS", bg="white", fg="black").place(x=40, y=60)

            Radiobutton(controller,
                        text="Depth-First Search",
                        variable=self.algorithm,
                        command=self.search,
                        value="DFS", bg="white", fg="black").place(x=200, y=60)
            Radiobutton(controller,
                        text="Greedy Best-First Search",
                        variable=self.algorithm,
                        command=self.search,
                        value="GBFS", bg="white", fg="black").place(x=360, y=60)
            Radiobutton(controller,
                        text="A* Search",
                        variable=self.algorithm,
                        command=self.search,
                        value="AS", bg="white", fg="black").place(x=560, y=60)
            Radiobutton(controller,
                        text="Bidirectional Search (Custom Uninformed Search)",
                        variable=self.algorithm,
                        command=self.search,
                        value="CUS1", bg="white", fg="black").place(x=660, y=60)
            Radiobutton(controller,
                        text="IDA Search (Custom Informed Search)",
                        variable=self.algorithm,
                        command=self.search,
                        value="CUS2", bg="white", fg="black").place(x=1000, y=60)
            self.legendCanvas = Canvas(controller, bg='white', width=1000, height=100,
                                       borderwidth=0, highlightthickness=0, name="legend")
            legendFont = ("calibre", 15)
            Label(self.legendCanvas, text="Start: ", fg='black',bg='white', font=legendFont).place(x=0,y=8)
            self.legendCanvas.create_rectangle(70, 0, 70 + 30, 0 + 30,
                                               fill="red")
            Label(self.legendCanvas, text="Goal: ", fg='black', bg='white',font=legendFont).place(x=150,y=8)
            self.legendCanvas.create_rectangle(220, 0, 220 + 30, 0 + 30,
                                               fill="green")
            Label(self.legendCanvas, text="Wall: ", fg='black', bg='white', font=legendFont).place(x=300,y=8)
            self.legendCanvas.create_rectangle(370, 0, 370 + 30, 0 +30,
                                               fill="black")
            Label(self.legendCanvas, text="Visited: ", fg='black', bg='white', font=legendFont).place(x=430,y=8)
            self.legendCanvas.create_rectangle(520, 0, 520 + 30, 0 + 30,
                                               fill="#241571")
            Label(self.legendCanvas, text="Path: ", fg='black', bg='white', font=legendFont).place(x=600,y=8)
            self.legendCanvas.create_rectangle(670, 0, 670 + 30, 0 + 30,
                                               fill="yellow")
            Label(self.legendCanvas, text="Frontier: ", fg='black', bg='white', font=legendFont).place(x=730,y=8)
            self.legendCanvas.create_rectangle(820, 0, 820 + 30, 0 + 30,
                                               fill="lightblue")

            self.legendCanvas.place(x=40, y=140)
            self.controller.drawMaze()
            self.solution = None

    def search(self):
        if self.solution is not None:
            self.solution.destroy()
        self.controller.path = []
        self.controller.visited = []
        self.controller.frontier = []
        method = self.algorithm.get()
        self.controller.robot = Robot(self.controller.filename)
        generator = self.controller.robot.solve(method)
        for result in generator:
            if not result["finish"]:
                self.controller.visited = result["visited"]
                self.controller.frontier = result["frontier"]

            else:
                if result["success"]:
                    self.controller.path = result["path"]
                    self.solution = Label(self.controller, text=f"Path to solution: {result['direction']}", fg='black',
                                          bg='white',
                                          font=self.controller.font)
                    self.solution.place(x=40, y=90)
                else:
                    self.solution = Label(self.controller, text=f"No solution found", fg='black', bg='white',
                                          font=self.controller.font)
                    self.solution.place(x=40, y=90)
            self.controller.tksleep(0.01)


class SelectMazeSizeFrame(Frame):
    """Allow the user to specify the number of row and column"""
    def __init__(self, controller, **kwargs):
        super().__init__(master=controller, **kwargs)
        self.controller = controller
        self.rowVar = IntVar()
        self.columnVar = IntVar()
        self.controller.environment = Environment()
        Label(controller, text="How many rows and column do you want to have for your maze?", fg='black', bg='white',
              font=self.controller.font).place(x=40, y=20)
        Label(controller, text="Row", fg='black', bg='white', font=self.controller.font).place(x=40, y=60)
        Entry(controller, textvariable=self.rowVar, fg='black', insertbackground='black',
              bg='white',font = self.controller.font).place(x=120, y=60)
        Label(controller, text="Column", fg='black', bg='white', font=self.controller.font).place(x=40, y=100)
        Entry(controller, textvariable=self.columnVar, fg='black', insertbackground='black',
              bg='white',font = self.controller.font).place(x=120, y=100)
        Button(controller, text='Confirm Size', command=self.confirmSize, bg='white', fg='black',
               highlightbackground='white', height=2, width=10,  font=self.controller.font).place(x=40, y=150)

    def confirmSize(self):
        self.controller.environment.row = self.rowVar.get()
        self.controller.environment.column = self.columnVar.get()
        self.controller.drawMaze()
        self.controller.switchFrame(SelectStartPointFrame)


class SelectStartPointFrame(Frame):
    """Allow the user to select the start node of the maze"""
    def __init__(self, controller, **kwargs):
        super().__init__(master=controller, **kwargs)
        self.controller = controller
        controller.bind("<ButtonRelease-1>", self.selectStartPoint)
        Label(controller, text="Select start point by clicking on a square in the maze", fg='black', bg='white',
              font=self.controller.font).place(x=40, y=20)
        Button(controller, text='Confirm start point', command=self.confirmStartPoint, bg='white', fg='black',
               highlightbackground='white', height=2, width=15,  font=self.controller.font).place(x=40, y=60)

    def selectStartPoint(self, event):
        if str(event.widget) == ".maze":
            mouse_x, mouse_y = event.x, event.y
            row = mouse_y // self.controller.squareSize
            column = mouse_x // self.controller.squareSize
            self.controller.environment.start = [column, row]

    def confirmStartPoint(self):
        self.controller.switchFrame(SelectGoalsFrame)


class SelectGoalsFrame(Frame):
    """Allow the user to select the goal nodes of the maze"""
    def __init__(self, controller, **kwargs):
        super().__init__(master=controller, **kwargs)
        controller.bind("<ButtonRelease-1>", self.selectGoals)
        self.controller = controller
        self.controller.environment.goals = []
        Label(controller,
              text="Select multiple goals by clicking on the squares in the maze. You can also click on a selected square to remove it",
              fg='black', bg='white', font=self.controller.font).place(x=40, y=20)
        Button(controller, text='Confirm goals', command=self.confirmGoals, bg='white', fg='black',
               highlightbackground='white', height=2, width=15,font=self.controller.font).place(x=40, y=60)

    def selectGoals(self, event):
        if str(event.widget) == ".maze":
            mouse_x, mouse_y = event.x, event.y
            row = mouse_y // self.controller.squareSize # calculate the row number based on the mouse position
            column = mouse_x // self.controller.squareSize # calculate the column number based on the mouse position
            if [column, row] in self.controller.environment.goals:
                self.controller.environment.goals.remove([column, row])
            elif [column, row] != self.controller.environment.start:
                self.controller.environment.goals.append([column, row])
            else:
                print("Point already occupied")

    def confirmGoals(self):
        self.controller.switchFrame(SelectWallFrame)


class SelectWallFrame(Frame):
    """Allow the user to select the wall squares"""
    def __init__(self, controller, **kwargs):
        super().__init__(master=controller, **kwargs)
        controller.bind("<ButtonRelease-1>", self.selectWalls)
        self.controller = controller
        self.controller.environment.walls = []
        Label(controller,
              text="Select multiple walls by clicking on the squares in the maze. You can also click on a selected square to remove it",
              fg='black', bg='white', font=self.controller.font).place(x=40, y=20)
        Button(controller, text='Save', command=self.confirmWalls, bg='white',
               fg='black',
               highlightbackground='white', height=2, width=15,  font=self.controller.font).place(x=40, y=60)

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
    """Allow the user to export the maze configuration to a txt file"""
    def __init__(self, controller, **kwargs):
        super().__init__(master=controller, **kwargs)
        self.controller = controller
        try:
            self.export()
        except:
            raise Exception("Can't export maze")
        Label(controller,
              text="The maze has been successfully saved. Go back to homepage to import the maze file and start searching",
              fg='black', bg='white', font=self.controller.font).place(x=40, y=20)
        Button(controller, text='Homepage', command=self.returnHomepage, bg='white',
               fg='black',
               highlightbackground='white', height=2, width=15, font=self.controller.font).place(x=40, y=60)

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
