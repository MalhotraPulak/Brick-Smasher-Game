import time
import tty
import sys
import select
from game import Game
import os
from enum import Enum
from util import cursor_to_top
import termios
from config import timeout


class State(Enum):
    GAME, MESSAGE, MESSAGE2 = range(0, 3)


old = termios.tcgetattr(sys.stdin.fileno())
tty.setcbreak(sys.stdin)
print("\033[?25l")
HEIGHT, WIDTH = os.popen('stty size', 'r').read().split()
HEIGHT = 25
WIDTH = 75

game = Game(width=WIDTH, height=HEIGHT)
state = State.GAME
score = 0
tim = 0
ch = ' '
os.system('clear')


def show_message(score, time, state):
    cursor_to_top()
    if state == State.MESSAGE2:
        print("You completed the game!!!")
    elif state == State.MESSAGE:
        print("You lost !!!")
    print(f"Score = {score}, Time = {time}")
    print(f"Press q to exit, r to restart")


while True:
    ch = None
    if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
        ch = sys.stdin.read(1)
    if ch == 'q':
        termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, old)
        print("\033[?25h")
        break
    if state == State.GAME:
        game.input(ch)
        ret = game.play()
        if ret[0] == -1:
            os.system("clear")
            state = State.MESSAGE
            score = ret[1]
            tim = ret[2]
        if ret[0] == -2:
            os.system("clear")
            state = State.MESSAGE2
            score = ret[1]
            tim = ret[2]
    elif state == State.MESSAGE or state == State.MESSAGE2:
        if ch == 'r':
            game = Game(width=WIDTH, height=HEIGHT)
            os.system('clear')
            state = State.GAME
        show_message(score, tim, state)
    time.sleep(timeout)
