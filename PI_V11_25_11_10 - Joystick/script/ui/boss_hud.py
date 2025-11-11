import pygame, os

class BossHud(pygame.sprite.Sprite):
    """
    HUD do Mapinguari com 6 sprites numeradas (5..0).
    Use: hud.set(value) para trocar a imagem conforme a vida.
    """
    def __init__(self, position=(0,0), size=(1280, 720),
                 folder="assets/charsSprite/bosses/", prefix="Hud_Mapinguari_"):
        super().__init__()
        self.frames = {}
        # Carrega 0..5 (deixe os arquivos no caminho indicado)
        for i in range(0, 6):
            path = os.path.join(folder, f"{prefix}{i}.png")
            img = pygame.image.load(path).convert_alpha()
            self.frames[i] = pygame.transform.scale(img, size)

        self.value = 5  # começa cheio
        self.image = self.frames[self.value]
        self.rect = self.image.get_rect(topleft=position)

    def set(self, value: int):
        """Atualiza HUD para 5..0 (clamp)."""
        v = max(0, min(5, int(value)))
        if v != self.value:
            self.value = v
            self.image = self.frames[self.value]

    def draw(self, screen):
        screen.blit(self.image, self.rect)