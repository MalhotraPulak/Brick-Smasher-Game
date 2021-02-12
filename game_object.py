from colorama import Back


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
        self.color = Back.GREEN
        self.set_show("*")

    def get_dim(self):
        return self.x, self.y, self.show, self.color, self.length

    def set_show(self, show):
        self.show = show
        self.length = len(show)

    def get_speed(self):
        return self.speed_x, self.speed_y
