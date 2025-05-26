from ursina import *

app = Ursina()

player = Entity(model='cube', color=color.azure, scale=1.5, position=(-2, 0, 0))

def change_player_color():
    player.color = color.random_color()

my_button = Button(text='Click Me', color=color.green, scale=(0.3, 0.1), position=(0.2,0))

icon = Entity(parent=my_button, model='quad', color=color.white, scale=(0.05, 0.05), position=(-0.1, 0, -0.01))

my_button.on_click = change_player_color

app.run()
