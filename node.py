from car import decode_command
from config_variables import *


class Node:
    def __init__(self, node_id, x, y, node_type, color, label="", index=0):
        self.id = node_id
        self.x = x
        self.y = y
        self.type = node_type
        self.color = color
        self.label = label
        self.index = index

    def draw_node(self, world):

        color_scheme = self.get_node_colors(world)

        py.draw.circle(world.win, color_scheme[0], (self.x, self.y), NODE_RADIUS)
        py.draw.circle(world.win, color_scheme[1], (self.x, self.y), NODE_RADIUS - 2)

        # draw labels
        if self.type != MIDDLE:
            text = NODE_FONT.render(self.label, 1, BLACK)
            world.win.blit(text, (
                self.x + (self.type - 1) * ((text.get_width() if not self.type else 0) + NODE_RADIUS + 5),
                self.y - text.get_height() / 2))

    def get_node_colors(self, world):

        if self.type == INPUT:
            ratio = world.bestInputs[self.index]
        elif self.type == OUTPUT:
            ratio = 1 if decode_command(world.bestCommands, self.index) else 0
        else:
            ratio = 0

        col = [[0, 0, 0], [0, 0, 0]]
        for i in range(3):
            col[0][i] = int(ratio * (self.color[1][i] - self.color[3][i]) + self.color[3][i])
            col[1][i] = int(ratio * (self.color[0][i] - self.color[2][i]) + self.color[2][i])
        return col


class Connection:
    def __init__(self, input_node, output, wt):
        self.input = input_node
        self.output = output
        self.wt = wt

    def draw_connection(self, world):
        color = GREEN if self.wt >= 0 else RED
        width = int(abs(self.wt * CONNECTION_WIDTH))
        py.draw.line(world.win, color, (self.input.x + NODE_RADIUS, self.input.y),
                     (self.output.x - NODE_RADIUS, self.output.y), width)
