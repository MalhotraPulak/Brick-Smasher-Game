from game_object import GameObject
from colorama import Back
import time


class Paddle(GameObject):

    def __init__(self, max_width, max_height):
        super().__init__(max_width, max_height, 0, 0)
        self.x = 0
        self.y = max_height - 1
        self.paddle_length = 5
        self.color = Back.GREEN
        self.paddle_bullets_enabled = False
        self.change_paddle_size(10)
        self.speed = 2
        self.last_bullet_gen = time.time()

    def move(self, inp):
        if inp == 'd':
            self.x = min(self.x + self.speed, self.max_width - self.length)
        elif inp == 'a':
            self.x = max(0, self.x - self.speed)

    def change_paddle_size(self, size):
        self.paddle_length = size
        if not self.paddle_bullets_enabled:
            self.set_show(" " * size)
        else:
            self.set_show("^" + " " * (size - 2) + "^")

    def enable_paddle_bullets(self):
        self.paddle_bullets_enabled = True
        self.change_paddle_size(self.paddle_length)

    def disable_paddle_bullets(self):
        self.paddle_bullets_enabled = False
        self.change_paddle_size(self.paddle_length)

    def gen_bullets(self):
        if time.time() - self.last_bullet_gen > 2 and self.paddle_bullets_enabled:
            self.last_bullet_gen = time.time()
            bullets = [Bullet(self.max_width, self.max_height, self.x, self.y - 1),
                       Bullet(self.max_width, self.max_height, self.x + self.paddle_length - 1, self.y - 1)]
            return bullets
        return None


class Bullet(GameObject):
    def __init__(self, max_width: int, max_height: int, x: int, y: int):
        super().__init__(max_width, max_height, x, y)
        self.dead = False
        self.speed_y = -1

    def move(self):
        self.y += self.speed_y
        if self.y <= 0:
            self.dead = True
