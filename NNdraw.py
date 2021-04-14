from node import *

py.font.init()


class NN:

    def __init__(self, config, genome, pos):
        self.input_nodes = []
        self.output_nodes = []
        self.nodes = []
        self.genome = genome
        self.pos = (int(pos[0] + NODE_RADIUS), int(pos[1]))
        input_names = ["Sensor F", "Sensor FR", "Sensor R", "Sensor BR", "Sensor B", "Sensor BL", "Sensor L",
                       "Sensor FL", "Speed"]
        output_names = ["Accelerate", "Brake", "Turn Left", "Turn Right"]
        middle_nodes = [n for n in genome.nodes.keys()]
        node_id_list = []

        # nodes
        h = (INPUT_NEURONS - 1) * (NODE_RADIUS * 2 + NODE_SPACING)
        for i, input_line in enumerate(config.genome_config.input_keys):
            n = Node(input_line, pos[0], pos[1] + int(-h / 2 + i * (NODE_RADIUS * 2 + NODE_SPACING)), INPUT,
                     [GREEN_PALE, GREEN, DARK_GREEN_PALE, DARK_GREEN], input_names[i], i)
            self.nodes.append(n)
            node_id_list.append(input_line)

        h = (OUTPUT_NEURONS - 1) * (NODE_RADIUS * 2 + NODE_SPACING)
        for i, out in enumerate(config.genome_config.output_keys):
            n = Node(out + INPUT_NEURONS, pos[0] + 2 * (LAYER_SPACING + 2 * NODE_RADIUS),
                     pos[1] + int(-h / 2 + i * (NODE_RADIUS * 2 + NODE_SPACING)), OUTPUT,
                     [RED_PALE, RED, DARK_RED_PALE, DARK_RED], output_names[i], i)
            self.nodes.append(n)
            middle_nodes.remove(out)
            node_id_list.append(out)

        h = (len(middle_nodes) - 1) * (NODE_RADIUS * 2 + NODE_SPACING)
        for i, m in enumerate(middle_nodes):
            n = Node(m, self.pos[0] + (LAYER_SPACING + 2 * NODE_RADIUS),
                     self.pos[1] + int(-h / 2 + i * (NODE_RADIUS * 2 + NODE_SPACING)), MIDDLE,
                     [BLUE_PALE, DARK_BLUE, BLUE_PALE, DARK_BLUE])
            self.nodes.append(n)
            node_id_list.append(m)

        # connections
        self.connections = []
        for c in genome.connections.values():
            if c.enabled:
                input_line, output = c.key
                self.connections.append(
                    Connection(
                        self.nodes[node_id_list.index(input_line)],
                        self.nodes[node_id_list.index(output)],
                        c.weight)
                )

    def draw(self, world):
        for c in self.connections:
            c.draw_connection(world)
        for node in self.nodes:
            node.draw_node(world)

# ----
