from ball import Ball
from game_object import GameObject
from enum import Enum
from random import randint
from colorama import Back
from copy import deepcopy

def log(s):
    with open("a.txt", "a") as f:
        f.write(s)

class PowerUpType(Enum):
    SHRINK, EXP, MULT, FAST, THRU, GRAB = range(6)


def createPowerUp(max_w, max_h, x, y):
    i = randint(0, 5)
    if i == 0:
        return ShrinkPowerUp(max_w, max_h, x, y, i)
    if i == 1:
        return ExpPowerUp(max_w, max_h, x, y, i)
    if i == 2:
        return MultPowerUp(max_w, max_h, x, y, i)
    if i == 3:
        return FastPowerUp(max_w, max_h, x, y, i)
    if i == 4:
        return ThruPowerUp(max_w, max_h, x, y, i)
    if i == 5:
        return GrabPowerUp(max_w, max_h, x, y, i)


class PowerUp(GameObject):
    def __init__(self, max_width: int, max_height: int, x: int, y: int, pw_type: int):
        super().__init__(max_width, max_height, x, y)
        self.speed = 0.5
        self.buffer = 0
        self.color = Back.BLACK
        self.type = PowerUpType(pw_type)
        self.time = 0
        self.set_show(str(pw_type))

    def move(self):
        self.buffer += self.speed
        if self.buffer > 1:
            self.y += 1
            self.buffer = 0
        if self.y >= self.max_height:
            self.y -= 1
            return -1
        return 0

    def get_type(self):
        return self.type

    def power_up_activate(self, game):
        pass

    def power_up_deactivate(self, game):
        pass

    def set_time(self, time):
        self.time = time


class ShrinkPowerUp(PowerUp):
    def __init__(self, max_width: int, max_height: int, x: int, y: int, pw_type: int):
        super().__init__(max_width, max_height, x, y, pw_type)

    def power_up_activate(self, game):
        game.paddle.change_paddle_size(5)

    def power_up_deactivate(self, game):
        game.paddle.change_paddle_size(10)


class ExpPowerUp(PowerUp):
    def __init__(self, max_width: int, max_height: int, x: int, y: int, pw_type: int):
        super().__init__(max_width, max_height, x, y, pw_type)

    def power_up_activate(self, game):
        game.paddle.change_paddle_size(20)

    def power_up_deactivate(self, game):
        game.paddle.change_paddle_size(10)


class MultPowerUp(PowerUp):
    def __init__(self, max_width: int, max_height: int, x: int, y: int, pw_type: int):
        super().__init__(max_width, max_height, x, y, pw_type)

    def power_up_activate(self, game):
        new_balls = []
        for ball in game.balls:
            new_balls.append(ball)
            new_balls.append(Ball(self.max_width, self.max_height, ball.x, ball.y))
        game.balls = new_balls

    def power_up_deactivate(self, game):
        pass


class FastPowerUp(PowerUp):
    def __init__(self, max_width: int, max_height: int, x: int, y: int, pw_type: int):
        super().__init__(max_width, max_height, x, y, pw_type)

    def power_up_activate(self, game):
        for ball in game.balls:
            ball.set_speed(1)

    def power_up_deactivate(self, game):

        for ball in game.balls:
            ball.set_speed(0.5)


class ThruPowerUp(PowerUp):
    def __init__(self, max_width: int, max_height: int, x: int, y: int, pw_type: int):
        super().__init__(max_width, max_height, x, y, pw_type)

    def power_up_activate(self, game):
        game.thru_ball = True

    def power_up_deactivate(self, game):
        game.thru_ball = False


class GrabPowerUp(PowerUp):
    def __init__(self, max_width: int, max_height: int, x: int, y: int, pw_type: int):
        super().__init__(max_width, max_height, x, y, pw_type)

    def power_up_activate(self, game):
        game.grab_ball = True

    def power_up_deactivate(self, game):
        game.grab_ball = False
