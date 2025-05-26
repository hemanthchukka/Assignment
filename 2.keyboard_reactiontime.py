import pygame
import random
import sys
import time

pygame.init()

WIDTH, HEIGHT = 1080, 720
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Keyboard Reaction Game")

BG_COLOR = (40, 44, 52)
TEXT_COLOR = (220, 220, 220)
HIGHLIGHT_COLOR = (100, 200, 255)
CORRECT_COLOR = (0, 255, 100)
WRONG_COLOR = (255, 60, 60)

FONT_BIG = pygame.font.SysFont('Segoe UI', 120, bold=True)
FONT_MED = pygame.font.SysFont('Segoe UI', 40, bold=True)
FONT_SMALL = pygame.font.SysFont('Segoe UI', 24)

ARROWS = [
    {"symbol": "←", "key": pygame.K_LEFT},
    {"symbol": "↑", "key": pygame.K_UP},
    {"symbol": "→", "key": pygame.K_RIGHT},
    {"symbol": "↓", "key": pygame.K_DOWN},
]

SHOW_DELAY = 1.5

def draw_text(text, font, color, x, y, center=True):
    rendered = font.render(text, True, color)
    rect = rendered.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    SCREEN.blit(rendered, rect)

def main():
    clock = pygame.time.Clock()
    running = True

    current_arrow = None
    waiting_for_key = False
    start_time = 0
    reaction_time = 0
    message = "Press START to begin"
    message_color = TEXT_COLOR

    attempts = 0
    best_time = None

    show_arrow_time = 0

    button_rect = pygame.Rect(WIDTH//2 - 75, HEIGHT - 70, 150, 50)
    button_color = HIGHLIGHT_COLOR
    button_text = "START"

    while running:
        SCREEN.fill(BG_COLOR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            elif event.type == pygame.KEYDOWN:
                if waiting_for_key and current_arrow:
                    if event.key == current_arrow["key"]:
                        reaction_time = time.perf_counter() - start_time
                        attempts += 1
                        if best_time is None or reaction_time < best_time:
                            best_time = reaction_time
                            message = f"🎉 Fastest: {reaction_time*1000:.0f} ms"
                        else:
                            message = f"Good! Reaction time: {reaction_time*1000:.0f} ms"
                        message_color = CORRECT_COLOR
                        waiting_for_key = False
                        show_arrow_time = time.perf_counter() + SHOW_DELAY
                    elif event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]:
                        message = "❌ Wrong key! Try again."
                        message_color = WRONG_COLOR
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and button_rect.collidepoint(event.pos):
                    current_arrow = None
                    waiting_for_key = False
                    message = "Get ready..."
                    message_color = TEXT_COLOR
                    attempts = 0
                    best_time = None
                    reaction_time = 0
                    pygame.time.set_timer(pygame.USEREVENT, int(SHOW_DELAY*1000))
            elif event.type == pygame.USEREVENT:
                pygame.time.set_timer(pygame.USEREVENT, 0)
                current_arrow = random.choice(ARROWS)
                waiting_for_key = True
                start_time = time.perf_counter()
                message = "Press the arrow key shown!"
                message_color = TEXT_COLOR

        if current_arrow and waiting_for_key:
            draw_text(current_arrow["symbol"], FONT_BIG, HIGHLIGHT_COLOR, WIDTH//2, HEIGHT//2)
        else:
            draw_text("?", FONT_BIG, (100, 100, 100), WIDTH//2, HEIGHT//2)

        draw_text(message, FONT_MED, message_color, WIDTH//2, HEIGHT//2 + 100)
        draw_text(f"Attempts: {attempts}", FONT_SMALL, TEXT_COLOR, 20, 20, center=False)
        best_time_disp = f"{best_time*1000:.0f} ms" if best_time is not None else "-"
        draw_text(f"Best Time: {best_time_disp}", FONT_SMALL, TEXT_COLOR, 20, 50, center=False)
        pygame.draw.rect(SCREEN, button_color, button_rect, border_radius=12)
        draw_text(button_text, FONT_MED, (30, 30, 30), button_rect.centerx, button_rect.centery)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
