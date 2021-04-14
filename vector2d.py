class Vector2d:
    def __init__(self, x=-1, y=-1, angle=0):
        self.x = x
        self.y = y
        self.angle = angle

    def co(self, x, y):
        self.x = x
        self.y = y

    def get_co(self):
        return self.x, self.y
