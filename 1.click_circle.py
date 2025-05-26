import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Circle Clicker Game")

BG_COLOR = (30, 30, 40)
CIRCLE_COLOR = (70, 190, 220)
TEXT_COLOR = (240, 240, 240)

CIRCLE_RADIUS = 30

font = pygame.font.SysFont("Arial", 28, bold=True)

score = 0

def get_random_pos():
    x = random.randint(CIRCLE_RADIUS, WIDTH - CIRCLE_RADIUS)
    y = random.randint(CIRCLE_RADIUS, HEIGHT - CIRCLE_RADIUS)
    return x, y

circle_pos = get_random_pos()

clock = pygame.time.Clock()

running = True
while running:
    screen.fill(BG_COLOR)

    pygame.draw.circle(screen, CIRCLE_COLOR, circle_pos, CIRCLE_RADIUS)

    score_text = font.render(f"Score: {score}", True, TEXT_COLOR)
    screen.blit(score_text, (10, 10))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = event.pos
            dx = mouse_x - circle_pos[0]
            dy = mouse_y - circle_pos[1]
            dist_squared = dx * dx + dy * dy
            if dist_squared <= CIRCLE_RADIUS * CIRCLE_RADIUS:
                score += 1
                circle_pos = get_random_pos()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
