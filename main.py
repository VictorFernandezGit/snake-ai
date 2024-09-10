# main.py
import pygame

from settings import SCREEN_WIDTH, SCREEN_HEIGHT
from snake import Snake
from food import Food
from utilities import draw_score, show_game_over, adjust_speed
from collission import check_collision


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    snake = Snake()
    food = Food()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        snake.handle_keys()
        snake.move()
        if snake.get_head_position() == food.position:
            snake.length += 1
            snake.score += 1
            food.randomize_position()

        screen.fill((0, 0, 0))
        snake.draw(screen)
        food.draw(screen)
        draw_score(screen, snake.score)
        pygame.display.update()

        # Adjust speed based on the score
        clock.tick(adjust_speed(snake.score))
        snake.handle_keys()

        # Check collision
        check_collision(snake, food)


if __name__ == '__main__':
    main()
