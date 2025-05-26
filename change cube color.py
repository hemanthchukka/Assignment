from ursina import *

app = Ursina()

box = Entity(model='cube', scale=1, color=rgb(200, 100, 50), position=(0, 0, 0))

def input(key):
    box.color = color.random_color()

app.run()
