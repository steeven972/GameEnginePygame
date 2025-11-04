import pygame as pg

class Elements:
    def __init__(self, pos: tuple, size:tuple, text:str, color: tuple, ft_size:int, bg_color:tuple, ft_family:str = 'Arial', border_radius=0):
        self.pos = pos
        self.size = size 
        self.relative_rect = pg.Rect(pos, size)
        self.ft_family = ft_family
        self.ft_size = ft_size
        self.color = color
        self.default_bg_color = bg_color
        self.bg_color = bg_color
        self.border_radius = border_radius
        self.text = text
        self.font = pg.font.SysFont(ft_family, ft_size)
    def draw(self, master):
        pg.draw.rect(master, self.color, self.relative_rect)
        text_surf = self.font.render(self.text, True, self.color)
        text_rect = text_surf.get_rect(center = self.relative_rect.center)
        master.blit(text_surf, text_rect)
        
    def get_rect(self):
        return self.relative_rect

    def get_pos(self):
        return self.relative_rect.center
class UIButton(Elements):
    def __init__(self, pos: tuple, size:tuple, text:str, color: tuple, ft_size:int, bg_color:tuple, ft_family:str = 'Arial', border_radius=0):
        super().__init__(pos, size, text, color,ft_size, bg_color, ft_family, border_radius)
        self.hover = tuple(min(255, max(0, x - 50)) for x in self.bg_color)
        self.relative_rect = pg.Rect(pos, size)
        self.text = text
    
    def draw(self, master):
        pg.draw.rect(master, self.bg_color, self.relative_rect, border_radius=self.border_radius)
        text_surf = self.font.render(self.text, True, self.color)
        text_rect = text_surf.get_rect(center = self.relative_rect.center)
        master.blit(text_surf, text_rect)

    def onClick(self, event: pg.event, callback):
        if event.type == pg.MOUSEMOTION:
            self.bg_color = self.hover if self.relative_rect.collidepoint(event.pos) else self.default_bg_color
        if event.type == pg.MOUSEBUTTONDOWN and self.relative_rect.collidepoint(event.pos):
            return callback()
    
class UITextBox(Elements):
    def __init__(self, pos, size, text, color, ft_size, bg_color, ft_family = 'Arial', border_radius=0):
        super().__init__(pos, size, text, color, ft_size, bg_color, ft_family, border_radius)
        self.active = False
        
    def clear(self):
        self.text = ""

    