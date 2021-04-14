import os
import pickle
import neat

from main import main


def run():
    gen = None
    try:
        with open('best_genome.bin', 'rb') as file:
            gen = [(1, pickle.load(file))]
    except IOError:
        return
    local_dir = os.path.dirname(__file__)
    path = os.path.join(local_dir, "config_file.txt")
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
                                neat.DefaultStagnation, path)

    if gen:
        main(gen, config)


if __name__ == '__main__':
    run()
