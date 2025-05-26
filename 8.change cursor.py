from ursina import *

if __name__ == '__main__':
    app = Ursina()

    camera.orthographic = True
    camera.fov = 4
    camera.position = (1, 1)
    Text.default_resolution *= 2

    player = Entity(name='$', color=color.azure)
    cursor = Tooltip(player.name, color=player.color, origin=(0, 0), scale=4, enabled=True)
    cursor.background.color = color.clear
    bg = Entity(parent=scene, model='quad', scale=(16, 8), z=10, color=color.rgb(180, 197, 228))
    mouse.visible = False
    

    app.run()
