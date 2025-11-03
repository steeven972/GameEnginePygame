import pygame as pg
from .utils.entity import Entity
from .utils.ressource import RessourceManager
from .utils.render import RenderSys
from .utils.scene import Scene
from .utils.input import inputManager

class Engine:
    def __init__(self, width: int, height: int, fps: int):
        self.width = width
        self.height = height
        self.fps = fps
        self.rm = RessourceManager()
        self.entities = {}
        self.all_sprites = pg.sprite.Group()

        pg.init()
        self.screen = pg.display.set_mode((width, height))
        self.bg_color = (0, 0, 0)
        
        self.clock = pg.time.Clock()
        self.running = True
        self.scene = Scene(self)
        self.input = inputManager(self)
        self.scene_type = "game"
        self.render = RenderSys(self.screen, self.bg_color, self.all_sprites)

    def change_scene(self, new_scene_type):
        self.scene_type = new_scene_type

    def mainloop(self):
        try:
            while self.running:
                self.tick = self.clock.tick(self.fps)
                dt = self.tick /1000.0
                self.scene.render.clear()
                events = pg.event.get()
                self.input.handle_events(events)
                
                
                self.render.draw_scene(self.scene_type, dt)
                
                pg.display.update()

        except Exception as e:
            print(f"[FATAL] Error in mainloop : {e}")
        finally:
            pg.quit()   

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False

    def stop(self):
        pg.quit()
