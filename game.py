import os
from paddle import Paddle
from screen import Screen
from brick import Brick
from ball import Ball
from numpy import genfromtxt
from game_object import GameObject
import time
from powerup import PowerUpType, createPowerUp
from enum import Enum
import numpy as np
from powerup import PowerUp


class Collision(Enum):
    VERTICAL, HORIZONTAL, DIAGONAL, NOPE = range(4)


BRICK_SIZE = 6


def cursor_to_top():
    print("\033[0;0H")


def log(s):
    with open("a.txt", "a") as f:
        f.write(s)


speed_x = np.array([0.25, 0.5, 0.75])


def get_bricks(width, height) -> [Brick]:
    data = genfromtxt('brick_pattern.csv', delimiter=',')
    bricks = []
    for line in data:
        new_brick = Brick(max_width=width, max_height=height, strength=int(line[-1]),
                          y=int(line[0]), x=int(line[1] * BRICK_SIZE), size=BRICK_SIZE)
        bricks.append(new_brick)
    return bricks


class Game:

    def __init__(self, width, height):
        self.paddle = Paddle(width, height)
        self.screen = Screen(width, height)
        self.bricks = get_bricks(width, height)
        self.height = height
        self.width = width
        self.balls: [Ball] = [Ball(max_width=width, max_height=height, x=width // 2, y=height // 2)]
        self.ball_on_paddle = True
        self.powerups = []
        self.score = 0
        self.lives = 3
        self.time = time.time()
        self.active_powerups: [PowerUp] = []
        self.thru_ball = False
        os.system('clear')

    def input(self, inp):
        if inp == ' ':
            self.ball_on_paddle = False
        self.paddle.move(inp)

    def spawn_powerup(self, x, y):
        self.powerups.append(createPowerUp(self.width, self.height, x, y))


    def check_paddle_collision(self, obj: GameObject):
        ball_x, ball_y, _, _, _ = obj.get_dim()
        paddle_x, paddle_y, paddle_show, _, _ = self.paddle.get_dim()
        paddle_center = paddle_x + len(paddle_show) / 2
        for i in range(len(paddle_show)):
            paddle_part_x = paddle_x + i
            dist_x = ball_x - paddle_part_x
            dist_y = ball_y - paddle_y
            if dist_x == 0 and dist_y == -1:
                if isinstance(obj, Ball):
                    if obj.get_speed()[1] < 0:
                        continue
                    paddle_dist_center = ball_x - paddle_center
                    ratio_dist = abs(2 * paddle_dist_center / len(paddle_show))
                    new_x_speed = speed_x.flat[np.abs(speed_x - ratio_dist).argmin()]
                    if ball_x < paddle_center:
                        new_x_speed = -new_x_speed
                    obj.set_speed_x(new_x_speed)
                    obj.reverse_y_speed()
                    log(str(new_x_speed))
                    return
                if isinstance(obj, PowerUp):
                    return -1

    def objects_collision(self, small: GameObject, big: GameObject):
        small_x, small_y, _, _, small_len = small.get_dim()
        big_x, big_y, _, _, big_len = big.get_dim()
        for i in range(big_len):
            big_part_x = big_x + i
            dist_x = small_x - big_part_x
            dist_y = small_y - big_y
            if (dist_x == 0 and dist_y == 1 and small.get_speed()[1] < 0) or (
                    dist_x == 0 and dist_y == -1 and small.get_speed()[1] > 0):
                return Collision.VERTICAL
            if (dist_y == 0 and dist_x == 1 and small.get_speed()[0] < 0) or (
                    dist_y == 0 and dist_x == -1 and small.get_speed()[0] > 0):
                return Collision.HORIZONTAL
        return Collision.NOPE

    def brick_ball_collision(self):
        for idx2 in range(len(self.bricks)):
            for idx, ball in enumerate(self.balls):
                collision = self.objects_collision(ball, self.bricks[idx2])
                if collision != Collision.NOPE:
                    new_strength = self.bricks[idx2].got_hit()
                    if new_strength <= 0:
                        self.score += 1
                        self.spawn_powerup(self.bricks[idx2].get_dim()[0], self.bricks[idx2].get_dim()[1])
                    if collision == Collision.VERTICAL:
                        self.balls[idx].reverse_y_speed()
                    if collision == Collision.HORIZONTAL:
                        self.balls[idx].reverse_x_speed()
        self.bricks = [brick for brick in self.bricks if brick.strength > 0]

    def check_collision(self):
        # check if ball collided with bricks
        self.brick_ball_collision()
        # check if ball collided with paddle
        [self.check_paddle_collision(ball) for ball in self.balls]
        # check if a powerup collided with paddle
        new_powerups = []
        for powerup in self.powerups:
            if self.check_paddle_collision(powerup) == -1:
                self.active_powerups = [pw for pw in self.active_powerups if powerup.get_type() != pw.get_type()]
                powerup.set_time(time.time())
                self.active_powerups.append(powerup)
                powerup.power_up_activate(self)
                log("activated powerup " + powerup.type.name)
                log(str(len(self.balls)))
            else:
                new_powerups.append(powerup)
        self.powerups = new_powerups

    def play(self):
        # active powerups
        new_active = []
        for pw in self.active_powerups:
            if time.time() - pw.time > 5:
                pw.power_up_deactivate(self)
            else:
                new_active.append(pw)
        self.active_powerups = new_active

        # move balls
        alive_ball = False
        for ball in self.balls:
            if ball.move() != -1:
                alive_ball = True
            else:
                ball.dead = True
        self.balls = [ball for ball in self.balls if not ball.dead]
        if not alive_ball:
            self.lives -= 1
            self.balls.append(Ball(self.width, self.height, 0, 0))
            self.ball_on_paddle = True
            if self.lives == 0:
                self.__init__(self.width, self.height)

        # move powerups
        new_powerups = []
        for powerup in self.powerups:
            if powerup.move() != -1:
                new_powerups.append(powerup)
        self.powerups = new_powerups

        # check for collisions
        self.check_collision()
        paddle_x, paddle_y, paddle_show, _, _ = self.paddle.get_dim()
        paddle_center = paddle_x + len(paddle_show) / 2
        if self.ball_on_paddle:
            [ball.set_x_y(int(paddle_center), paddle_y - 1) for ball in self.balls]
        # set all the sprites and render
        self.screen.set_sprites(paddle=self.paddle, bricks=self.bricks, balls=self.balls, powerups=self.powerups)
        cursor_to_top()
        self.screen.render(self.time, self.score, self.lives)
