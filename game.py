import os
import random

from paddle import Paddle, Bullet
from screen import Screen
from ball import Ball

from game_object import GameObject, Collision, objects_collision_vh, objects_collision_d
import time
from powerup import PowerUpType, createPowerUp
import numpy as np
from util import cursor_to_top, log, get_bricks
from powerup import PowerUp
from ufo import UFO

speed_x = np.array([0.25, 0.5, 0.75])


class Game:

    def __init__(self, width, height):
        self.paddle = Paddle(width, height)
        self.screen = Screen(width, height)
        self.bricks = get_bricks(width, height, 1)
        self.final_boss = False
        self.ufo = None
        self.height = height
        self.width = width
        self.balls: [Ball] = [Ball(max_width=width, max_height=height, x=width // 2, y=height // 2)]
        self.ball_on_paddle = True
        self.powerups = []
        self.score = 0
        self.lives = 3
        self.time = time.time()
        self.active_powerups: [PowerUp] = []
        self.thru_ball = True
        self.grab_ball = False
        self.game_level = 1
        self.time_attack = False
        self.pending_defense = False
        self.paddle_bullets: [Bullet] = []
        os.system('clear')

    def input(self, inp):
        if inp == ' ':
            self.ball_on_paddle = False
        self.paddle.move(inp)

    def spawn_powerup(self, x, y, ball, rigged=False):
        if random.randint(0, 0) == 0 and not self.final_boss:
            self.powerups.append(createPowerUp(self.width, self.height, x, y, ball.speed_x * 0.5, ball.speed_y * 0.5))
        if self.final_boss and rigged:
            self.powerups.append(createPowerUp(self.width, self.height, x, y, 0, 1, rigged=True))

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
                    if self.time_attack and not self.final_boss:
                        for idd, _ in enumerate(self.bricks):
                            self.bricks[idd].y += 1
                    if self.final_boss:
                        if (self.ufo.health == 5 or self.ufo.health == 8) and self.pending_defense:
                            self.bricks += self.ufo.spawn_defense(self.ufo.health // 3)
                            self.pending_defense = False
                        # log(str(new_x_speed))
                    return
                if isinstance(obj, PowerUp):
                    return -1

    def brick_ball_collision(self):
        colz_ufo = False
        for idx2 in range(len(self.bricks)):
            for idx, ball in enumerate(self.balls):
                collision = objects_collision_vh(ball, self.bricks[idx2])
                if collision != Collision.NOPE:
                    colz_ufo = self.bricks[idx2].ufo
                    if not self.thru_ball:
                        new_strength = self.bricks[idx2].got_hit()
                        if new_strength <= 0:
                            self.score += 1
                            self.spawn_powerup(self.bricks[idx2].get_dim()[0], self.bricks[idx2].get_dim()[1], ball)
                        if collision == Collision.VERTICAL:
                            self.balls[idx].reverse_y_speed()
                        if collision == Collision.HORIZONTAL:
                            self.balls[idx].reverse_x_speed()
                        log("collision " + collision.name + "\n")
                    else:
                        self.bricks[idx2].strength = 0
                        self.score += 1
                        self.spawn_powerup(self.bricks[idx2].get_dim()[0], self.bricks[idx2].get_dim()[1], ball)
        self.bricks = [brick for brick in self.bricks if brick.strength > 0]
        for idx2 in range(len(self.bricks)):
            for idx, ball in enumerate(self.balls):
                collision = objects_collision_d(ball, self.bricks[idx2])
                if collision != Collision.NOPE:
                    colz_ufo = self.bricks[idx2].ufo
                    if not self.thru_ball:
                        new_strength = self.bricks[idx2].got_hit()
                        if new_strength <= 0:
                            self.score += 1
                            self.spawn_powerup(self.bricks[idx2].get_dim()[0], self.bricks[idx2].get_dim()[1], ball)
                        if collision == Collision.DIAGONAL:
                            self.balls[idx].reverse_x_speed()
                            self.balls[idx].reverse_y_speed()
                        log("collision " + collision.name + "\n")
                    else:
                        self.bricks[idx2].strength = 0
                        self.score += 1
                        self.spawn_powerup(self.bricks[idx2].get_dim()[0], self.bricks[idx2].get_dim()[1], ball)
        self.bricks = [brick for brick in self.bricks if brick.strength > 0]
        if self.final_boss and colz_ufo:
            self.ufo.health -= 1
            if self.ufo.health == 5 or self.ufo.health == 8:
                self.pending_defense = True

    def brick_bullet_collision(self):
        for idx2 in range(len(self.bricks)):
            for idx, bullet in enumerate(self.paddle_bullets):
                collision = objects_collision_vh(bullet, self.bricks[idx2])
                if collision != Collision.NOPE:
                    new_strength = self.bricks[idx2].got_hit()
                    if new_strength <= 0:
                        self.score += 1
                        self.spawn_powerup(self.bricks[idx2].get_dim()[0], self.bricks[idx2].get_dim()[1],
                                           self.balls[0])
                    self.paddle_bullets[idx].dead = True
        self.bricks = [brick for brick in self.bricks if brick.strength > 0]

    def check_collision(self):
        # check if ball collided with bricks
        self.brick_ball_collision()
        log("dickkk " + str(len(self.paddle_bullets)))
        self.brick_bullet_collision()
        self.paddle_bullets = [bullet for bullet in self.paddle_bullets if not bullet.dead]
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
                log("activated powerup " + powerup.type.name + "\n")
                # log(str(len(self.balls)))
            else:
                new_powerups.append(powerup)
        self.powerups = new_powerups

    def play(self):
        if self.final_boss and self.ufo.health == 0:
            return -2, self.score + 200, int(time.time() - self.time)
        if self.lives <= 0:
            return -1, self.score, int(time.time() - self.time)

        # active powerups
        new_active = []
        for pw in self.active_powerups:
            if time.time() - pw.time > 10:
                pw.power_up_deactivate(self)
            else:
                new_active.append(pw)
        self.active_powerups = new_active

        # move bullets
        for bullet in self.paddle_bullets:
            bullet.move()
        self.paddle_bullets = [bullet for bullet in self.paddle_bullets if not bullet.dead]

        # bricks
        for brick in self.bricks:
            brick.change()
            if brick.y == self.paddle.y:
                return -1, self.score, int(time.time() - self.time)

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
                return -1, self.score, int(time.time() - self.time)

        # move powerups
        new_powerups = []
        for powerup in self.powerups:
            if powerup.move() != -1:
                new_powerups.append(powerup)
        self.powerups = new_powerups

        # check for collisions
        self.check_collision()

        # ball on paddle
        paddle_x, paddle_y, paddle_show, _, _ = self.paddle.get_dim()
        paddle_center = paddle_x + len(paddle_show) / 2
        if self.ball_on_paddle:
            [ball.set_x_y(int(paddle_center), paddle_y - 1) for ball in self.balls]
            # set all the sprites and render
        if self.final_boss:
            self.ufo.move(paddle_center)

        self.screen.set_sprites(paddle=self.paddle, bricks=self.bricks, balls=self.balls, powerups=self.powerups,
                                bullets=self.paddle_bullets)
        cursor_to_top()
        pw_time = 0
        for pw in self.active_powerups:
            if pw.get_type() == PowerUpType.BULLET:
                pw_time = time.time() - pw.time
        ufo_health = -1
        if self.final_boss:
            ufo_health = self.ufo.health
        self.screen.render(self.time, self.score, self.lives, self.game_level, pw_time, ufo_health)

        # get bullets
        new_b = self.paddle.gen_bullets()
        if new_b is not None:
            self.paddle_bullets = new_b

        if self.final_boss and self.ufo.bombTime():
            self.spawn_powerup(random.randint(self.ufo.x_start, self.ufo.x_end), self.ufo.y + 5, self.balls[0],
                               rigged=True)
            # self.spawn_powerup(random.randint(self.ufo.x_start, self.ufo.x_end), self.ufo.y + 5, self.balls[0],
            #                    rigged=True)
            self.ufo.last_bomb = time.time()
        # check for time attack
        if not self.time_attack and time.time() - self.time > 5:
            self.time_attack = True
        # check for level end
        level_end = True
        for brick in self.bricks:
            if brick.strength != 4:
                level_end = False
        if level_end:
            self.game_level += 1

            if self.game_level == 4:
                return -2, self.score, int(time.time() - self.time)
            else:
                self.powerups = []
                for powerup in self.active_powerups:
                    powerup.power_up_deactivate(self)
                self.active_powerups = []
                if self.game_level == 3:
                    self.final_boss = True
                    self.ufo = UFO(self.width, self.height, 0, 0)
                    self.bricks = self.ufo.art_to_bricks()
                else:
                    self.bricks = get_bricks(self.width, self.height, self.game_level)
                self.ball_on_paddle = True
                self.time = time.time()
                self.time_attack = False
                self.balls = [self.balls[0]]
                log("level upped")
        return 0, 0, 0
