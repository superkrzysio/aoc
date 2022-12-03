import turtle
import time

# "programmed fast" version, definitely not "running fast"

class Board:
    def __init__(self):
        self.row = []

    def at(self, row, col):
        [row, col] = self.unwrap(row, col)

        return self.row[row][col]

    def unwrap(self, row, col):
        while row < 0:
            row += len(self.row)
        while row >= len(self.row):
            row -= len(self.row)

        current_col = self.row[row]
        while col < 0:
            col += len(current_col)
        while col >= len(current_col):
            col -= len(current_col)

        return row, col

    def add_row(self, row: list):
        self.row.append(row)

    def get_size(self):
        return len(self.row), len(self.row[0])

    def set(self, row, col, val):
        [row, col] = self.unwrap(row, col)
        self.row[row][col] = val

    def __str__(self):
        ret = ""
        for row in self.row:
            for col in row:
                ret += col
            ret += "\n"
        return ret


class Loader:
    def __init__(self, file: str, consumer: Board):
        self.consumer = consumer
        self.file = file

    def load(self):
        with open(self.file, "r") as fp:
            while line := fp.readline():
                self.consumer.add_row(list(line.strip()))
        return self.consumer


class Graphix:

    MAX_FPS = 5
    COLORS = {">": (255, 0, 0), "v": (255, 255, 0), "white": (255, 255, 255)}

    def __init__(self, width, height, pixelsize = 1):
        self.width = width
        self.height = height
        self.pixelsize = pixelsize

        width = self.scale_by_pixelsize(width)
        height = self.scale_by_pixelsize(height)

        turtle.setup(width, height)
        turtle.setworldcoordinates(0, 0, width, height)
        self.recent_render = time.time()
        self.max_frame_time = 1/Graphix.MAX_FPS

    def scale_by_pixelsize(self, val, shift=2):
        return (val+shift) * self.pixelsize

    def drawpixel(self, x, y, color):
        y = self.height - y
        turtle.tracer(0, 0)
        turtle.colormode(255)
        turtle.penup()
        turtle.setpos(self.scale_by_pixelsize(x, 1), self.scale_by_pixelsize(y, 1))
        turtle.color(color)
        turtle.pendown()
        turtle.begin_fill()
        for i in range(4):
            turtle.forward(self.pixelsize)
            turtle.right(90)
        turtle.end_fill()

    def showimage(self):
        render_interval = time.time() - self.recent_render
        time_to_sleep = self.max_frame_time - render_interval
        if time_to_sleep > 0:
            time.sleep(time_to_sleep)
        self.recent_render = time.time()
        turtle.hideturtle()
        turtle.update()


    def clear(self):
        turtle.clear()


board = Loader("input.txt", Board()).load()
pixel_size = int(600 / board.get_size()[1])
graphix = Graphix(board.get_size()[1], board.get_size()[0], pixel_size)

print("init graphix: " + str((board.get_size()[1], board.get_size()[0])) + ", pixel size: " + str(pixel_size))

step = 0
[w, h] = board.get_size()



moved_anything = True
while moved_anything:
    moved_anything = False
    step += 1
    graphix.clear()
    for herd in [">", "v"]:
        movable = []
        # marking, todo: optimize: use pro indexing with numpy...
        for x in range(w):
            for y in range(h):
                target_x = x
                target_y = y
                if herd == ">":
                    target_y += 1
                if herd == "v":
                    target_x += 1
                at = board.at(x, y)
                if at == herd:
                    if board.at(target_x, target_y) == ".":
                        movable.append({"from": (x, y), "to": (target_x, target_y)})
                        graphix.drawpixel(target_x, target_y, Graphix.COLORS[herd])
                    else:
                        graphix.drawpixel(x, y, Graphix.COLORS[herd])
                # elif at == ".":
                #     graphix.drawpixel(x, y, Graphix.COLORS["white"])

        # moving
        for moving in movable:
            moved_anything = True
            board.set(moving["from"][0], moving["from"][1], ".")
            board.set(moving["to"][0], moving["to"][1], herd)

    graphix.showimage()

print(step)