import sys
import pygame
from settings import INITIAL_SPEED, SCREEN_WIDTH, SCREEN_HEIGHT


def draw_score(surface, score):
    font = pygame.font.SysFont('Arial', 36)
    score_text = font.render('Score: {0}'.format(score), True, (255, 255, 255))
    surface.blit(score_text, (5, 10))


def show_game_over(surface):
    font = pygame.font.SysFont('Arial', 48)
    game_over_text = font.render('Game Over', True, (255, 255, 255))
    surface.blit(game_over_text, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 3))
    restart_text = font.render('Press Space to Restart', True, (255, 255, 255))
    surface.blit(restart_text, (SCREEN_WIDTH // 6, SCREEN_HEIGHT // 2))
    pygame.display.update()
    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                # This needs to reset the game properly, likely needs rethinking
                waiting_for_input = False
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

def adjust_speed(score):
    if score < 10:
        return 10
    elif score < 20:
        return 15
    else:
        return 20
