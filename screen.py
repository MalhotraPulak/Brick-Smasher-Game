from paddle import Paddle
from game_object import GameObject
from colorama import Back
from brick import Brick
from ball import Ball
import time
from powerup import PowerUp
from util import log

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
        log(f"{object_x} !! {object_y} \n")
        for i in range(object_len):
            self.mat[object_y][min(object_x + i, self.width - 1)] = object_color + object_show[i] + Back.RESET

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
        for idx, line in enumerate(self.mat):
            print(' ', end="")
            for c in line:
                print(c, end="")
            print()

    def add_border(self):
        self.mat.insert(0, [u"━" for _ in range(self.width)])
        self.mat.append(["─" for _ in range(self.width)])
        for i in range(len(self.mat)):
            self.mat[i].insert(0, u"┃")
            self.mat[i].append(u"┃")
