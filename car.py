import os

from pygame import Mask

from road import *
from vector2d import Vector2d


class Car:
    x = 0  # coordinates relative to the global reference system,
    y = 0  # the position on the screen is relative to the position of the best machine

    def __init__(self, x, y, turn, nogui):
        self.nogui = nogui
        self.x = x
        self.y = y
        self.rot = turn
        self.rot = 0
        self.vel = MAX_VEL / 2
        self.acc = 0
        self.img = None
        self.brake_img = None
        if not nogui:
            self.init_imgs()
        self.commands = [0, 0, 0, 0]

    def init_imgs(self):
        img_names = ["yellow_car.png", "red_car.png", "blu_car.png", "green_car.png"]
        random_img_num = int(floor(random() * len(img_names)) % len(img_names))
        name = img_names[random_img_num]  # take one of these images at random

        self.img = py.transform.rotate(
            py.transform.scale(py.image.load(os.path.join("imgs", name)).convert_alpha(), (120, 69)), -90)
        self.brake_img = py.transform.rotate(
            py.transform.scale(py.image.load(os.path.join("imgs", "brakes.png")).convert_alpha(), (120, 69)), -90)

    def detect_collision(self, road):
        # get mask
        if self.nogui:
            mask = Mask(size=(69, 120), fill=True)
        else:
            mask = py.mask.from_surface(self.img)

        (width, height) = mask.get_size()
        for v in [road.pointsLeft, road.pointsRight]:
            for p in v:
                x = p.x - self.x + width / 2
                y = p.y - self.y + height / 2
                try:
                    if mask.get_at((int(x), int(y))):
                        return True
                except IndexError:
                    continue
        return False

    def get_inputs(self, world, road):  # win is used to draw the sensors if DBG = True
        sensors = []
        for k in range(8):
            sensors.append(SENSOR_DISTANCE)
        sensors_equations = get_sensor_equations(self, world, self.nogui)

        for v in [road.pointsLeft, road.pointsRight]:
            i = road.bottomPointIndex
            while v[i].y > self.y - SENSOR_DISTANCE:
                next_index = get_point(i + 1, NUM_POINTS * road.num_ctrl_points)

                get_distance(self, sensors, sensors_equations, v[i], v[next_index])
                i = next_index

        if CAR_DBG and not self.nogui:
            for k, s in enumerate(sensors):
                omega = radians(self.rot + 45 * k)
                dx = s * sin(omega)
                dy = - s * cos(omega)
                # draw sensor intersections
                if s < SENSOR_DISTANCE:
                    py.draw.circle(world.win, RED, world.get_screen_coords(self.x + dx, self.y + dy), 6)

        # convert to value between 0 (distance = max) and 1 (distance = 0)
        for s in range(len(sensors)):
            sensors[s] = 1 - sensors[s] / SENSOR_DISTANCE
        # sensors[0] = 1  # Front
        # sensors[1] = 1  # Front-Right
        # sensors[2] = 1  # Right
        # sensors[3] = 1  # Back-Right
        # sensors[4] = 1  # Back
        # sensors[5] = 1  # Back-Left
        # sensors[6] = 1  # Left
        # sensors[7] = 1  # Front-Left
        return sensors

    def move(self, t):
        self.acc = FRICTION

        if decode_command(self.commands, ACC):
            self.acc = ACC_STRENGTH
        if decode_command(self.commands, BRAKE):
            self.acc = -BRAKE_STRENGTH
        if decode_command(self.commands, TURN_LEFT):
            self.rot -= TURN_VEL
            # self.rot -= TURN_VEL * ((MAX_VEL - self.vel) / MAX_VEL) + TURN_VEL / MAX_VEL
        if decode_command(self.commands, TURN_RIGHT):
            self.rot += TURN_VEL
        if self.vel == 0:
            self.rot = 0
        time_buffer = 500
        if MAX_VEL_REDUCTION == 1 or t >= time_buffer:
            max_vel_local = MAX_VEL
        else:
            ratio = MAX_VEL_REDUCTION + (1 - MAX_VEL_REDUCTION) * (t / time_buffer)
            max_vel_local = MAX_VEL * ratio

        self.vel += self.acc
        if self.vel > max_vel_local:
            self.vel = max_vel_local
        if self.vel < 0:
            self.vel = 0
        self.x = self.x + self.vel * sin(radians(self.rot))
        self.y = self.y - self.vel * cos(radians(self.rot))  # I subtract because the origin is top left

        return self.x, self.y

    def draw(self, world):
        screen_position = world.get_screen_coords(self.x, self.y)
        rotated_img = py.transform.rotate(self.img, -self.rot)
        new_rect = rotated_img.get_rect(center=screen_position)
        if not self.nogui:
            world.win.blit(rotated_img, new_rect.topleft)

        if decode_command(self.commands, BRAKE) and not self.nogui:
            rotated_img = py.transform.rotate(self.brake_img, -self.rot)
            new_rect = rotated_img.get_rect(center=screen_position)
            world.win.blit(rotated_img, new_rect.topleft)

    # ======================== LOCAL FUNCTIONS ==========================


# returns the equations of the lines (in variable y) of the machine
# in order [vertical, increasing diagonal, horizontal, decreasing diagonal]
def get_sensor_equations(self, world, nogui):
    eq = []
    for i in range(4):
        omega = radians(self.rot + 45 * i)
        dx = SENSOR_DISTANCE * sin(omega)
        dy = - SENSOR_DISTANCE * cos(omega)

        if CAR_DBG and not nogui:  # draw sensor lines
            py.draw.lines(world.win, GREEN, False, [world.get_screen_coords(self.x + dx, self.y + dy),
                                                    world.get_screen_coords(self.x - dx, self.y - dy)], 2)

        coef = get_segment_equation(self, Vector2d(x=self.x + dx, y=self.y + dy))
        eq.append(coef)
    return eq


# equations in variable y between two points (taking into account the
# coordinate system with y inverted) in the general form ax + by + c = 0
def get_segment_equation(p, q):

    a = p.y - q.y
    b = q.x - p.x
    c = p.x * q.y - q.x * p.y

    return a, b, c


def get_distance(car, sensors, sensors_equations, p,
                 q):  # given the segment (m, q) I calculate the distance and put it in the corresponding sensor
    (a2, b2, c2) = get_segment_equation(p, q)

    for i, (a1, b1, c1) in enumerate(sensors_equations):
        # get intersection between sensor and segment

        if a1 != a2 or b1 != b2:
            d = b1 * a2 - a1 * b2
            if d == 0:
                continue
            y = (a1 * c2 - c1 * a2) / d
            x = (c1 * b2 - b1 * c2) / d
            if (y - p.y) * (y - q.y) > 0 or (x - p.x) * (
                    x - q.x) > 0:  # if the intersection is not between a and b, go to the next iteration
                continue
        else:  # coincident lines
            (x, y) = (abs(p.x - q.x), abs(p.y - q.y))

        # get distance
        distance = ((car.x - x) ** 2 + (car.y - y) ** 2) ** 0.5

        # insert into the sensor in the right direction
        omega = car.rot + 45 * i  # angle of the sensor line (and its opposite)
        alpha = 90 - degrees(atan2(car.y - y, x - car.x))  # angle to vertical (as car.rot)
        if cos(alpha) * cos(omega) * 100 + sin(alpha) * sin(omega) * 100 > 0:
            index = i
        else:
            index = i + 4

        if distance < sensors[index]:
            sensors[index] = distance


def decode_command(commands, command_type):
    if commands[command_type] > ACTIVATION_THRESHOLD:
        if command_type == ACC and commands[command_type] > commands[BRAKE]:
            return True
        elif command_type == BRAKE and commands[command_type] > commands[ACC]:
            return True
        elif command_type == TURN_LEFT and commands[command_type] > commands[TURN_RIGHT]:
            return True
        elif command_type == TURN_RIGHT and commands[command_type] > commands[TURN_LEFT]:
            return True
    return False

    # ----
