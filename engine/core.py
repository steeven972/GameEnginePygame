import pygame as pg
from .utils.ressource import RessourceManager
from .utils.render import RenderSys
from .utils.scene import Scene
from .utils.input import inputManager
from .utils.UIManager import UIManager
from editor.elements import UIButton

class Engine:
    def __init__(self, width: int, height: int, fps: int):

        self.width = width
        self.height = height
        self.fps = fps
        self.running = True

        pg.init()

        self.screen = pg.display.set_mode((width, height))
        pg.display.set_caption("Game engine")
        self.bg_color = (30, 30, 30)
        self.clock = pg.time.Clock()

        self.rm = RessourceManager()
        self.scene = Scene(self)
        self.input = inputManager(self)
        self.render = RenderSys(self)
        self.ui = UIManager()

        self.all_sprites = pg.sprite.Group()
        self.entities = {}
        self.scene_type = "initProject"

        
        self.button = UIButton((0,0), (100, 60), "Start Game", (0, 0, 0), 16, (255, 0, 0))
        self.ui.add(self.button)

       
    def change_scene(self, new_scene_type:str):
        self.scene_type = new_scene_type
    
    def start_game(self):
        self.scene_type = "game"
        print("hello")

    def mainloop(self):
        try:
            while self.running:
                self.tick = self.clock.tick(self.fps)
                dt = self.tick /1000.0
                self.scene.render.clear()

                for e in pg.event.get():
                    self.input.handle_events(e)
                    self.button.onClick(e, self.start_game)
              
                if self.scene_type == "initProject":
                    self.ui.draw(self.screen)
                else:
                    self.render.draw_scene(self.scene_type, dt)
                
                pg.display.update()

        except Exception as e:
            import traceback
            print("[FATAL] Error in mainloop:")
            traceback.print_exc()

        finally:
            pg.quit()   

    def stop(self):
        pg.quit()
