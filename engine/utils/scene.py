
import pygame as pg
from .render import RenderSys
from .entity import Entity

class Scene:
    def __init__(self, engine):
        self.engine = engine   
        self.render = RenderSys(engine)

    def create_entity(self, filePath:str, pos: tuple) -> Entity:
        try:
            file = filePath.split("/")[-1]
            name, _ = file.split(".")
            entity = Entity(name,image=self.engine.rm.get_image(file), pos=pos)
            self.engine.entities[name] = entity
            self.engine.all_sprites.add(entity)
            return entity
        except Exception as e:
            import traceback
            print(f"[FATAL] Failed to create entity : {name} error : {e}")
            traceback.print_exc()
            return None
