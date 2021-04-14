from config_variables import *
import pygame as py
import numpy as np
from scipy import interpolate
from math import *
from vector2d import *
from random import random, seed


class Road:
    def __init__(self, world):
        self.num_ctrl_points = int((world.win_height + SAFE_SPACE) / SPACING) + 2
        seed(ROAD_SEED)
        self.last_ctrl_point = 0
        self.ctrl_points = []
        self.centerPoints = []
        self.pointsLeft = []
        self.pointsRight = []

        for i in range(self.num_ctrl_points):
            self.ctrl_points.append(Vector2d())

        for i in range(NUM_POINTS * self.num_ctrl_points):  # fill in the pointsLeft and pointsRight vectors
            self.pointsLeft.append(Vector2d(1000, 1000))
            self.pointsRight.append(Vector2d(1000, 1000))
            self.centerPoints.append(Vector2d(1000, 1000))

        self.ctrl_points[0].co(0, SPACING)  # initializes the first two control_points to be straight
        self.ctrl_points[1].co(0, 0)
        for i in range(NUM_POINTS):
            x = self.ctrl_points[0].x
            y = self.ctrl_points[0].y - SPACING / NUM_POINTS * i
            self.centerPoints[i].co(x, y)
            self.pointsLeft[i].co(x - ROAD_WIDTH / 2, y)
            self.pointsRight[i].co(x + ROAD_WIDTH / 2, y)
        self.next_point = NUM_POINTS

        for i in range(self.num_ctrl_points - 2):
            self.create_segment(i + 1)

        self.last_ctrl_point = self.num_ctrl_points - 1
        self.bottomPointIndex = 0

    def calc_borders(self, i):
        prev_index = get_point(i - 1, self.num_ctrl_points * NUM_POINTS)
        center = self.centerPoints[i]
        prev = self.centerPoints[prev_index]
        angle = atan2(center.x - prev.x, prev.y - center.y)

        x = ROAD_WIDTH / 2 * cos(angle)
        y = ROAD_WIDTH / 2 * sin(angle)
        self.pointsLeft[i].x = center.x - x
        self.pointsLeft[i].y = center.y - y if not center.y - y >= self.pointsLeft[prev_index].y else self.pointsLeft[
            prev_index].y
        self.pointsRight[i].x = center.x + x
        self.pointsRight[i].y = center.y + y if not center.y + y >= self.pointsRight[prev_index].y else \
            self.pointsRight[prev_index].y

    def create_segment(self, index):
        p1 = self.ctrl_points[get_point(index, self.num_ctrl_points)]
        p2 = self.ctrl_points[get_point(index + 1, self.num_ctrl_points)]

        # define p2
        # seed(1)
        p2.co(p1.x + (random() - 0.5) * MAX_DEVIATION, p1.y - SPACING)
        p2.angle = MAX_ANGLE * (random() - 0.5)

        y_tmp = []
        for i in range(NUM_POINTS):
            y_tmp.append(p2.y + SPACING / NUM_POINTS * i)

        # get cubic spline of the center line of the road
        ny = np.array([p2.y, p1.y])  # inverted because scipy wants the x increasing (in this case the y)
        nx = np.array([p2.x, p1.x])
        cs = interpolate.CubicSpline(ny, nx, axis=0, bc_type=((1, p2.angle), (1, p1.angle)))
        res = cs(y_tmp)

        # create the actual borders
        for i in range(NUM_POINTS):
            self.centerPoints[self.next_point].x = res[NUM_POINTS - i - 1]
            self.centerPoints[self.next_point].y = y_tmp[NUM_POINTS - i - 1]
            self.calc_borders(self.next_point)

            self.next_point = get_point(self.next_point + 1, NUM_POINTS * self.num_ctrl_points)

        self.last_ctrl_point = get_point(self.last_ctrl_point + 1, self.num_ctrl_points)
        self.bottomPointIndex = self.next_point

    def update(self, world):
        if world.get_screen_coords(0, self.ctrl_points[self.last_ctrl_point].y)[1] > -SAFE_SPACE:
            self.create_segment(self.last_ctrl_point)

    def draw(self, world):
        def _draw_lines(point, next_point):
            p = point
            f = next_point
            if p.y >= f.y:
                py.draw.line(world.win, BLACK, world.get_screen_coords(p.x, p.y), world.get_screen_coords(f.x, f.y), 4)
        # draw control_points
        if ROAD_DBG:
            # for p in self.ctrl_points:     #EEEEEEEEEEEEEEEEE
            # py.draw.circle(win, BLUE, (int(p.x), int(p.y)), 4)
            for i in range(len(self.pointsLeft)):
                py.draw.circle(
                    world.win,
                    BLUE,
                    world.get_screen_coords(self.pointsLeft[i].x, self.pointsLeft[i].y),
                    2
                )
                py.draw.circle(
                    world.win,
                    BLUE,
                    world.get_screen_coords(self.pointsRight[i].x, self.pointsRight[i].y),
                    2
                )
        else:
            # draw borders
            for i in range(len(self.pointsLeft)):
                next_index = get_point(i + 1, NUM_POINTS * self.num_ctrl_points)

                _draw_lines(self.pointsLeft[i], self.pointsLeft[next_index])
                _draw_lines(self.pointsRight[i], self.pointsRight[next_index])


def get_point(i, cap):
    return (i + cap) % cap

    # -----------------
