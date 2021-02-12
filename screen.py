from paddle import Paddle
from game_object import GameObject
from colorama import Back
from brick import Brick
from ball import Ball
import time
from powerup import PowerUp


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
        object_x, object_y, object_show, object_color, object_len = obj.get_dim()
        for i in range(object_len):
            self.mat[object_y][object_x + i] = object_color + object_show[i] + Back.RESET

    def set_sprites(self, paddle: Paddle, bricks: [Brick], balls: [Ball], powerups: [PowerUp]):
        self.set_empty_screen()
        self.add_object(paddle)
        for brick in bricks:
            self.add_object(brick)
        for powerup in powerups:
            self.add_object(powerup)
        for ball in balls:
            self.add_object(ball)

    def render(self, time2, score, lives):
        print(f"Time {int(time.time() - time2)}  Score {score}  Lives {lives}\n", end="")
        self.add_border()
        # for i in range(self.width):
        #     print((i - 1) % 10, end="")
        # print()
        for idx, line in enumerate(self.mat):
            print(f'{idx % 10}', end="")
            for c in line:
                print(c, end="")
            print()

    def add_border(self):
        self.mat.insert(0, ["_" for _ in range(self.width)])
        self.mat.append(["_" for _ in range(self.width)])
        for i in range(len(self.mat)):
            self.mat[i].insert(0, "|")
            self.mat[i].append("|")
