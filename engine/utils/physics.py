class Gravity:
    def __init__(self):
        self.gravity = 0.05
        self.speedX = 0
        self.speedY = 0
        self.gravitySpeed = 0
        self.max_fall = 9.81
    def update(self, entity):
        if self.gravitySpeed < self.max_fall:
            self.gravitySpeed += self.gravity
        entity.x += self.speedX
        entity.y += self.speedY + self.gravitySpeed
        entity.update_rect()

