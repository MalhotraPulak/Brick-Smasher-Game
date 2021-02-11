import os
from paddle import Paddle
from screen import Screen
from brick import Brick
from ball import Ball
from numpy import genfromtxt
from game_object import GameObject

BRICK_SIZE = 6


def cursor_to_top():
    print("\033[0;0H")


def log(s):
    with open("a.txt", "a") as f:
        f.write(s)


class Game:

    def get_bricks(self, width, height) -> [Brick]:
        data = genfromtxt('brick_pattern.csv', delimiter=',')
        bricks = []
        for line in data:
            new_brick = Brick(max_width=width, max_height=height, strength=int(line[-1]),
                              y=int(line[0]), x=int(line[1] * BRICK_SIZE), size=BRICK_SIZE)
            bricks.append(new_brick)
        return bricks

    def __init__(self, width, height):
        self.paddle = Paddle(width, height)
        self.screen = Screen(width, height)
        self.bricks = self.get_bricks(width, height)
        self.height = height
        self.width = width
        self.ball = Ball(max_width=width, max_height=height, x=width // 2, y=height // 2)
        os.system('clear')

    def input(self, inp):
        self.paddle.move(inp)

    def check_one_brick(self, brick: Brick):
        ball_x, ball_y, _, _ = self.ball.get_dim()
        brick_x, brick_y, _, _ = brick.get_dim()
        for i in range(BRICK_SIZE):
            brick_part_x = brick_x + i
            dist_x = ball_x - brick_part_x
            dist_y = ball_y - brick_y
            if (dist_x == 0 and dist_y == 1 and self.ball.get_speed()[1] < 0) or (
                    dist_x == 0 and dist_y == -1 and self.ball.get_speed()[1] > 0):
                self.ball.reverse_y_speed()
                if brick.got_hit() <= 0:
                    return None
                else:
                    return brick
            if (dist_y == 0 and dist_x == 1 and self.ball.get_speed()[0] < 0) or (
                    dist_y == 0 and dist_x == -1 and self.ball.get_speed()[0] > 0):
                self.ball.reverse_x_speed()
                if brick.got_hit() <= 0:
                    return None
                else:
                    return brick
        return brick

    def check_paddle_collision(self, obj: GameObject):
        ball_x, ball_y, _, _ = obj.get_dim()
        paddle_x, paddle_y, paddle_show, _ = self.paddle.get_dim()
        paddle_center = paddle_x + len(paddle_show) / 2
        for i in range(len(paddle_show)):
            paddle_part_x = paddle_x + i
            dist_x = ball_x - paddle_part_x
            dist_y = ball_y - paddle_y
            if (dist_x == 0 and dist_y == 1 and self.ball.get_speed()[1] < 0) or (
                    dist_x == 0 and dist_y == -1 and self.ball.get_speed()[1] > 0):
                with open("a.txt", "a") as f:
                    f.write(f"pd {ball_x} {ball_y} {paddle_part_x} {paddle_y}\n")
                paddle_dist_center = ball_x - paddle_center
                ratio_dist = paddle_dist_center / len(paddle_show)
                new_x_speed = ratio_dist * 2
                log(str(new_x_speed))
                self.ball.set_speed_x(new_x_speed)
                self.ball.set_speed_y(-(1 - new_x_speed ** 2))

    def check_collision(self):
        new_bricks = []
        for brick in self.bricks:
            brick = self.check_one_brick(brick)
            if brick is not None:
                new_bricks.append(brick)
        self.bricks = new_bricks
        self.check_paddle_collision(self.ball)

    def play(self):
        self.ball.move()
        self.check_collision()
        self.screen.set_sprites(paddle=self.paddle, bricks=self.bricks, ball=self.ball)
        cursor_to_top()
        self.screen.render()
