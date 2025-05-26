import pygame
import time
import random
import os
import sys

# Initialize Pygame
pygame.init()

# Define colors
white = (255, 255, 255)
green = (0, 255, 0)
red = (213, 50, 80)
black = (0, 0, 0)

# Display dimensions
dis_width, dis_height = 800, 600
snake_block = 20
snake_speed = 9

# Create game window
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game')
clock = pygame.time.Clock()

# Fonts
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

# Asset directory
ASSET_DIR = "C:\\Users\\chukk\\OneDrive\\Desktop\\snake.py"

# Asset paths
snake_img_path = os.path.join(ASSET_DIR, "snake (2).png")
apple_img_path = os.path.join(ASSET_DIR, "apple.png")
background_img_path = os.path.join(ASSET_DIR, "background.png")
snake_head_img_path = os.path.join(ASSET_DIR, "head.png")

# Image loading helper
def load_image(path, fallback_color=None, size=None):
    try:
        image = pygame.image.load(path).convert_alpha()
        if size:
            image = pygame.transform.scale(image, size)
        return image
    except (pygame.error, FileNotFoundError) as e:
        print(f"Error loading image {path}: {e}")
        if fallback_color:
            surface = pygame.Surface(size if size else (snake_block, snake_block))
            surface.fill(fallback_color)
            return surface
        return None

# Load images
snake_img = load_image(snake_img_path, fallback_color=green, size=(40, 40))
apple_img = load_image(apple_img_path, fallback_color=red, size=(snake_block, snake_block))
background_img = load_image(background_img_path, size=(dis_width, dis_height))
snake_head_img_original = load_image(snake_head_img_path, fallback_color=green, size=(snake_block, snake_block))

# Load sounds
try:
    coin_sound = pygame.mixer.Sound(r"C:\Users\chukk\OneDrive\Desktop\snake.py\coin.wav")
    lose_sound = pygame.mixer.Sound(r"C:\Users\chukk\OneDrive\Desktop\snake.py\lose.wav")
except pygame.error as e:
    print(f"Error loading sound files: {e}")
    coin_sound = lose_sound = None

# Score display
def your_score(score):
    score_text = score_font.render("Score: " + str(score), True, white)
    dis.blit(score_text, (dis_width - score_text.get_width() - 10, 10))

# Header (title + icon)
def draw_header():
    text = font_style.render("Snake Game", True, white)
    dis.blit(text, (10, 10))
    if snake_img:
        dis.blit(snake_img, (10 + text.get_width() + 10, 5))

# Draw snake with last segment as head
def our_snake(snake_list, direction):
    if snake_list:
        head = snake_list[-1]  # Last is visual head
        angle = {'RIGHT': 0, 'LEFT': 180, 'UP': 90, 'DOWN': 270}.get(direction, 0)
        if snake_head_img_original:
            rotated_head = pygame.transform.rotate(snake_head_img_original, angle)
            dis.blit(rotated_head, (head[0], head[1]))
        else:
            pygame.draw.rect(dis, green, [*head, snake_block, snake_block])
        for segment in snake_list[:-1]:
            pygame.draw.rect(dis, green, [*segment, snake_block, snake_block])

# Message display
def message(msg, color):
    mesg = font_style.render(msg, True, color)
    mesg_rect = mesg.get_rect(center=(dis_width // 2, dis_height // 2))
    dis.blit(mesg, mesg_rect)

# Main game loop
def gameLoop():
    game_over = False
    game_close = False

    x1 = dis_width // 2
    y1 = dis_height // 2
    x1_change = snake_block
    y1_change = 0
    direction = 'RIGHT'

    snake_List = []
    Length_of_snake = 1

    foodx = random.randrange(0, dis_width - snake_block, snake_block)
    foody = random.randrange(0, dis_height - snake_block, snake_block)

    while not game_over:

        while game_close:
            dis.blit(background_img, (0, 0)) if background_img else dis.fill(black)
            message("You Lost! Press Q to Quit or C to Play Again", red)
            your_score(Length_of_snake - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        return  # Restart game loop

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change, y1_change = -snake_block, 0
                    direction = 'LEFT'
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change, y1_change = snake_block, 0
                    direction = 'RIGHT'
                elif event.key == pygame.K_UP and y1_change == 0:
                    x1_change, y1_change = 0, -snake_block
                    direction = 'UP'
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    x1_change, y1_change = 0, snake_block
                    direction = 'DOWN'

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            if lose_sound: lose_sound.play()
            game_close = True

        x1 += x1_change
        y1 += y1_change

        dis.blit(background_img, (0, 0)) if background_img else dis.fill(black)
        draw_header()

        if apple_img:
            dis.blit(apple_img, (foodx, foody))
        else:
            pygame.draw.rect(dis, red, [foodx, foody, snake_block, snake_block])

        snake_List.append([x1, y1])

        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        # Tail collects food
        if snake_List[0][0] == foodx and snake_List[0][1] == foody:
            if coin_sound: coin_sound.play()
            Length_of_snake += 1
            foodx = random.randrange(0, dis_width - snake_block, snake_block)
            foody = random.randrange(0, dis_height - snake_block, snake_block)

        # Self collision
        if snake_List[-1] in snake_List[:-1]:
            if lose_sound: lose_sound.play()
            game_close = True

        our_snake(snake_List, direction)
        your_score(Length_of_snake - 1)
        pygame.display.update()
        clock.tick(snake_speed)

    pygame.quit()
    sys.exit()

# Start the game loop
while True:
    gameLoop()
