import pygame, os
from script.core.obj import Obj

class Boss_Mapinguari(Obj):
    """Boss 'Mapinguari' com 5 de vida, HUD reativa e morte ao chegar a 0."""

    def __init__(self, position, groups, size=(400, 400), debug_hitbox=False):
        image_path = os.path.join("assets", "charsSprite", "bosses", "Mapinguari_1.png")
        super().__init__(image_path, position, groups, size)
        
        # ---- Vida / estado ----
        self.max_life = 5
        self.life = 5
        self.dead = False
        self.name = "Mapinguari"

        # callback seguro para HUD (evita erro se não for setado externamente)
        self.on_life_change = lambda v: None
        
        # ---- Animação ----
        self.size = size
        self.state = "idle"
        self.current_frame = 0
        self.ticks = 0
        self.animation_speed = 60

        # Carrega animações
        self.animations = {"idle": []}

        # Para simular uma animação, carregue imagens diferentes ex: Mapinguari_1.png, Mapinguari_2.png
        for i in range(1, 3):  # Espera Mapinguari_1.png e Mapinguari_2.png
            path = os.path.join("assets", "charsSprite", "bosses", f"Mapinguari_{i}.png")
            img = pygame.image.load(path).convert_alpha()
            img = pygame.transform.scale(img, self.size)
            self.animations["idle"].append(img)

        # Define imagem inicial
        self.image = self.animations[self.state][self.current_frame]
        self.rect = self.image.get_rect(topleft=position)

        # ---- Debug ----
        self.debug_hitbox = debug_hitbox

        # ---- Multi-Hitboxes (proporcionais ao rect) ----
        # Importante: são recalculados quando a imagem muda (animate)
        self.hitboxes = {"normal": [], "critical": []}
        self._rebuild_hitboxes()

        # ---- MORTE (config) ----
        death_path = os.path.join("assets", "charsSprite", "bosses", "Mapinguari_D.png")
        self.death_image = pygame.image.load(death_path).convert_alpha()
        self.death_image = pygame.transform.scale(self.death_image, self.size)
        self.death_alpha = 255            # começa opaco
        self.death_duration = 180         # ~3s @60fps
        self.death_timer = 0
        self.death_finished = False

    # ---------- Hitboxes ----------
    def _rebuild_hitboxes(self):
        """
        Recalcula as caixas com base no tamanho/posição atual da sprite.
        Use proporções aproximadas da referência que você desenhou:
        - 3 verdes (tronco/abdômen/pernas) => dano x1
        - 2 vermelhas (olho/boca)         => dano x2
        Ajuste as proporções se mudar a arte.
        """
        w, h = self.rect.size
        cx, cy = self.rect.center

        # Helpers para criar retângulos por proporção (x,y,w,h) relativos ao self.rect
        def R(rel_x, rel_y, rel_w, rel_h):
            rx = self.rect.left + int(rel_x * w)
            ry = self.rect.top  + int(rel_y * h)
            rw = int(rel_w * w)
            rh = int(rel_h * h)
            return pygame.Rect(rx, ry, rw, rh)

        # ---------------- VERDES (dano normal) ----------------
        normal = [
            R(0.30, 0.22, 0.40, 0.25),  # tronco/peito
            R(0.20, 0.42, 0.60, 0.22),  # abdômen
            R(0.18, 0.64, 0.64, 0.30),  # pernas
        ]

        # ---------------- VERMELHAS (críticos x2) ----------------
        critical = [
            R(0.44, 0.08, 0.12, 0.08),  # olho
            R(0.36, 0.30, 0.30, 0.22),  # boca
        ]

        self.hitboxes["normal"] = normal
        self.hitboxes["critical"] = critical

    def draw_hitboxes(self, screen):
        """Desenho opcional para debug."""
        if not self.debug_hitbox:
            return
        for rect in self.hitboxes["normal"]:
            pygame.draw.rect(screen, (0, 255, 0), rect, 2)   # verdes
        for rect in self.hitboxes["critical"]:
            pygame.draw.rect(screen, (255, 0, 0), rect, 2)   # vermelhas


     # ---------- Combate ----------
    def take_damage(self, amount=1):
        """Aplica dano; atualiza HUD; mata ao chegar a 0."""
        if self.dead or amount <= 0:
            return
        self.life = max(0, self.life - amount)
        if callable(self.on_life_change):
            self.on_life_change(self.life)  # atualiza HUD (5..0)
        if self.life <= 0:
            self.die()

    def die(self):
        # entra no estado de morte (não sumir instantaneamente!)
        self.dead = True
        self.state = "dying"
        self.image = self.death_image.copy()
        self.image.set_alpha(self.death_alpha)
        # mantém posição de “queda” coerente
        old_midbottom = self.rect.midbottom
        self.rect = self.image.get_rect()
        self.rect.midbottom = old_midbottom
        # sem colisões
        self._rebuild_hitboxes()
    
    
    # ---------- Loop ----------
    def update(self):
        if self.state == "dying":
            # fade-out e término
            if not self.death_finished:
                self.death_timer += 1
                # diminui alpha suavemente
                step = int(255 / max(1, self.death_duration))
                self.death_alpha = max(0, self.death_alpha - step)
                self.image.set_alpha(self.death_alpha)

                if self.death_timer >= self.death_duration:
                    self.death_finished = True
                    # remove do grupo e avisa a cena
                    self.kill()
                    try:
                        self.on_death_finished()
                    except Exception:
                        pass
            return

        # Vivo: roda animação normal
        self.animate(self.state)
        
    def animate(self, name):
        """Atualiza animação e ressincroniza hitboxes quando troca o frame."""
        self.ticks += 1
        if self.ticks >= self.animation_speed:
            self.ticks = 0
            self.current_frame = (self.current_frame + 1) % len(self.animations[name])
            old_midbottom = self.rect.midbottom  # mantém âncora para não "pular"
            self.image = self.animations[name][self.current_frame]
            self.rect = self.image.get_rect()
            self.rect.midbottom = old_midbottom
            self._rebuild_hitboxes()  # << SINCRONIZA as caixas com a nova imagem

    def interact(self, player):
        """Define interação do boss com o jogador (ex: início de combate)."""
        if self.rect.colliderect(player.rect):
            print("Mapinguari: VOCÊ ATRAVESSOU OS LIMITES! PREPARE-SE PARA LUTAR.")
            # Aqui você pode iniciar o combate, mostrar HUD de batalha, etc.