import pygame
import random
import sys


pygame.init()


WIDTH, HEIGHT = 1080, 800
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Color Catch Game")


WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
GRAY = (100, 100, 100)
PINK = (255, 192, 203)

COLORS = {
    "red": (220, 50, 50),
    "green": (50, 200, 70),
    "blue": (70, 140, 220),
    "yellow": (230, 220, 80),
    "purple": (150, 70, 200),
}

COLOR_NAMES = list(COLORS.keys())

FONT_BIG = pygame.font.SysFont('Segoe UI', 48, bold=True)
FONT_MED = pygame.font.SysFont('Segoe UI', 32)
FONT_SMALL = pygame.font.SysFont('Segoe UI', 24)

BUCKET_WIDTH, BUCKET_HEIGHT = 120, 30
BUCKET_SPEED = 15

BLOCK_SIZE = 40
FALL_SPEED_START = 3
FALL_SPEED_INCREMENT = 0.2

clock = pygame.time.Clock()

class Block:
    def __init__(self, color_name):
        self.color_name = color_name
        self.color = COLORS[color_name]
        self.x = random.randint(0, WIDTH - BLOCK_SIZE)
        self.y = -BLOCK_SIZE
        self.speed = FALL_SPEED_START + random.random() * 1.5

    def move(self):
        self.y += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(screen, BLACK, (self.x, self.y, BLOCK_SIZE, BLOCK_SIZE), 2)

    def off_screen(self):
        return self.y > HEIGHT

    def get_rect(self):
        return pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)


def draw_bucket(screen, x):
    bucket_rect = pygame.Rect(x, HEIGHT - BUCKET_HEIGHT - 10, BUCKET_WIDTH, BUCKET_HEIGHT)
    pygame.draw.rect(screen, PINK, bucket_rect)
    pygame.draw.rect(screen, BLACK, bucket_rect, 3)
    return bucket_rect

def main():
    running = True

    bucket_x = WIDTH // 2 - BUCKET_WIDTH // 2
    blocks = []
    spawn_timer = 0
    spawn_interval = 700  

    target_color_name = random.choice(COLOR_NAMES)
    score = 0
    fall_speed = FALL_SPEED_START

    message = ""

    while running:
        dt = clock.tick(60)
        spawn_timer += dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            bucket_x -= BUCKET_SPEED
        if keys[pygame.K_RIGHT]:
            bucket_x += BUCKET_SPEED

        bucket_x = max(0, min(WIDTH - BUCKET_WIDTH, bucket_x))

        if spawn_timer >= spawn_interval:
            spawn_timer = 0
            color_name = random.choice(COLOR_NAMES)
            new_block = Block(color_name)

            new_block.speed = fall_speed + random.random() * 1.5
            blocks.append(new_block)

            if score > 0 and score % 5 == 0:
                fall_speed += FALL_SPEED_INCREMENT
                spawn_interval = max(300, spawn_interval - 20)

        for block in blocks:
            block.move()

        bucket_rect = pygame.Rect(bucket_x, HEIGHT - BUCKET_HEIGHT - 10, BUCKET_WIDTH, BUCKET_HEIGHT)

        caught_blocks = []
        for block in blocks:
            if block.get_rect().colliderect(bucket_rect) and block.y + BLOCK_SIZE >= HEIGHT - BUCKET_HEIGHT - 10:
                caught_blocks.append(block)

        for block in caught_blocks:
            blocks.remove(block)
            if block.color_name == target_color_name:
                score += 1
                message = "Correct! +1 point"

                if score % 5 == 0:

                    available_colors = [c for c in COLOR_NAMES if c != target_color_name]
                    target_color_name = random.choice(available_colors)
                    message = "Target color changed!"
            else:
                score = max(0, score - 1)
                message = "Wrong color! -1 point"

        blocks = [b for b in blocks if not b.off_screen()]

        SCREEN.fill(WHITE)

        draw_text = FONT_BIG.render("Catch:", True, BLACK)
        SCREEN.blit(draw_text, (20, 20))
        pygame.draw.rect(SCREEN, COLORS[target_color_name], (180, 20, 60, 60))
        pygame.draw.rect(SCREEN, BLACK, (180, 20, 60, 60), 3)

        score_text = FONT_MED.render(f"Score: {score}", True, BLACK)
        SCREEN.blit(score_text, (WIDTH - 180, 30))

        msg_text = FONT_SMALL.render(message, True, BLACK)
        SCREEN.blit(msg_text, (WIDTH - 180, 70))

        for block in blocks:
            block.draw(SCREEN)

        draw_bucket(SCREEN, bucket_x)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
