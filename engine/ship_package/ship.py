from engine.environment.cell_package.cell import Cell


class Ship:
    def __init__(self, size, x, y, rotation):
        self.size = size
        self.hp = size
        self.x = x
        self.y = y
        self.rotation = rotation
        self.set_rotation(rotation)

    def __str__(self):
        return Cell.ship_cell

    def set_position(self, x, y, r):
        self.x = x
        self.y = y
        self.set_rotation(r)

    def set_rotation(self, r):
        self.rotation = r

        if self.rotation == 0:
            self.width = self.size
            self.height = 1
        elif self.rotation == 1:
            self.width = 1
            self.height = self.size
        elif self.rotation == 2:
            self.y = self.y - self.size + 1
            self.width = self.size
            self.height = 1
        elif self.rotation == 3:
            self.x = self.x - self.size + 1
            self.width = 1
            self.height = self.size
