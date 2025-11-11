import pygame, os
from script.setting import BASE_HEIGHT, GROUND_LEVEL
from script.core.obj import Obj
from script.combat.projectiles import Shot


class Player(Obj):
    """
    Guardiões de Pindorama — Player

    Controles:
      • A/D ou ←/→ : andar e VIRAR o personagem imediatamente
      • S/↓ (segurar): agachar parado (down / c_idle)
      • K: bloquear em pé (block)
      • S/↓ + K: bloquear agachado (c_block)
      • Q: atacar em pé (shot)
      • S/↓ + Q (segurar Q): atacar agachado (c_shot); ao soltar Q, continua agachado
      • SPACE: pular (se não estiver bloqueando/rolando)
      • Left Shift: dash/roll (percorre EXATOS 200 px, com cooldown)
    """

    # -------------------------------
    # Loader tolerante de sprites
    # -------------------------------
    def _load_seq_scaled(self, prefix: str, count: int, size=None,
                         root="assets/charsSprite/player/indigenaM/"):
        """
        Carrega sequência prefix0..prefix{count-1} (ex.: R_D0.png).
        Se não achar, tenta arquivo único prefix.png (ex.: R_D.png).
        Também tenta variação sem underscore (R_D -> RD). Retorna ≥1 frame.
        """
        size = size or self.size
        frames = []

        # 1) tenta sequência
        for i in range(count):
            found = None
            for pf in (prefix, prefix.replace("_", "")):
                for ext in (".png", ".PNG"):
                    path = os.path.join(root, f"{pf}{i}{ext}")
                    if os.path.exists(path):
                        found = path
                        break
                if found:
                    break
            if not found:
                if i == 0:
                    frames = []
                break
            img = pygame.image.load(found).convert_alpha()
            frames.append(pygame.transform.scale(img, size))

        if frames:
            return frames

        # 2) tenta arquivo único
        for pf in (prefix, prefix.replace("_", "")):
            for ext in (".png", ".PNG"):
                one = os.path.join(root, f"{pf}{ext}")
                if os.path.exists(one):
                    img = pygame.image.load(one).convert_alpha()
                    return [pygame.transform.scale(img, size)]

        # 3) falhou: relata tentativas
        tried = []
        for pf in (prefix, prefix.replace("_", "")):
            for ext in (".png", ".PNG"):
                tried.append(os.path.join(root, f"{pf}{ext}"))
                tried.append(os.path.join(root, f"{pf}0{ext}"))
        raise FileNotFoundError(f"Nenhuma imagem encontrada para '{prefix}'. Tentativas: {tried}")

    # --------------------------------------
    # Lazy-load para animações específicas
    # --------------------------------------
    def _ensure_anim(self, key: str, prefix: str, count: int):
        """Carrega self.animations[key] se ainda não estiver carregada."""
        if key not in self.animations or not self.animations[key]:
            self.animations[key] = self._load_seq_scaled(prefix, count)

    # --------------------------------------
    # (Opcional) mover X respeitando limites
    # --------------------------------------
    def _move_x_with_limits(self, dx: int):
        
        if getattr(self, "exit_mode", False):
            self.rect.x += dx
            return
        
        """
        Move no eixo X respeitando bordas de tela e (se aplicável) o lock do buraco.
        Usado no dash para não sair da tela/atravessar limites.
        """
        
        
        screen_width = 1280
        buffer = 75
        next_x = self.rect.x + dx

        if self.in_hole and self.fall_lock_x_range:
            left, right = self.fall_lock_x_range
            next_x = max(left, min(next_x, right - self.rect.width))
            self.rect.x = next_x
            return

        if dx > 0:
            if next_x + self.rect.width - buffer < screen_width:
                self.rect.x = next_x
        else:
            if next_x + buffer > 0:
                self.rect.x = next_x

    # -------------------------------
    # Construção / estado inicial
    # -------------------------------
    def __init__(self, image_path, position, groups, size=(200, 200),
                 life=25, lives=3, xp=0, has_hole=True):
        super().__init__(image_path, position, groups, size)

        # Atributos gerais
        self.image_path = image_path
        self.life = life
        self.lives = lives
        self.xp = xp
        self.size = size
        self.has_hole = has_hole

        # Sprite inicial (idle frame 0)
        self.original_image = pygame.image.load(
            "assets/charsSprite/player/indigenaM/R0.png"
        ).convert_alpha()
        self.image = pygame.transform.scale(self.original_image, size)
        self.rect = self.image.get_rect(topleft=position)

        # Mundo/física
        self.in_hole = False
        self.fall_lock_x_range = None
        self.facing_right = True
        self.is_dead = False

        self.vel = 5
        self.grav = 0.5
        self.jump_power = -15
        self.is_jumping = False
        self.on_ground = False

        # Inputs horizontais
        self.right = False
        self.left  = False

        # Estados avançados
        self.crouching = False
        self.blocking  = False
        self.rolling   = False
        self.invulnerable = False

        # DASH/ROLL — distância exata + cooldown
        self.roll_key = pygame.K_LSHIFT
        self.roll_duration_ms = 350         # duração do dash
        self.roll_distance_px = 200         # DISTÂNCIA EXATA
        self.roll_cooldown_ms = 450         # cooldown entre dashes
        self.roll_timer = 0
        self._last_tick_ms = 0
        self._last_roll_end_ms = -9999
        self._roll_acc_px = 0.0             # acumula subpixels por frame
        self.roll_moved_px = 0.0            # quanto já percorreu no dash atual

        # Disparos/anim
        self.shots = pygame.sprite.Group()
        self.shot_released = False
        self.current_frame = 0
        self.animation_speed = 5
        self.ticks = 0
        self.img = 0

        # Offsets e velocidades do tiro por postura
        self.shot_offsets = {
            "stand":  {"right": (80, 60), "left": (30, 60)},
            "crouch": {"right": (70, 105), "left": (20, 90)},
        }
        self.shot_speed = {"stand": 7, "crouch": 6}

        # -------------------------------
        # Registro de animações
        # -------------------------------
        self.animations = {
            "idle": [
                pygame.transform.scale(pygame.image.load(
                    "assets/charsSprite/player/indigenaM/R0.png"), size),
                pygame.transform.scale(pygame.image.load(
                    "assets/charsSprite/player/indigenaM/R1.png"), size),
            ],
            "walk": [pygame.transform.scale(
                pygame.image.load(f"assets/charsSprite/player/indigenaM/M{i}.png"), size)
                for i in range(8)],
            "shot": self._load_seq_scaled("S", 7),
            "jump": self._load_seq_scaled("J", 17),

            # c_idle será carregada on-demand ao agachar
            "c_idle": [],

            # Bloqueio (em pé/abaixado) — normalmente 1 frame; aceita sequência se existir
            "block":   self._load_seq_scaled("B_U", 1),
            "c_block": self._load_seq_scaled("B_D", 1),

            # Ataque agachado (aceita S_D0.. ou S_D.png)
            "c_shot": self._load_seq_scaled("S_D", 7),

            # Placeholders (trocar quando tiver sprites dedicados)
            "roll": [pygame.transform.scale(
                pygame.image.load("assets/charsSprite/player/indigenaM/B_D.png"), size)],
            "dead": [pygame.transform.scale(
                pygame.image.load("assets/charsSprite/player/indigenaM/B_D.png"), size)],
        }

        # Espelhadas (listas prontas para left/right)
        self.animations["shot_left"]  = [pygame.transform.flip(img, True, False)
                                         for img in self.animations["shot"]]
        self.animations["shot_right"] = self.animations["shot"]
        self.animations["jump_left"]  = [pygame.transform.flip(img, True, False)
                                         for img in self.animations["jump"]]
        self.animations["jump_right"] = self.animations["jump"]
        self.animations["c_shot_left"]  = [pygame.transform.flip(img, True, False)
                                           for img in self.animations["c_shot"]]
        self.animations["c_shot_right"] = self.animations["c_shot"]

        # Alias do agachado parado (preenchido no 1º agachamento)
        self.animations["down"] = []

        # Estados que NÃO têm variantes left/right (flipamos manualmente)
        self._dirless = {"idle", "walk", "down", "block", "c_block", "roll", "dead"}

        # Estado inicial
        self.state = "idle"
        self.image = self.animations[self.state][self.current_frame]
        self.rect  = self.image.get_rect(topleft=position)

        # Outros
        self.gold = 0
        self.dialog_active = False
        self.dialog_npc = None

    # -------------------------------
    # Utilitário de cooldown do roll
    # -------------------------------
    def _roll_ready(self) -> bool:
        return pygame.time.get_ticks() - self._last_roll_end_ms >= self.roll_cooldown_ms

    # -------------------------------
    # Ciclo por frame
    # -------------------------------
    def update(self):
        super().update()
        self.gravity()

        # Movimenta apenas se não estiver em um estado “ocupado”
        busy = self.state in ("shot", "c_shot", "block", "c_block", "roll", "dead") or self.blocking
        if not busy:
            self.movements()

        # Atualiza projéteis
        self.shots.update()

        # ---- Bloqueio: anima mesmo sem movements() ----
        if self.blocking:
            self.state = "c_block" if self.crouching else "block"
            self.animate(self.state, 80, 1)

        # ---- Ataques (em pé / agachado) ----
        if self.state == "shot":
            self.animate("shot_right" if self.facing_right else "shot_left", 25, 7)
        if self.state == "c_shot":
            self.animate("c_shot_right" if self.facing_right else "c_shot_left", 25, 7)

        # ---- Garante agachado parado mesmo se movements() não rodar neste frame ----
        if (self.crouching and not self.left and not self.right
            and not self.is_jumping and not self.blocking
            and self.state not in ("shot", "c_shot", "roll", "dead")):

            if not self.animations["c_idle"]:
                self._ensure_anim("c_idle", "R_D", 1)
                self.animations["down"] = self.animations["c_idle"]

            self.state = "down"
            frames_down = max(1, len(self.animations.get("down", [])))
            self.animate("down", 100, frames_down)

        # ---- ROLL/DASH: distância EXATA de 200 px, independente do FPS ----
        if self.state == "roll":
            now = pygame.time.get_ticks()
            dt_ms = now - (self._last_tick_ms or now)
            self._last_tick_ms = now
            self.roll_timer += dt_ms

            # velocidade (px/ms) p/ cobrir a distância no tempo alvo
            speed_px_per_ms = self.roll_distance_px / max(1, self.roll_duration_ms)

            # deslocamento sugerido neste frame (float)
            step = speed_px_per_ms * dt_ms

            # não ultrapassa a distância restante
            remaining = self.roll_distance_px - self.roll_moved_px
            step = min(step, max(0.0, remaining))

            # acumula subpixel e aplica a parte inteira
            self._roll_acc_px += step
            apply_px = int(self._roll_acc_px)
            self._roll_acc_px -= apply_px

            if apply_px > 0:
                dx = apply_px if self.facing_right else -apply_px
                self._move_x_with_limits(dx)
                self.roll_moved_px += abs(apply_px)

            # anima roll (placeholder até ter sprites)
            self.animate("roll", 10, max(1, len(self.animations["roll"])))

            # encerra: completou distância ou estourou tempo (fallback)
            if self.roll_moved_px >= self.roll_distance_px or self.roll_timer >= self.roll_duration_ms:
                self.rolling = False
                self.invulnerable = False
                self.state = "idle"
                self.roll_timer = 0
                self._last_roll_end_ms = pygame.time.get_ticks()
                self._roll_acc_px = 0.0
                self.roll_moved_px = 0.0

        # ---- Morte ----
        if self.is_dead or self.state == "dead":
            self.is_dead = True
            self.animate("dead", 12, max(1, len(self.animations["dead"])))
            return

        # ---- Diálogo trava ações ----
        if self.dialog_active:
            return

        # ---- Queda fatal / respawn ----
        if self.check_death():
            if self.lives <= 0:
                self.die()

    # -------------------------------
    # Física vertical
    # -------------------------------
    def gravity(self):
        self.vel += self.grav
        self.rect.y += self.vel

        # buracos da fase
        if hasattr(self, "holes"):
            for hole_rect in self.holes:
                if hole_rect.collidepoint(self.rect.centerx, self.rect.bottom):
                    if not self.in_hole:
                        print("[DEBUG] Entrou no buraco!")
                        self.in_hole = True
                        self.fall_lock_x_range = (hole_rect.left, hole_rect.right)
                    break

        # clamp de queda
        if self.vel >= 10:
            self.vel = 10

        # colide com o chão se não estiver caindo no buraco
        if not self.in_hole:
            if self.rect.y >= GROUND_LEVEL - self.rect.height:
                self.rect.y = GROUND_LEVEL - self.rect.height
                self.vel = 0
                self.on_ground = True
                self.is_jumping = False

    def set_holes(self, hole_list):
        self.holes = hole_list

    # -------------------------------
    # Entrada de teclado
    # -------------------------------
    def events(self, events):
        if events.type == pygame.KEYDOWN:
            pressed = pygame.key.get_pressed()
            crouch_mod = pressed[pygame.K_s] or pressed[pygame.K_DOWN]

            if events.key in (pygame.K_d, pygame.K_RIGHT):
                self.right = True
                self.facing_right = True     # Vira imediatamente p/ direita

            elif events.key in (pygame.K_a, pygame.K_LEFT):
                self.left = True
                self.facing_right = False    # Vira imediatamente p/ esquerda

            elif events.key in (pygame.K_s, pygame.K_DOWN):
                self.crouching = True
                if not self.animations["c_idle"]:
                    self._ensure_anim("c_idle", "R_D", 1)
                    self.animations["down"] = self.animations["c_idle"]
                self.state = "c_block" if self.blocking else "down"

            elif events.key == pygame.K_k:
                self.blocking = True
                self.state = "c_block" if (crouch_mod or self.crouching) else "block"

            elif events.key == self.roll_key:
                if not self.rolling and not self.blocking and self._roll_ready():
                    self.rolling = True
                    self.invulnerable = True
                    self.roll_timer = 0
                    self._last_tick_ms = pygame.time.get_ticks()
                    self.state = "roll"
                    self.img = 0
                    self.ticks = 0
                    self._roll_acc_px = 0.0
                    self.roll_moved_px = 0.0

            elif events.key == pygame.K_SPACE:
                if self.on_ground and not self.blocking and not self.rolling:
                    self.vel = self.jump_power
                    self.on_ground = False
                    self.is_jumping = True
                    self.state = "jump"

            elif events.key == pygame.K_q:
                if self.blocking:
                    return  # opcional: impedir ataque durante bloqueio
                if crouch_mod or self.crouching:
                    self.state = "c_shot"
                else:
                    self.state = "shot"
                self.shot()

            elif events.key == pygame.K_e:
                if self.dialog_npc:
                    self.start_dialogue(self.dialog_npc)

        elif events.type == pygame.KEYUP:
            if events.key in (pygame.K_d, pygame.K_RIGHT):
                self.right = False
            elif events.key in (pygame.K_a, pygame.K_LEFT):
                self.left = False
            elif events.key in (pygame.K_s, pygame.K_DOWN):
                self.crouching = False
                self.state = "block" if self.blocking else "idle"
            elif events.key == pygame.K_k:
                self.blocking = False
                if self.state.startswith("block"):
                    self.state = "idle"
            elif events.key == pygame.K_q:
                # Soltou Q: se ainda agachado, volta para down; senão, idle
                if self.crouching:
                    self.state = "down"
                else:
                    self.state = "idle"

    # -------------------------------
    # Movimentação lateral
    # -------------------------------
    def movements(self):
        screen_width = 1280
        buffer = 75

        # não anda em estados “ocupados”
        if self.state in ("shot", "c_shot", "block", "c_block", "roll", "dead") or self.blocking:
            return

        # agachado parado (idle agachado)
        if self.crouching and not self.left and not self.right and not self.is_jumping:
            if not self.animations["down"]:
                self._ensure_anim("c_idle", "R_D", 1)
                self.animations["down"] = self.animations["c_idle"]
            self.state = "down"
            frames_down = max(1, len(self.animations.get("down", [])))
            self.animate("down", 100, frames_down)
            return

        # andar para a direita
        if self.right:
            next_x = self.rect.x + 2.8

            if self.in_hole:
                if self.fall_lock_x_range and next_x + self.rect.width <= self.fall_lock_x_range[1]:
                    self.rect.x = next_x
            else:
                if getattr(self, "exit_mode", False):
                    # saída liberada: não aplica buffer, deixa atravessar
                    self.rect.x = next_x
                else:
                    if next_x + self.rect.width - buffer < screen_width:
                        self.rect.x = next_x

            if self.rect.x + self.rect.width - buffer < screen_width:
                self.facing_right = True

            self.state = "walk"
            self.animate("walk", 15, 7)

        # andar para a esquerda
        elif self.left:
            next_x = self.rect.x - 2.8
            if self.in_hole:
                if self.fall_lock_x_range and next_x >= self.fall_lock_x_range[0]:
                    self.rect.x = next_x
            else:
                if next_x + buffer > 0:
                    self.rect.x = next_x
            if self.rect.x + buffer > 0:
                self.facing_right = False
            self.state = "walk"
            self.animate("walk", 15, 7)

        # parado em pé
        else:
            self.state = "idle"
            self.animate("idle", 100, 1)

        # pulo (jump já tem listas esquerda/direita)
        if self.is_jumping:
            direction_anim = "jump_right" if self.facing_right else "jump_left"
            self.animate(direction_anim, 50, 17)

    # -------------------------------
    # Animação + gatilhos
    # -------------------------------
    def animate(self, name, ticks, limit):
        # avanço de frame por “ticks”
        self.ticks += 1
        if self.ticks >= ticks:
            self.ticks = 0
            self.img += 1

        frames = self.animations.get(name, [])
        num_frames = len(frames)
        if num_frames == 0:
            return

        if self.img >= num_frames:
            self.img = 0

        # aplica quadro
        self.image = frames[self.img]
        self.rect = self.image.get_rect(topleft=self.rect.topleft)

        # dispara flecha no frame 4 em QUALQUER animação com "shot" no nome
        if "shot" in name and self.img == 4 and not self.shot_released:
            self.real_shot()
            self.shot_released = True

        # libera novo disparo ao fim do ciclo
        if self.img >= num_frames - 1 and "shot" in name:
            self.shot_released = False

        # ---- FLIP CENTRALIZADO ----
        # Só flipamos para animações que NÃO têm variação left/right própria
        if name in self._dirless:
            if not self.facing_right:
                self.image = pygame.transform.flip(self.image, True, False)

    # -------------------------------
    # Tiro
    # -------------------------------
    def shot(self):
        """Inicia animação de ataque (o spawn real ocorre no frame 4 em animate)."""
        self.current_frame = 0
        if self.state == "c_shot":
            self.animate("c_shot", 25, 6)
        else:
            self.animate("shot", 25, 6)
        self.shot_released = False

    def real_shot(self):
        """Instancia o projétil com offsets/velocidade por postura."""
        stance = "crouch" if (self.crouching or self.state == "c_shot") else "stand"
        side = "right" if self.facing_right else "left"
        dx, dy = self.shot_offsets[stance][side]
        speed = self.shot_speed.get(stance, 7)

        shot_x = self.rect.x + dx
        shot_y = self.rect.y + dy
        direction = 1 if self.facing_right else -1

        shot = Shot(shot_x, shot_y, direction, self.shots, size=(80, 25), speed=speed)
        self.shots.add(shot)

    # -------------------------------
    # Diálogo
    # -------------------------------
    def start_dialogue(self, npc):
        self.dialog_active = True
        print(f"{npc.__class__.__name__}: Bem-vindo, jovem guerreiro! O que procura?")
        self.is_moving = False

    def stop_dialogue(self):
        self.dialog_active = False
        self.is_moving = True
        print("Diálogo finalizado.")

    # -------------------------------
    # Vida / morte
    # -------------------------------
    def check_death(self):
        # morte ao cair além da base
        if self.rect.y > BASE_HEIGHT:
            self.lives -= 1
            print(f"[DEBUG] Morreu. Vidas restantes: {self.lives}")
            if self.lives > 0:
                # respawn
                self.rect.x, self.rect.y = 100, 250
                self.vel = 0
                self.on_ground = False
                self.is_jumping = False
                self.in_hole = False
                self.state = "idle"
                return True
            else:
                self.die()
                return False
        return False

    def lose_life(self):
        self.lives -= 1
        if self.lives <= 0:
            self.die()

    def die(self):
        self.is_dead = True
        self.state = "dead"
        self.img = 0
        self.ticks = 0