from game_object import GameObject
from colorama import Back


class Brick(GameObject):

    def set_strength(self, strength):
        self.strength = strength
        if strength == 1:
            self.color = Back.RED
        elif strength == 2:
            self.color = Back.BLUE
        elif strength == 3:
            self.color = Back.CYAN
        elif strength == 4:
            self.color = Back.GREEN

    def __init__(self, max_width: int, max_height: int, strength: int, x: int, y: int, size: int, unbreakable=False):
        super().__init__(max_width, max_height, x, y)
        self.strength = strength
        self.set_show(" " * size)
        self.strength = strength
        self.set_strength(strength)

    def got_hit(self):
        if self.strength == 4:
            return self.strength
        new_strength = self.strength - 1
        self.set_strength(new_strength)
        return new_strength
