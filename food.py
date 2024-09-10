import random
import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, GRID_SIZE


class Food:
    def __init__(self):
        self.color = (223, 163, 49)  # Color of the food pixel
        self.randomize_position()  # Directly set the initial position with the method

    def randomize_position(self):
        # Ensures that food doesn't spawn on the boundary
        self.position = (random.randint(0, (SCREEN_WIDTH - GRID_SIZE) // GRID_SIZE) * GRID_SIZE,
                         random.randint(0, (SCREEN_HEIGHT - GRID_SIZE) // GRID_SIZE) * GRID_SIZE)

    def draw(self, surface):
        r = pygame.Rect((self.position[0], self.position[1]), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.color, r)
        pygame.draw.rect(surface, (93, 216, 228), r, 1)
