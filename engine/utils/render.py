import pygame as pg
from .movements import Movements
from .physics import Gravity

class RenderSys:
    def __init__(self,engine):
        self.engine = engine
        self.move = Movements()
        self.gravity = Gravity()

    def clear(self):
        """Efface l’écran avec la couleur de fond."""
        self.engine.screen.fill(self.engine.bg_color)
        
   
    def draw_game(self, dt):
        """Rendu de la scène de jeu (avec les entités et mouvements)."""
        self.clear()

        # Gérer les mouvements
        for entity in self.engine.all_sprites:

            is_character =getattr(entity, "character", False)
            is_rigid =getattr(entity, "rigid", False)

            if is_rigid:
                self.gravity.update(entity)

            if is_character:  # sécurité
                self.move.handle_input(self.engine.screen, entity, dt)
                
           

        # Mettre à jour les sprites et les dessiner
        self.engine.all_sprites.update()
        self.engine.all_sprites.draw(self.engine.screen)

    def draw_menu(self):
        """Rendu du menu principal."""
        self.clear()
        font = pg.font.SysFont(None, 50)
        text_surface = font.render("Press ENTER to start", True, (255, 255, 255))
        self.engine.screen.blit(text_surface, (100, 200))

    def draw_scene(self, scene_type: str, dt=0, event=None):
        """
        Permet de choisir dynamiquement le rendu selon la scène active.
        Exemple : render.draw_scene("menu") ou render.draw_scene("game", dt)
        """
        if event is None:
            if scene_type == "menu":
                self.draw_menu()
            elif scene_type == "game":
                self.draw_game(dt)
        elif event is not None:
            if scene_type == "initProject":
                self.draw_initProject_Interface(event)
        else:
            raise ValueError(f"Unknown scene type: {scene_type}")
