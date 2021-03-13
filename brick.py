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
        elif strength == 10:
            self.color = Back.LIGHTBLACK_EX

    def __init__(self, max_width: int, max_height: int, strength: int, x: int, y: int, size: int, ufo=False, ascii=""):
        super().__init__(max_width, max_height, x, y)
        self.strength = strength
        self.ufo = ufo
        if not ufo:
            self.set_show("▏" + " " * (size - 2) + "▕")
        else:
            self.set_show(ascii)
            self.set_strength(10)
        self.changeColor = False
        if strength == 5:
            self.changeColor = True
            strength = 1
        self.strength = strength
        self.set_strength(strength)

    def change(self):
        if self.changeColor:
            self.set_strength((self.strength + 1) % 4 + 1)

    def got_hit(self):
        if self.changeColor:
            self.changeColor = False
            return self.strength
        if self.strength == 4 or self.strength == 10:
            return self.strength
        new_strength = self.strength - 1
        self.set_strength(new_strength)
        return new_strength
