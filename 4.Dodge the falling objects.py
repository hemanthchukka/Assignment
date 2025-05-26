import pygame
import random

pygame.init()

WIDTH, HEIGHT = 1080, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dodge the Falling Objects")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (50, 50, 50)
player_width, player_height = 60, 60
player_speed = 10

obj_width, obj_height = 50, 50
obj_spawn_delay = 800  
speed_increase_interval = 5000
max_lives = 5

font = pygame.font.SysFont(None, 36)
large_font = pygame.font.SysFont(None, 72)

player_img = pygame.image.load("C:/Users/chukk/OneDrive/Desktop/Assignment/jet.png")
player_img = pygame.transform.scale(player_img, (player_width, player_height))

obj_img = pygame.image.load("C:/Users/chukk/OneDrive/Desktop/Assignment/bullet.png")
obj_img = pygame.transform.scale(obj_img, (obj_width, obj_height))

clock = pygame.time.Clock()
FPS = 60

def draw_text(text, color, x, y, font_obj=font):
    img = font_obj.render(text, True, color)
    screen.blit(img, (x, y))

def reset_game():
    global lives, obj_list, obj_speed, player_x, game_over
    lives = max_lives
    obj_list.clear()
    obj_speed = 5
    player_x = WIDTH // 2 - player_width // 2
    game_over = False

def draw_button(text, rect, base_color, hover_color):
    mouse_pos = pygame.mouse.get_pos()
    clicked = False

    if rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, hover_color, rect)
        if pygame.mouse.get_pressed()[0]:
            clicked = True
    else:
        pygame.draw.rect(screen, base_color, rect)

    draw_text(text, WHITE, rect.x + 20, rect.y + 10)
    return clicked

player_x = WIDTH // 2 - player_width // 2
obj_list = []
last_spawn_time = pygame.time.get_ticks()
last_speed_increase = pygame.time.get_ticks()
obj_speed = 5
lives = max_lives
game_over = False

running = True
while running:
    clock.tick(FPS)
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                reset_game()

    if not game_over:

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_x -= player_speed
            if player_x < 0:
                player_x = 0
        if keys[pygame.K_RIGHT]:
            player_x += player_speed
            if player_x > WIDTH - player_width:
                player_x = WIDTH - player_width

        current_time = pygame.time.get_ticks()
        if current_time - last_spawn_time > obj_spawn_delay:
            obj_x = random.randint(0, WIDTH - obj_width)
            obj_list.append(pygame.Rect(obj_x, 0, obj_width, obj_height))
            last_spawn_time = current_time

        if current_time - last_speed_increase > speed_increase_interval:
            obj_speed += 0.5
            last_speed_increase = current_time

        player_rect = pygame.Rect(player_x, HEIGHT - player_height - 10, player_width, player_height)
        for obj in obj_list[:]:
            obj.y += obj_speed
            if obj.colliderect(player_rect):
                lives -= 1
                obj_list.remove(obj)
                if lives <= 0:
                    game_over = True
            elif obj.y > HEIGHT:
                obj_list.remove(obj)

        screen.blit(player_img, player_rect.topleft)

        for obj in obj_list:
            screen.blit(obj_img, obj.topleft)

        draw_text(f"Lives: {lives}", WHITE, 10, 15)

    else:
        draw_text("GAME OVER", RED, WIDTH//2 - 150, HEIGHT//3, large_font)

        button_rect = pygame.Rect(WIDTH//2 - 100, HEIGHT//2, 200, 60)
        if draw_button("Replay", button_rect, GRAY, DARK_GRAY):
            reset_game()

        draw_text("Press SPACE to Replay", WHITE, WIDTH//2 - 140, HEIGHT//2 + 80)

    pygame.display.flip()

pygame.quit()
