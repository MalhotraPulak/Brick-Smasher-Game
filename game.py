import os
import random

from paddle import Paddle
from screen import Screen
from ball import Ball

from game_object import GameObject, Collision, objects_collision
import time
from powerup import PowerUpType, createPowerUp
import numpy as np
from util import cursor_to_top, log, get_bricks
from powerup import PowerUp

speed_x = np.array([0.25, 0.5, 0.75])


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
        self.grab_ball = False
        os.system('clear')

    def input(self, inp):
        if inp == ' ':
            self.ball_on_paddle = False
        self.paddle.move(inp)

    def spawn_powerup(self, x, y):
        if random.randint(0, 2) == 0:
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
                    if self.grab_ball:
                        self.ball_on_paddle = True
                    log(str(new_x_speed))
                    return
                if isinstance(obj, PowerUp):
                    return -1

    def brick_ball_collision(self):
        for idx2 in range(len(self.bricks)):
            for idx, ball in enumerate(self.balls):
                collision = objects_collision(ball, self.bricks[idx2])
                if collision != Collision.NOPE:
                    if not self.thru_ball:
                        new_strength = self.bricks[idx2].got_hit()
                        if new_strength <= 0:
                            self.score += 1
                            self.spawn_powerup(self.bricks[idx2].get_dim()[0], self.bricks[idx2].get_dim()[1])
                        if collision == Collision.VERTICAL:
                            self.balls[idx].reverse_y_speed()
                        if collision == Collision.HORIZONTAL:
                            self.balls[idx].reverse_x_speed()
                    else:
                        self.bricks[idx2].strength = 0
                        self.score += 1
                        self.spawn_powerup(self.bricks[idx2].get_dim()[0], self.bricks[idx2].get_dim()[1])

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
                if powerup.get_type() == PowerUpType.SHRINK or powerup.get_type() == PowerUpType.EXP:
                    self.active_powerups = [pw for pw in self.active_powerups if
                                            pw.get_type() not in [PowerUpType.EXP, PowerUpType.SHRINK]]
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
            if time.time() - pw.time > 10:
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
            for powerup in self.active_powerups:
                powerup.power_up_deactivate(self)
            self.active_powerups = []
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
