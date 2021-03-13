from game_object import GameObject
from colorama import Back
from util import log
import random


class Ball(GameObject):
    def __init__(self, max_width: int, max_height: int, x: int, y: int):
        super().__init__(max_width, max_height, x, y)
        self.speed_multiplier = 0.5
        self.speed_x = random.randint(-2, 2) * 0.25
        self.speed_y = -0.5
        self.actual_x = x
        self.actual_y = y
        self.color = Back.RESET
        self.set_show("○")

    def move(self):
        self.actual_x += self.speed_x * self.speed_multiplier
        self.actual_y += self.speed_y * self.speed_multiplier
        if self.actual_x >= self.max_width - self.length:
            self.actual_x = self.max_width - self.length - 1
            self.reverse_x_speed()
        if self.actual_x < 0:
            self.actual_x = 0
            self.reverse_x_speed()
        if self.actual_y >= self.max_height:
            self.actual_y = self.max_height - 1
            return -1
        if self.actual_y < 0:
            self.actual_y = 0
            self.reverse_y_speed()
        log(f"{self.x} {self.y}\n")
        if abs(self.actual_x - self.x) >= 1:
            self.x = int(round(self.actual_x))
        if abs(self.actual_y - self.y) >= 1:
            self.y = int(round(self.actual_y))
        return 0

    def reverse_x_speed(self):
        self.actual_x = self.x
        self.speed_x = -self.speed_x

    def reverse_y_speed(self):
        self.actual_y = self.y
        self.speed_y = -self.speed_y

    def get_speed(self):
        return self.speed_x, self.speed_y

    def set_speed_x(self, inp):
        self.speed_x = inp

    def set_speed_y(self, inp):
        self.speed_y = inp

    def set_x_y(self, x, y):
        self.x = x
        self.actual_x = x
        self.y = y
        self.actual_y = y

    def set_speed(self, s):
        self.speed_multiplier = s
