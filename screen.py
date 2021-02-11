from paddle import Paddle
from game_object import GameObject
from colorama import Back


class Screen:
    def set_empty_screen(self):
        mat = []
        for i in range(self.height):
            mat.append([' ' for _ in range(self.width)])
        self.mat = mat

    def __init__(self, width: int, height: int):
        self.mat = None
        self.height = height
        self.width = width
        self.set_empty_screen()

    def add_object(self, obj: GameObject):
        object_x, object_y, object_show, object_color = obj.get_dim()
        print(":" + str(len(object_show)) + ":", end="\n")
        for i in range(len(object_show)):
            self.mat[object_y][object_x + i] = object_show[i]
        self.mat[object_y][object_x] = object_color + self.mat[object_y][object_x]
        self.mat[object_y][object_x + len(object_show) - 1] += Back.RESET

    def set_sprites(self, paddle: Paddle):
        self.set_empty_screen()
        self.add_object(paddle)

    def render(self):
        self.add_border()
        for idx, line in enumerate(self.mat):
            for c in line:
                print(c, end="")
            print(end="\n")

    def add_border(self):
        self.mat.insert(0, ["_" for _ in range(self.width)])
        self.mat.append(["_" for _ in range(self.width)])
        for i in range(len(self.mat)):
            self.mat[i].insert(0, "|")
            self.mat[i].append("|")
