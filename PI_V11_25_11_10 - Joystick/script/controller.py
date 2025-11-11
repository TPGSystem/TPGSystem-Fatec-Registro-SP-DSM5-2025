import pygame
import time

class Controller:
    """
    Controller compatível com Xbox 360/XOne e PS4 (DualShock 4), com:
      - Mapeamento de botões -> teclas
      - D-Pad via HAT (Xbox) e via botões (PS4)
      - Suporte a analógico esquerdo -> setas (deadzone + auto-repeat)
      - Hotplug (conectar/desconectar em tempo de execução)

    Funcionalidades mapeadas:
      - Direcional (↑ ↓ ← →)
      - Ataque → Q
      - Pulo → Espaço
      - Defesa → K
      - Roll/Dash → Shift Esquerdo
      - Interagir → E
      - Share → Esc
      - Options → Enter
    """

    # ===== Configs gerais =====
    DEADZONE = 0.35           # zona morta para analógicos
    REPEAT_DELAY = 0.25       # atraso antes de repetir (seg)
    REPEAT_RATE = 0.12        # intervalo entre repetições (seg)

    def __init__(self, debug=False):
        self.debug = debug

        pygame.joystick.init()
        self.joystick = None
        self.button_map = {}
        self.dpad_map = {}
        self.uses_hat = False

        # Estados para D-Pad e analógico (evitar flood)
        self.dpad_state = {"up": False, "down": False, "left": False, "right": False}

        # Estados de auto-repeat para setas (analógico)
        self.axis_hold = {
            "left":  {"active": False, "t_first": 0.0, "t_next": 0.0},
            "right": {"active": False, "t_first": 0.0, "t_next": 0.0},
            "up":    {"active": False, "t_first": 0.0, "t_next": 0.0},
            "down":  {"active": False, "t_first": 0.0, "t_next": 0.0},
        }

        self._init_first_joystick()

    # ===== Inicialização e hotplug =====
    def _init_first_joystick(self):
        count = pygame.joystick.get_count()
        if count > 0:
            self._attach_joystick(0)
        else:
            print("[JOYSTICK] Nenhum controle encontrado")

    def _attach_joystick(self, index):
        try:
            self.joystick = pygame.joystick.Joystick(index)
            self.joystick.init()
            name = self.joystick.get_name()
            print(f"[JOYSTICK] Detectado: {name}")

            # Heurística simples de identificação
            name_l = (name or "").lower()
            if "wireless controller" in name_l or "dualshock" in name_l or "ps4" in name_l or "sony" in name_l:
                self._map_ps4()
            else:
                self._map_xbox()

            if self.debug:
                self._print_caps()

        except Exception as e:
            print(f"[JOYSTICK] Falha ao inicializar joystick {index}: {e}")
            self.joystick = None

    def _detach_joystick(self):
        if self.joystick:
            try:
                name = self.joystick.get_name()
                self.joystick.quit()
                print(f"[JOYSTICK] Desconectado: {name}")
            except Exception:
                pass
        self.joystick = None

    def _print_caps(self):
        if not self.joystick:
            return
        print(
            f"[JOYSTICK] Buttons={self.joystick.get_numbuttons()} "
            f"Hats={self.joystick.get_numhats()} "
            f"Axes={self.joystick.get_numaxes()}"
        )

    # ===== Mapas =====
    def _map_xbox(self):
        """Mapeamento padrão para Xbox 360/One."""
        self.button_map = {
            0: pygame.K_SPACE,    # A -> Pulo
            1: pygame.K_LSHIFT,   # B -> Roll/Dash
            2: pygame.K_q,        # X -> Ataque
            3: pygame.K_k,        # Y -> Defesa
            4: pygame.K_e,        # LB -> Interagir
            6: pygame.K_ESCAPE,   # Back -> Esc
            7: pygame.K_RETURN,   # Start -> Enter
            # (5=RB, 8=LS, 9=RS se quiser mapear depois)
        }
        # D-Pad via HAT
        self.dpad_map = {"hat": True}
        self.uses_hat = True
        print("[MAPEAMENTO] Xbox carregado")

    def _map_ps4(self):
        """
        Mapeamento do DualShock 4.
        Observação: índices podem variar por SO/driver. Ative debug=True para imprimir eventos e ajustar se necessário.
        """
        self.button_map = {
            0: pygame.K_SPACE,      # Cross (X) → Espaço (Pulo)
            1: pygame.K_LSHIFT,     # Circle (O) → Roll/Dash
            2: pygame.K_q,          # Square (☐) → Ataque
            3: pygame.K_k,          # Triangle (Δ) → Defesa
            4: pygame.K_ESCAPE,     # Share → Esc
            6: pygame.K_RETURN,     # Options → Enter
            9: pygame.K_e,          # L1 → Interagir (corrigido)
        }
        # D-Pad via BOTÕES (11–14)
        self.dpad_map = {
            11: pygame.K_UP,
            12: pygame.K_DOWN,
            13: pygame.K_LEFT,
            14: pygame.K_RIGHT,
        }
        self.uses_hat = False
        print("[MAPEAMENTO] PS4 carregado")

    # ===== Envio de teclas =====
    def _post_key(self, key, down: bool):
        if key is None:
            return
        evt_type = pygame.KEYDOWN if down else pygame.KEYUP
        pygame.event.post(pygame.event.Event(evt_type, {"key": key}))

    # ===== Eventos -> teclado =====
    def process_event(self, event):
        """Converte eventos do pygame em teclas. Retorna None (usa post)."""

        # Hotplug
        if event.type == pygame.JOYDEVICEADDED:
            # Conecta o primeiro disponível se não houver joystick
            if not self.joystick:
                self._attach_joystick(event.device_index)
            return None

        if event.type == pygame.JOYDEVICEREMOVED:
            # Se o removido é o atual, detach
            if self.joystick and event.instance_id == self.joystick.get_instance_id():
                self._detach_joystick()
            return None

        # Sem joystick -> nada a fazer
        if not self.joystick:
            return None

        # D-Pad por botões (PS4 em vários drivers)
        if event.type in (pygame.JOYBUTTONDOWN, pygame.JOYBUTTONUP):
            if event.button in self.dpad_map:
                key = self.dpad_map[event.button]
                self._post_key(key, event.type == pygame.JOYBUTTONDOWN)
                return None

            if event.button in self.button_map:
                self._post_key(self.button_map[event.button], event.type == pygame.JOYBUTTONDOWN)
                return None

            if self.debug:
                print(f"[JOY BTN] idx={event.button} down={event.type==pygame.JOYBUTTONDOWN}")

        # D-Pad via HAT (Xbox)
        if self.uses_hat and event.type == pygame.JOYHATMOTION:
            hat_x, hat_y = event.value
            # Cima
            if hat_y == 1 and not self.dpad_state["up"]:
                self._post_key(pygame.K_UP, True)
                self.dpad_state["up"] = True
            if hat_y != 1 and self.dpad_state["up"]:
                self._post_key(pygame.K_UP, False)
                self.dpad_state["up"] = False
            # Baixo
            if hat_y == -1 and not self.dpad_state["down"]:
                self._post_key(pygame.K_DOWN, True)
                self.dpad_state["down"] = True
            if hat_y != -1 and self.dpad_state["down"]:
                self._post_key(pygame.K_DOWN, False)
                self.dpad_state["down"] = False
            # Esquerda
            if hat_x == -1 and not self.dpad_state["left"]:
                self._post_key(pygame.K_LEFT, True)
                self.dpad_state["left"] = True
            if hat_x != -1 and self.dpad_state["left"]:
                self._post_key(pygame.K_LEFT, False)
                self.dpad_state["left"] = False
            # Direita
            if hat_x == 1 and not self.dpad_state["right"]:
                self._post_key(pygame.K_RIGHT, True)
                self.dpad_state["right"] = True
            if hat_x != 1 and self.dpad_state["right"]:
                self._post_key(pygame.K_RIGHT, False)
                self.dpad_state["right"] = False

            return None

        return None

    # ===== Poll contínuo (analógico esquerdo -> setas, com auto-repeat) =====
    def update(self):
        """Chamar a cada frame (antes da cena atualizar) para mapear analógico -> setas."""
        if not self.joystick:
            return

        now = time.time()

        # Eixos típicos: 0 = LX, 1 = LY (inverter Y p/ cima = negativo)
        try:
            lx = self.joystick.get_axis(0)
            ly = self.joystick.get_axis(1)
        except Exception:
            return

        # Horizontal
        self._axis_repeat_logic(axis_value=lx, neg_key=pygame.K_LEFT, pos_key=pygame.K_RIGHT,
                                neg_name="left", pos_name="right", now=now)

        # Vertical (nota: ly<0 = UP, ly>0 = DOWN)
        self._axis_repeat_logic(axis_value=-ly, neg_key=pygame.K_DOWN, pos_key=pygame.K_UP,
                                neg_name="down", pos_name="up", now=now)

    def _axis_repeat_logic(self, axis_value, neg_key, pos_key, neg_name, pos_name, now):
        """
        Se axis_value < -DEADZONE => direção negativa (ex.: esquerda ou baixo)
        Se axis_value >  +DEADZONE => direção positiva (ex.: direita ou cima)
        Gera KEYDOWN uma vez, depois repeats em REPEAT_RATE, e KEYUP ao sair da zona.
        """
        # Decide direção
        if axis_value <= -self.DEADZONE:
            self._handle_axis_direction(name=neg_name, key=neg_key, now=now)
            # Garantir que a direção oposta solte
            self._release_axis_direction(name=pos_name, key=pos_key)
        elif axis_value >= self.DEADZONE:
            self._handle_axis_direction(name=pos_name, key=pos_key, now=now)
            self._release_axis_direction(name=neg_name, key=neg_key)
        else:
            # Centro -> solta ambas
            self._release_axis_direction(name=neg_name, key=neg_key)
            self._release_axis_direction(name=pos_name, key=pos_key)

    def _handle_axis_direction(self, name, key, now):
        st = self.axis_hold[name]
        if not st["active"]:
            # Primeiro KEYDOWN
            st["active"] = True
            st["t_first"] = now
            st["t_next"] = now + self.REPEAT_DELAY
            self._post_key(key, True)
        else:
            # Auto-repeat
            if now >= st["t_next"]:
                self._post_key(key, True)
                st["t_next"] = now + self.REPEAT_RATE

    def _release_axis_direction(self, name, key):
        st = self.axis_hold[name]
        if st["active"]:
            st["active"] = False
            st["t_first"] = 0.0
            st["t_next"] = 0.0
            self._post_key(key, False)