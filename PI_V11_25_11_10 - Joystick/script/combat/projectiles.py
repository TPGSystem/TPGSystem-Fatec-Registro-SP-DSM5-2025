import pygame
from script.setting import BASE_WIDTH

class Shot(pygame.sprite.Sprite):
    """
    Projétil com hitbox linear (linha do ponto anterior ao atual).
    - Colide primeiro com hitboxes CRÍTICOS (×2), depois com os NORMAIS (×1).
    - Usa pygame.Rect.clipline para detectar o ponto de entrada na caixa.
    """
    def __init__(self, x, y, direction, groups, size=(80, 25), speed=12, damage=1, debug=False):
        super().__init__(groups)

        self.direction = 1 if direction >= 0 else -1
        self.speed = speed
        self.damage = damage
        self.debug = debug

        # Carrega imagem (visual), mas a colisão é pela linha do movimento
        image = pygame.image.load("assets/projectiles/Shot1.png").convert_alpha()
        image = pygame.transform.scale(image, size)
        if self.direction == -1:
            image = pygame.transform.flip(image, True, False)
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))

        # Guardar o centro anterior para formar a "linha" do frame
        self.prev_center = pygame.Vector2(self.rect.center)

    def _apply_damage_and_die(self, boss, multiplier, impact_point):
        """Aplica dano ao boss e encerra o projétil."""
        boss.take_damage(int(self.damage * multiplier))
        # Posiciona visualmente no ponto de impacto (opcional)
        if impact_point:
            self.rect.center = (int(impact_point[0]), int(impact_point[1]))
        self.kill()

    def update(self, boss=None):
        """
        Move o projétil e, se 'boss' for passado, testa a linha de impacto
        contra os retângulos do boss (críticos primeiro).
        """
        # 1) Movimento
        self.prev_center.update(self.rect.center)  # guarda posição anterior
        self.rect.x += self.direction * self.speed

        # 2) Fora da tela? morre
        if self.rect.right < 0 or self.rect.left > BASE_WIDTH:
            self.kill()
            return

        # 3) Colisão por linha (se boss disponível)
        if boss and not boss.dead:
            p0 = (self.prev_center.x, self.prev_center.y)
            p1 = (self.rect.centerx, self.rect.centery)
            seg = (p0, p1)

            # --- críticos primeiro (x2) ---
            for r in boss.hitboxes["critical"]:
                hit = r.clipline(seg)
                if hit:
                    # ponto de entrada = hit[0]
                    self._apply_damage_and_die(boss, multiplier=2.0, impact_point=hit[0])
                    return

            # --- normais (x1) ---
            for r in boss.hitboxes["normal"]:
                hit = r.clipline(seg)
                if hit:
                    self._apply_damage_and_die(boss, multiplier=1.0, impact_point=hit[0])
                    return

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)
        if self.debug:
            # Desenha a "linha" (hitbox linear) do último frame
            pygame.draw.line(surface, (255, 0, 0),
                             (int(self.prev_center.x), int(self.prev_center.y)),
                             (int(self.rect.centerx), int(self.rect.centery)), 2)