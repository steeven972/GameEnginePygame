import pygame as pg
from .entity import Entity
import math

class Movements:
    def __init__(self):
        pass

    def handle_input(self,screen, entity, dt: float):
        key = pg.key.get_pressed()
        if key[pg.K_z]:
            entity.y -= entity.speed * dt
        if key[pg.K_s]:
            entity.y += entity.speed * dt
        if key[pg.K_d]:
            entity.x += entity.speed * dt
        if key[pg.K_q]:
            entity.x -= entity.speed * dt
        entity.draw(screen)
        entity.update_rect()
    
    def follow_target(self, entity, target: Entity, dt):
        dx = target.x - entity.x
        dy = target.y - entity.y

        distance = math.sqrt(dx**2 + dy**2)

        if distance > 1:
            dx /= distance
            dy /= distance

            entity.x += dx * entity.speed * dt
            entity.y += dy * entity.speed * dt

            entity.update_rect()
        else:
            entity.set_pos(target.x, target.y)
