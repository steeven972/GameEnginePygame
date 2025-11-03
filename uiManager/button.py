import pygame as pg

pg.init()
screen = pg.display.set_mode((800, 600))
clock = pg.time.Clock()

class Button:
    def __init__(self, text, pos, size, callback):
        self.rect = pg.Rect(pos, size)
        self.text = text
        self.callback = callback
        self.font = pg.font.SysFont(None, 36)
        self.color_default = (60, 60, 60)
        self.color_hover = (100, 100, 100)
        self.color = self.color_default

    def handle_event(self, event):
        if event.type == pg.MOUSEMOTION:
            self.color = self.color_hover if self.rect.collidepoint(event.pos) else self.color_default
        if event.type == pg.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.callback()

    def draw(self, surface):
        pg.draw.rect(surface, self.color, self.rect, border_radius=8)
        text_surf = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

class UIManager:
    def __init__(self):
        self.widgets = []

    def add(self, widget):
        self.widgets.append(widget)

    def handle_event(self, event):
        for w in self.widgets:
            w.handle_event(event)

    def draw(self, surface):
        for w in self.widgets:
            w.draw(surface)

def start_game():
    print("Game started!")

ui = UIManager()
ui.add(Button("Start Game", (300, 250), (200, 60), start_game))

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        ui.handle_event(event)

    screen.fill((30, 30, 30))
    ui.draw(screen)
    pg.display.flip()
    clock.tick(60)
