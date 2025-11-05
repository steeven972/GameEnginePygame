import pygame as pg


class inputManager:
    def __init__(self, engine):
        self.engine = engine

    def handle_events(self, event):
        if event.type == pg.QUIT:
            self.engine.running = False
