import pygame

class Ground(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, debug=False):
        super().__init__()
        # surface com alpha
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)

        if debug:
            # só se quiser ver o chão durante depuração:
            pygame.draw.rect(self.image, (0, 255, 0), self.image.get_rect(), 2)
        # se debug=False, fica totalmente invisível

        self.rect = self.image.get_rect(topleft=(x, y))