class Pipe:
    def __init__(self, surface, midtop=None, midbottom=None):
        self.surface = surface
        if midtop is not None:
            self.rect = self.surface.get_rect(midtop=midtop)
        elif midbottom is not None:
            self.rect = self.surface.get_rect(midbottom=midbottom)

    def move(self):
        self.rect.centerx -= 2

    def draw(self, screen):
        screen.blit(self.surface, self.rect)
