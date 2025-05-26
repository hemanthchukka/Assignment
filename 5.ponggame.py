import pygame
import sys
import random

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Classic Pong")

BG_COLOR = (20, 20, 30)
PADDLE_COLOR = (100, 200, 255)
BALL_COLOR = (255, 255, 255)
SCORE_COLOR = (240, 240, 240)
CENTER_LINE_COLOR = (70, 70, 90)
BUTTON_COLOR = (180, 180, 180)
BUTTON_HOVER = (140, 140, 140)

score_font = pygame.font.SysFont("Consolas", 60)
large_font = pygame.font.SysFont("Consolas", 72)
info_font = pygame.font.SysFont("Consolas", 20)

try:
    sound_paddle = pygame.mixer.Sound('pong_hit.wav')
    sound_score = pygame.mixer.Sound('pong_score.wav')
except Exception:
    sound_paddle = None
    sound_score = None

FPS = 60
clock = pygame.time.Clock()

PADDLE_WIDTH, PADDLE_HEIGHT = 15, 100
PADDLE_SPEED = 7

BALL_SIZE = 20
BALL_START_SPEED = 5
BALL_SPEED_INCREMENT = 0.5
MAX_BALL_SPEED = 12

score_left = 0
score_right = 0
winner = None
game_over = False

left_paddle = pygame.Rect(30, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
right_paddle = pygame.Rect(WIDTH - 30 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)

ball_speed_x = random.choice([-BALL_START_SPEED, BALL_START_SPEED])
ball_speed_y = random.uniform(-3, 3)

def reset_ball(direction):
    global ball_speed_x, ball_speed_y
    ball.center = (WIDTH // 2, HEIGHT // 2)
    ball_speed_x = direction * BALL_START_SPEED
    ball_speed_y = random.uniform(-3, 3)

def reset_game():
    global score_left, score_right, winner, game_over, ball_speed_x, ball_speed_y
    score_left = 0
    score_right = 0
    winner = None
    game_over = False
    left_paddle.y = HEIGHT // 2 - PADDLE_HEIGHT // 2
    right_paddle.y = HEIGHT // 2 - PADDLE_HEIGHT // 2
    reset_ball(random.choice([-1, 1]))

def draw_center_line():
    segment_height = 15
    for y in range(0, HEIGHT, segment_height * 2):
        pygame.draw.rect(screen, CENTER_LINE_COLOR, (WIDTH//2 - 2, y, 4, segment_height))

def draw_scores():
    left_text = score_font.render(str(score_left), True, SCORE_COLOR)
    right_text = score_font.render(str(score_right), True, SCORE_COLOR)
    screen.blit(left_text, (WIDTH // 4 - left_text.get_width() // 2, 20))
    screen.blit(right_text, (WIDTH * 3 // 4 - right_text.get_width() // 2, 20))

def paddle_movement(keys):
    if keys[pygame.K_w] and left_paddle.top > 0:
        left_paddle.y -= PADDLE_SPEED
    if keys[pygame.K_s] and left_paddle.bottom < HEIGHT:
        left_paddle.y += PADDLE_SPEED
    if keys[pygame.K_UP] and right_paddle.top > 0:
        right_paddle.y -= PADDLE_SPEED
    if keys[pygame.K_DOWN] and right_paddle.bottom < HEIGHT:
        right_paddle.y += PADDLE_SPEED

def play_sound(sound):
    if sound:
        sound.play()

def draw_button(text, rect, base_color, hover_color):
    mouse_pos = pygame.mouse.get_pos()
    clicked = False

    if rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, hover_color, rect)
        if pygame.mouse.get_pressed()[0]:
            clicked = True
    else:
        pygame.draw.rect(screen, base_color, rect)

    text_img = info_font.render(text, True, (0, 0, 0))
    screen.blit(text_img, (rect.x + (rect.width - text_img.get_width())//2, rect.y + (rect.height - text_img.get_height())//2))
    return clicked

reset_game()

running = True
while running:
    clock.tick(FPS)
    screen.fill(BG_COLOR)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                reset_game()

    if not game_over:
        keys = pygame.key.get_pressed()
        paddle_movement(keys)

        ball.x += ball_speed_x
        ball.y += ball_speed_y
        if ball.top <= 0 or ball.bottom >= HEIGHT:
            ball_speed_y *= -1

        if ball.colliderect(left_paddle) and ball_speed_x < 0:
            ball_speed_x *= -1
            ball_speed_y += random.uniform(-1, 1)
            ball_speed_x = min(MAX_BALL_SPEED, abs(ball_speed_x) + BALL_SPEED_INCREMENT)
            ball_speed_x = ball_speed_x if ball_speed_x > 0 else -ball_speed_x
            play_sound(sound_paddle)

        if ball.colliderect(right_paddle) and ball_speed_x > 0:
            ball_speed_x *= -1
            ball_speed_y += random.uniform(-1, 1)
            ball_speed_x = -min(MAX_BALL_SPEED, abs(ball_speed_x) + BALL_SPEED_INCREMENT)
            play_sound(sound_paddle)

        if ball.left <= 0:
            score_right += 1
            play_sound(sound_score)
            if score_right >= 10:
                winner = "Player 2"
                game_over = True
            else:
                reset_ball(direction=1)

        if ball.right >= WIDTH:
            score_left += 1
            play_sound(sound_score)
            if score_left >= 10:
                winner = "Player 1"
                game_over = True
            else:
                reset_ball(direction=-1)

        draw_center_line()
        pygame.draw.rect(screen, PADDLE_COLOR, left_paddle)
        pygame.draw.rect(screen, PADDLE_COLOR, right_paddle)
        pygame.draw.ellipse(screen, BALL_COLOR, ball)
        draw_scores()

        info_text = info_font.render("W/S = Left Paddle | UP/DOWN = Right Paddle", True, SCORE_COLOR)
        screen.blit(info_text, (WIDTH // 2 - info_text.get_width() // 2, HEIGHT - 30))

    else:
        win_text = large_font.render(f"{winner} Wins!", True, SCORE_COLOR)
        screen.blit(win_text, (WIDTH//2 - win_text.get_width()//2, HEIGHT//3))

        button_rect = pygame.Rect(WIDTH//2 - 100, HEIGHT//2, 200, 60)
        if draw_button("Replay", button_rect, BUTTON_COLOR, BUTTON_HOVER):
            reset_game()

        instr_text = info_font.render("Press SPACE to Replay", True, SCORE_COLOR)
        screen.blit(instr_text, (WIDTH//2 - instr_text.get_width()//2, HEIGHT//2 + 80))

    pygame.display.flip()
