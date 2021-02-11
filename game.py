import os
from paddle import Paddle
from screen import Screen


def cursor_to_top():
    print("\033[0;0H")


class Game:
    def __init__(self, width, height):
        self.paddle = Paddle(width, height)
        self.screen = Screen(width, height)
        self.height = height
        self.width = width
        os.system('clear')

    def input(self, inp):
        self.paddle.move(inp)

    def play(self):
        self.screen.set_sprites(paddle=self.paddle)
        cursor_to_top()
        self.screen.render()


