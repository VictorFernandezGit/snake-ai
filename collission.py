from food import Food


def check_collision(snake, food):
    if snake.positions[0] == food.position:
        snake.length += 1
        snake.score += 1
        food.randomize_position()
    for segment in snake.positions[1:]:
        if segment == snake.positions[0]:
            snake.reset()
