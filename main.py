import sys
from robot import Robot

def main():
    if len(sys.argv) != 3:
        raise Exception("Wrong number of argument")
    else:
        filename = sys.argv[1]
        method = sys.argv[2]
        robot = Robot(filename)
        generator = robot.solve(method)
        for result in generator:
            pass
        if result["success"]:
            print(filename,method,result["numberOfNodes"])
            print(result["direction"])
        else:
            print(result["message"])


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
main()