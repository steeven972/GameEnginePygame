from engine.core import Engine


if __name__ == "__main__":

    WIDTH = 1280
    HEIGHT = 720
    app = Engine(WIDTH, HEIGHT, 60)

    app.rm.load_image("Pouch.png")
    app.rm.load_image("Atrox.png")

    scene = app.scene
    player = scene.create_entity("Pouch.png", (WIDTH // 2, HEIGHT // 2))
    atrox = scene.create_entity("Atrox.png", (200, 200))

   
    if player:
        player.is_character(True)
        player.is_rigidBody(True)

    app.mainloop()
    app.stop()

   