from enum import Enum

from colorama import Back


class Collision(Enum):
    VERTICAL, HORIZONTAL, DIAGONAL, NOPE = range(4)


class GameObject:

    def __init__(self, max_width: int, max_height: int, x: int, y: int):
        self.x = x
        self.y = y
        self.max_height = max_height
        self.max_width = max_width
        self.show = ""
        self.length = 0
        self.speed_x = 0
        self.speed_y = 0
        self.dead = False
        self.color = Back.GREEN
        self.set_show("*")

    def get_dim(self):
        return self.x, self.y, self.show, self.color, self.length

    def set_show(self, show):
        self.show = show
        self.length = len(show)

    def get_speed(self):
        return self.speed_x, self.speed_y


def objects_collision_vh(small: GameObject, big: GameObject):
    small_x, small_y, _, _, small_len = small.get_dim()
    big_x, big_y, _, _, big_len = big.get_dim()

    for i in range(big_len):
        big_part_x = big_x + i
        dist_x = small_x - big_part_x
        dist_y = small_y - big_y
        x_speed, y_speed = small.get_speed()
        dist_x_new = small_x + x_speed - big_part_x
        dist_y_new = small_y + y_speed - big_y
        if dist_x == 0 and abs(dist_y) == 1 and abs(dist_y_new) < abs(dist_y):
            return Collision.VERTICAL
        if dist_y == 0 and abs(dist_x) == 1 and abs(dist_x_new) < abs(dist_x):
            return Collision.HORIZONTAL
    return Collision.NOPE


def objects_collision_d(small: GameObject, big: GameObject):
    small_x, small_y, _, _, small_len = small.get_dim()
    big_x, big_y, _, _, big_len = big.get_dim()
    for i in [0, big_len - 1]:
        big_part_x = big_x + i
        dist_x = small_x - big_part_x
        dist_y = small_y - big_y
        if (i == 0 or i == big_len - 1) and (abs(dist_x) == 1 and abs(dist_y) == 1):
            x_speed, y_speed = small.get_speed()
            dist_x_new = small_x + x_speed - big_part_x
            dist_y_new = small_y + y_speed - big_y
            if abs(dist_x_new) < abs(dist_x) and abs(dist_y_new) < abs(dist_y):
                return Collision.DIAGONAL
    return Collision.NOPE
