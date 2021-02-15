import time
import tty
import sys
import select
from game import Game
import os
from enum import Enum
from util import show_message
import termios
from config import timeout


class State(Enum):
    GAME, MESSAGE = range(0, 2)


old = termios.tcgetattr(sys.stdin.fileno())
tty.setcbreak(sys.stdin)

HEIGHT, WIDTH = os.popen('stty size', 'r').read().split()
HEIGHT = int(HEIGHT) - 5
WIDTH = int(WIDTH) - 4

game = Game(width=WIDTH, height=HEIGHT)
state = State.GAME
score = 0
tim = 0
ch = ' '
os.system('clear')

while True:
    ch = None
    if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
        ch = sys.stdin.read(1)
    if ch == 'q':
        termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, old)
        break
    if state == State.GAME:
        game.input(ch)
        ret = game.play()
        if ret[0] == -1:
            state = State.MESSAGE
            score = ret[1]
            tim = ret[2]
    elif state == State.MESSAGE:
        if ch == 'r':
            game = Game(width=WIDTH, height=HEIGHT)
            os.system('clear')
            state = State.GAME
        show_message(score, tim)
    time.sleep(timeout)
