import pygame as py


class World:

    initialPos = (0, 0)
    bestCarPos = (0, 0)

    def __init__(self, starting_pos, world_width, world_height, nogui):
        self.nogui = nogui
        self.initialPos = starting_pos
        self.bestCarPos = (0, 0)
        self.win = py.display.set_mode((world_width, world_height)) if not nogui else None
        self.win_width = world_width
        self.win_height = world_height
        self.score = 0
        self.bestGenome = None
        self.bestNN = None

    def update_best_car_pos(self, pos):
        self.bestCarPos = pos

    def get_screen_coords(self, x, y):
        return int(x + self.initialPos[0] - self.bestCarPos[0]), int(y + self.initialPos[1] - self.bestCarPos[1])

    def get_best_car_pos(self):
        return self.bestCarPos

    def update_score(self, new_score):
        self.score = new_score

    def get_score(self):
        return self.score
