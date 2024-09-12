import os
import neat
import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, GRID_SIZE
from food import Food
from snake import Snake
from utilities import adjust_speed, draw_score
from collission import check_collision

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


class Snake():
    def __init__(self):
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = DOWN
        self.color = (0, 255, 0)
        self.score = 0

    def turn_left(self):
        x, y = self.direction
        self.direction = (-y, x)

    def turn_right(self):
        x, y = self.direction
        self.direction = (y, -x)

    def go_straight(self):
        pass

    def move(self):
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction
        new_head = (head_x + dx * GRID_SIZE, head_y + dy * GRID_SIZE)
        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.positions.pop()

    def get_head_position(self):
        return self.positions[0]

    def draw(self, surface):
        for p in self.positions:
            r = pygame.Rect((p[0], p[1]), (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, self.color, r)


def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        genome.fitness = 0
        fitness = game_loop(genome, net)
        genome.fitness = fitness


def game_loop(genome, net):
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    snake = Snake()
    food = Food()

    frame_limit = 500
    frames = 0

    while frames < frame_limit:
        frames += 1

        # Get inputs for neural network
        inputs = get_inputs(snake, food)
        output = net.activate(inputs)

        # Network output controls snake
        decision = output.index(max(output))
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

        if check_collision(snake):
            break

        screen.fill((0, 0, 0))
        snake.draw(screen)
        food.draw(screen)
        draw_score(screen, snake.score)

        pygame.display.update()
        clock.tick(adjust_speed(snake.score))

    return snake.score


def run_neat():
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    # Load NEAT configuration
    try:
        config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                             neat.DefaultSpeciesSet, neat.DefaultStagnation,
                             config_path)
    except Exception as e:
        print(f"Error loading NEAT config: {e}")
        return

    # Create the population
    try:
        p = neat.Population(config)
        p.add_reporter(neat.StdOutReporter(True))

        winner = p.run(eval_genomes, 50)
        print("NEAT run completed. Winner:", winner)
    except Exception as e:
        print("An error occurred during NEAT setup or execution:", e)


def get_inputs(snake, food):
    head_x, head_y = snake.get_head_position()
    food_x, food_y = food.position

    dist_x = (food_x - head_x) / SCREEN_WIDTH
    dist_y = (food_y - head_y) / SCREEN_HEIGHT

    inputs = [
        dist_x,
        dist_y,
        snake.direction[0],
        snake.direction[1],
    ]

    return inputs


if __name__ == '__main__':
    run_neat()
