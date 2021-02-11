from game_object import GameObject
from colorama import Back


class Paddle(GameObject):

    def __init__(self, max_width, max_height):
        super().__init__(max_width, max_height)
        self.x = 0
        self.y = max_height - 1
        self.paddle_length = 5
        self.color = Back.GREEN
        self.change_paddle_size(10)
        self.speed = 2

    def move(self, inp):
        if inp == 'd':
            self.x = min(self.x + self.speed, self.max_width - self.length)
        elif inp == 'a':
            self.x = max(0, self.x - self.speed)

    def change_paddle_size(self, size):
        self.paddle_length = size
        self.set_show(" " * size)
