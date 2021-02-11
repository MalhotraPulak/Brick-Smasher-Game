import time
import tty
import sys
from game import Game
from input import nonBlockingRawInput
import os
tty.setcbreak(sys.stdin)

timeout = 1/60

HEIGHT, WIDTH = os.popen('stty size', 'r').read().split()


game = Game(width=int(WIDTH) - 4, height=int(HEIGHT) - 5)

while True:
    ch = nonBlockingRawInput(timeout)
    if ch == 'q':
        break
    game.input(ch)
    game.play()
    time.sleep(timeout)

