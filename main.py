import os
import pickle

import neat

from NNdraw import NN
from car import Car
from config_variables import *
import config_variables as cv
from road import Road
from world import World

py.font.init()

bg = py.Surface((WIN_WIDTH, WIN_HEIGHT))
bg.fill(GRAY)


def draw_win(cars, road, world):  # x and y are the coordinates of the best car
    road.draw(world)
    for car in cars:
        car.draw(world)

    text = STAT_FONT.render("Best Car Score: " + str(int(world.get_score())), 1, BLACK)
    world.win.blit(text, (world.win_width - text.get_width() - 10, 10))
    text = STAT_FONT.render("Gen: " + str(cv.GEN - 1), 1, BLACK)
    world.win.blit(text, (world.win_width - text.get_width() - 10, 50))

    if not cv.NO_NN:
        world.bestNN.draw(world)

    py.display.update()
    # blit of the background immediately after the update so if I have
    # draws before draw_win they are not covered by the background
    world.win.blit(bg, (0,
                        0))


def main(genomes=None, config=None):
    nogui = cv.NO_GUI
    if config is None:
        config = []
    if genomes is None:
        genomes = []
    cv.GEN += 1

    nets = []
    ge = []
    cars = []
    t = 0

    world = World(STARTING_POS, WIN_WIDTH, WIN_HEIGHT, nogui)
    if world.win:
        world.win.blit(bg, (0, 0))

    networks = []

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        cars.append(Car(0, 0, 0, nogui))
        g.fitness = 0
        ge.append(g)
        if not cv.NO_NN:
            networks.append(NN(config, g, (90, 210)))

    road = Road(world)
    clock = py.time.Clock()

    running = True
    while running:
        t += 1
        if not nogui:
            clock.tick(FPS)
        world.update_score(0)
        if not nogui:
            for event in py.event.get():
                if event.type == py.QUIT:
                    running = False
                    py.quit()
                    quit()

        (xb, yb) = (0, 0)
        i = 0
        while i < len(cars):
            car = cars[i]

            car_input = car.get_inputs(world, road)
            car_input.append(car.vel / MAX_VEL)
            car.commands = nets[i].activate(tuple(car_input))

            y_old = car.y
            (x, y) = car.move(t)
            # the t is used to avoid eliminating machines in the first few frames
            # (in the first frames getCollision () always returns true)
            if t > 10 and (car.detect_collision(road) or y > world.get_best_car_pos()[
                    1] + BAD_GENOME_THRESHOLD or y > y_old or car.vel < 0.1):
                ge[i].fitness -= 1
                cars.pop(i)
                nets.pop(i)
                ge.pop(i)
                if not cv.NO_NN:
                    networks.pop(i)
            else:
                temp1 = -(y - y_old) / 100
                temp2 = car.vel * SCORE_VEL_MULTIPLIER
                temp = temp1 + temp2
                ge[i].fitness += temp
                if ge[i].fitness > world.get_score():
                    world.update_score(ge[i].fitness)
                    if not cv.NO_NN:
                        world.bestNN = networks[i]
                    world.bestInputs = car_input
                    world.bestCommands = car.commands
                i += 1

            if y < yb:
                (xb, yb) = (x, y)

        if len(cars) == 0:
            running = False

        world.update_best_car_pos((xb, yb))
        road.update(world)
        if not nogui:
            draw_win(cars, road, world)


# NEAT function
def run(config_path):

    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
                                neat.DefaultStagnation, config_path)

    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    gen = p.run(main, 10000)
    with open('best_genome.bin', 'wb') as file:
        pickle.dump(gen, file)


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    path = os.path.join(local_dir, "config_file.txt")
    run(path)
