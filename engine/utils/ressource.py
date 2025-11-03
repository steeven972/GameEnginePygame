import pygame as pg
import os
class RessourceManager:
    def __init__(self):
        self._images = {}
        self.base_path = os.path.join('assets', 'images')

    def load_image(self, fileName) -> pg.Surface:
        try:
            path = os.path.join(self.base_path, fileName)
            if path in self._images:
                print(f"[INFO] Image already loaded")
                return self._images[path]
            else:
                image = pg.image.load(path).convert_alpha()
                self._images[fileName] = image
                print(f"[INFO] Image loaded succefully : {path}")
                return image
        except Exception as e:
            print(f"[WARNING] Erreur in load_image() : {e}")
            return None
        
    def get_image(self, imageName: str) -> pg.Surface:
        if imageName in self._images:
            return self._images[imageName]
        else:
            print(f"[FATAL] Image {imageName} is not loaded")
            return None

