from ursina import *

app = Ursina()

window_width = 16
window_height = 9
camera.orthographic = True
camera.fov = window_height
camera.position = (window_width/2, -window_height/2, -20)

background = Entity(
    model='quad',
    texture='brick',   
    scale=(window_width, window_height),
    position=(window_width/2, -window_height/2, 5), 
)

ball = Entity(
    model='circle',
    texture='shore',   
    color=color.white,
    scale=0.5,
    position=(window_width/2, -window_height/2, 0),
)

gravity = -9.8 
velocity = Vec3(3, 7, 0)  
dt = 1/60 

def update():
    global velocity

    
    velocity.y += gravity * dt

   
    ball.position += velocity * dt

  
    if ball.x - ball.scale_x/2 < 0:
        ball.x = ball.scale_x/2
        velocity.x *= -1
    elif ball.x + ball.scale_x/2 > window_width:
        ball.x = window_width - ball.scale_x/2
        velocity.x *= -1

   
    if ball.y - ball.scale_y/2 < -window_height:
        ball.y = -window_height + ball.scale_y/2
        velocity.y *= -0.8
        if abs(velocity.y) < 0.1:
            velocity.y = 0
    elif ball.y + ball.scale_y/2 > 0:
        ball.y = 0 - ball.scale_y/2
        velocity.y *= -1

def input(key):
    global velocity
    on_floor = abs(ball.y - (-window_height + ball.scale_y/2)) < 0.01
    if key == 'space' and on_floor:
        velocity.y = 7  #

app.run()
