from brick import Brick
from config import BRICK_SIZE
from game_object import GameObject
import time


class UFO(GameObject):
    def __init__(self, max_width: int, max_height: int, x: int, y: int):
        super().__init__(max_width, max_height, x, y)
        self.health = 10
        self.speed_x = 1
        self.x_start = 100
        self.x_end = 0
        self.bricks = []
        self.last_bomb = time.time()

    def art_to_bricks(self):
        brick_art = ""
        x = 0
        y = 0
        bricks = []
        art = \
            """
                         _,--=--._
                       ,'    _    `.
                      -    _(_)_o   -
                 ____'    /_  _/]    `____
          -=====::(+):::::::::::::::::(+)::=====-
                   (+).-------------,(+)
                       . -  -  -  - ,
                         `  -=-  '
        """
        for char in art:
            if char == "\n":
                brick_art += (6 - len(brick_art)) * " "
            else:
                brick_art += char
            # print(f"**{brick_art}**")
            if len(brick_art) == 6:
                if brick_art.count(" ") != 6:
                    # print(f"({x}, {y}), art={brick_art}")
                    self.x_start = min(self.x_start, x * BRICK_SIZE)
                    self.x_end = max(self.x_end, x * BRICK_SIZE + BRICK_SIZE)
                    bricks.append(
                        Brick(self.max_width, self.max_height, strength=10, x=x * BRICK_SIZE, y=y, ascii=brick_art,
                              size=BRICK_SIZE, ufo=True))
                brick_art = ""
                x += 1
            if char == "\n":
                y += 1
                x = 0
        self.bricks = bricks
        return bricks

    def move(self, paddle_center):
        current_center = (self.x_start + self.x_end) / 2
        if current_center < paddle_center:
            self.speed_x = 1
        else:
            self.speed_x = -1

        new_x_start = self.x_start + self.speed_x
        new_x_end = self.x_end + self.speed_x

        if new_x_start >= 0 and new_x_end < self.max_width:
            self.x_end = new_x_end
            self.x_start = new_x_start
            for idx, _ in enumerate(self.bricks):
                self.bricks[idx].x += self.speed_x

    def bombTime(self):
        return time.time() - self.last_bomb > 2

    def spawn_defense(self, j):
        bricks = []
        for x in range(int(self.max_width / BRICK_SIZE)):
            bricks.append(Brick(self.max_width, self.max_height, x=x * BRICK_SIZE, y=11 + j, strength=1, size=BRICK_SIZE))
        return bricks
