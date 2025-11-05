import pygame as pg

class Entity(pg.sprite.Sprite):
    def __init__(self,name, image, pos: tuple, tag:str = "entity", gravity: bool =False,
                  visible:bool =True, rigid_body: bool =False, character: bool=False):
        
        super().__init__()
        self.name = name
        self.image = image
        self.sprite = None
        self.rect = image.get_rect(center = pos)
        self.tag = tag

        self.x, self.y = pos
        self.speed = 200
        self.max_speed = 200
        self.velocity_x = 0
        self.velocity_y = 0
        self.acceleration_x = 0
        self.acceleration_y = 0

        self.use_gravity = gravity
        self.character = character
        self.rigid_body = rigid_body
        self.visible = visible

    def draw(self, screen: pg.display):
        screen.blit(self.image, self.rect)

    def update_rect(self):
        self.rect.center = (self.x, self.y)

    def get_pos(self):
        return (self.x, self.y)
    
    def set_pos(self, x, y):
        self.x = x
        self.y = y
        self.update_rect()

    def is_character(self, bool: bool):
        self.character = bool
        return self.character

    def is_rigidBody(self, bool: bool):
        self.rigid_body = bool
        return self.rigid_body
    
    def set_speed(self, speed):
        self.speed = speed

    def get_speed(self):
        return self.speed