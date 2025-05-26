from ursina import *
import time

app = Ursina()

maze_map = [
    "WWWWWWWWWW",
    "W...W....W",
    "W.W.W.WW.W",
    "W.W...W..W",
    "W.WWW.WW.W",
    "W.....W..W",
    "WWW.W.WW.W",
    "W...W....W",
    "W.W.W.WG.W",
    "WWWWWWWWWW",
]

TILE_SIZE = 1

walls = []
wall_positions = set()  

for y, row in enumerate(maze_map):
    for x, tile in enumerate(row):
        world_x, world_y = x * TILE_SIZE, -y * TILE_SIZE
        if tile == "W":
            wall = Entity(
                model='quad',
                color=color.gray,
                collider='box',
                position=(world_x, world_y, 0),
                scale=(TILE_SIZE, TILE_SIZE)
            )
            walls.append(wall)
            wall_positions.add((world_x, world_y))
        elif tile == ".":
            floor = Entity(
                model='quad',
                color=color.light_gray,
                position=(world_x, world_y, 0),
                scale=(TILE_SIZE, TILE_SIZE)
            )
        elif tile == "G":
            goal = Entity(
                model='sphere',  
                color=color.green,
                position=(world_x, world_y, 0),
                scale=(TILE_SIZE, TILE_SIZE)
            )
            goal_pos = (world_x, world_y)
        elif tile == "P":
            player_start = (world_x, world_y)

if 'player_start' not in locals():
    player_start = (TILE_SIZE, -TILE_SIZE)

player = Entity(
    model='quad',
    color=color.orange,
    scale=(TILE_SIZE * 0.8, TILE_SIZE * 0.8),
    position=(player_start[0], player_start[1], -0.1),
    collider='box'
)

camera.orthographic = True
camera.fov = 10
camera.position = (TILE_SIZE * 5, -TILE_SIZE * 5, -20)

move_cooldown = 0.15
last_move_time = 0
game_started = True
start_time = time.time()  

win_text = Text(text='', origin=(0, 0), scale=2, position=(0, 0), color=color.white)

def move_player(dx, dy):
    global last_move_time, game_started
    current_time = time.time()
    if current_time - last_move_time < move_cooldown:
        return

    target_pos = (player.position.x + dx * TILE_SIZE, player.position.y + dy * TILE_SIZE)

    if target_pos in wall_positions:
        return 

    player.position = (target_pos[0], target_pos[1], player.position.z)
    last_move_time = current_time

    if (player.position.x, player.position.y) == goal_pos:
        elapsed_time = current_time - start_time  
        win_text.text = f"You Won!\nTime: {elapsed_time:.2f} seconds"  
        game_started = False  

def update():
    if not game_started:
        return  

    if held_keys['a'] or held_keys['left arrow']:
        move_player(-1, 0)
    elif held_keys['d'] or held_keys['right arrow']:
        move_player(1, 0)
    elif held_keys['w'] or held_keys['up arrow']:
        move_player(0, 1)
    elif held_keys['s'] or held_keys['down arrow']:
        move_player(0, -1)

app.run()
