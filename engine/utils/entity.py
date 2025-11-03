import pygame as pg

class Entity(pg.sprite.Sprite):
    def __init__(self,name, image, pos: tuple ):
        super().__init__()
        self.name = name
        self.image = image
        self.rect = image.get_rect(center = pos)
        self.x, self.y = pos
        self.speed = 200
        self.character = False
        self.rigid = False

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
        self.rigid = bool
        return self.rigid
    def set_speed(self, speed):
        self.speed = speed

    def get_speed(self):
        return self.speed