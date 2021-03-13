from ball import Ball
from game_object import GameObject
from enum import Enum
from random import randint
from colorama import Back
from util import log


class PowerUpType(Enum):
    SHRINK, EXP, MULT, FAST, THRU, GRAB, BULLET, BOMB = range(8)


def createPowerUp(max_w, max_h, x, y, ball_x, ball_y, rigged=False):
    i = randint(0, 6)
    if rigged:
        i = 7
    if i == 0:
        return ShrinkPowerUp(max_w, max_h, x, y, i, ball_x, ball_y)
    if i == 1:
        return ExpPowerUp(max_w, max_h, x, y, i, ball_x, ball_y)
    if i == 2:
        return MultPowerUp(max_w, max_h, x, y, i, ball_x, ball_y)
    if i == 3:
        return FastPowerUp(max_w, max_h, x, y, i, ball_x, ball_y)
    if i == 4:
        return ThruPowerUp(max_w, max_h, x, y, i, ball_x, ball_y)
    if i == 5:
        return GrabPowerUp(max_w, max_h, x, y, i, ball_x, ball_y)
    if i == 6:
        return BulletPowerUp(max_w, max_h, x, y, i, ball_x, ball_y)
    if i == 7:
        return BombPowerUp(max_w, max_h, x, y, i, ball_x, ball_y)


class PowerUp(GameObject):
    def __init__(self, max_width: int, max_height: int, x: int, y: int, pw_type: int, ball_x, ball_y):
        super().__init__(max_width, max_height, x, y)
        self.actual_x = x
        self.actual_y = y
        self.color = Back.BLACK
        self.type = PowerUpType(pw_type)
        self.time = 0
        self.speed_x = ball_x
        self.speed_y = ball_y
        self.set_show(str(pw_type))

    def move(self):
        self.actual_x += self.speed_x
        self.actual_y += self.speed_y
        self.speed_y = min(self.speed_y + 0.01, 0.5)
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

    def get_type(self):
        return self.type

    def power_up_activate(self, game):
        pass

    def power_up_deactivate(self, game):
        pass

    def set_time(self, time):
        self.time = time

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


class ShrinkPowerUp(PowerUp):
    def __init__(self, max_width: int, max_height: int, x: int, y: int, pw_type: int, ball_x, ball_y):
        super().__init__(max_width, max_height, x, y, pw_type, ball_x, ball_y)

    def power_up_activate(self, game):
        game.paddle.change_paddle_size(5)
        game.paddle.color = Back.RED

    def power_up_deactivate(self, game):
        game.paddle.change_paddle_size(10)
        game.paddle.color = Back.GREEN


class ExpPowerUp(PowerUp):
    def __init__(self, max_width: int, max_height: int, x: int, y: int, pw_type: int, ball_x, ball_y):
        super().__init__(max_width, max_height, x, y, pw_type, ball_x, ball_y)

    def power_up_activate(self, game):
        game.paddle.change_paddle_size(20)
        game.paddle.color = Back.MAGENTA

    def power_up_deactivate(self, game):
        game.paddle.change_paddle_size(10)
        game.paddle.color = Back.GREEN


class MultPowerUp(PowerUp):
    def __init__(self, max_width: int, max_height: int, x: int, y: int, pw_type: int, ball_x, ball_y):
        super().__init__(max_width, max_height, x, y, pw_type, ball_x, ball_y)

    def power_up_activate(self, game):
        new_balls = []
        for ball in game.balls:
            new_balls.append(ball)
            new_balls.append(Ball(self.max_width, self.max_height, ball.x, ball.y))
        game.balls = new_balls

    def power_up_deactivate(self, game):
        pass


class FastPowerUp(PowerUp):
    def __init__(self, max_width: int, max_height: int, x: int, y: int, pw_type: int, ball_x, ball_y):
        super().__init__(max_width, max_height, x, y, pw_type, ball_x, ball_y)

    def power_up_activate(self, game):
        for ball in game.balls:
            ball.set_speed(1)

    def power_up_deactivate(self, game):

        for ball in game.balls:
            ball.set_speed(0.5)


class ThruPowerUp(PowerUp):
    def __init__(self, max_width: int, max_height: int, x: int, y: int, pw_type: int, ball_x, ball_y):
        super().__init__(max_width, max_height, x, y, pw_type, ball_x, ball_y)

    def power_up_activate(self, game):
        game.thru_ball = True

    def power_up_deactivate(self, game):
        game.thru_ball = False


class GrabPowerUp(PowerUp):
    def __init__(self, max_width: int, max_height: int, x: int, y: int, pw_type: int, ball_x, ball_y):
        super().__init__(max_width, max_height, x, y, pw_type, ball_x, ball_y)

    def power_up_activate(self, game):
        game.grab_ball = True
        game.paddle.color = Back.YELLOW

    def power_up_deactivate(self, game):
        game.grab_ball = False
        game.paddle.color = Back.GREEN


class BulletPowerUp(PowerUp):
    def __init__(self, max_width: int, max_height: int, x: int, y: int, pw_type: int, ball_x, ball_y):
        super().__init__(max_width, max_height, x, y, pw_type, ball_x, ball_y)

    def power_up_activate(self, game):
        game.paddle.enable_paddle_bullets()
        game.paddle.color = Back.BLUE

    def power_up_deactivate(self, game):
        game.paddle.disable_paddle_bullets()
        game.paddle.color = Back.GREEN


class BombPowerUp(PowerUp):
    def __init__(self, max_width: int, max_height: int, x: int, y: int, pw_type: int, ball_x, ball_y):
        super().__init__(max_width, max_height, x, y, pw_type, ball_x, ball_y)
        self.color = Back.RED
        self.set_show("*")

    def power_up_activate(self, game):
        game.lives -= 1

    def power_up_deactivate(self, game):
        pass