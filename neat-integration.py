import os
import neat
import pygame
from neat import genome
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, GRID_SIZE
from food import Food
from snake import Snake
from utilities import adjust_speed, draw_score
from collission import check_collision

"""
NEAT config currently needs to be implemented
"""
def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        game_loop(net)


def game_loop(net):
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    snake = Snake()
    food = Food()

    while True:
        inputs = check_collision(snake, food)
        output = net.activate(inputs)

        # Example assuming output is [turn_left, go_straight, turn_right]
        decision = output.index(max(output))
        # need to set control inputs
        if decision == 0:
            snake.turn_left()
        elif decision == 1:
            snake.go_straight()
        elif decision == 2:
            snake.turn_right()

        snake.move()
        if snake.get_head_position() == food.position:
            snake.length += 1
            snake.score += 1
            food.randomize_position()
            genome.fitness += 10  # Increase fitness for eating food

        if check_collision(snake):  # This needs to be implemented
            genome.fitness -= 10  # Decrease fitness for hitting walls or itself
            break

        screen.fill((0, 0, 0))
        snake.draw(screen)
        food.draw(screen)
        draw_score(screen, snake.score)
        pygame.display.update()

        clock.tick(adjust_speed(snake.score))


def run_neat():
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    winner = p.run(eval_genomes, 50)


if __name__ == '__main__':
    run_neat()
