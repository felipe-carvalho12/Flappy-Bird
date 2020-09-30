class Coin:
    def __init__(self, surface, center):
        self.surface = surface
        self.rect = self.surface.get_rect(center=center)

    def move(self):
        self.rect.centerx -= 2

    def draw(self, screen):
        screen.blit(self.surface, self.rect)
