
import pygame
import sys
import traceback

from script.scenes.auth.login import Login
from script.scenes import *        # Title, Map, Level, etc.
from script.setting import *       # BASE_WIDTH, BASE_HEIGHT, FPS...
from script.core.obj import *           # Player, HUD, etc. (se usado indiretamente pelas cenas)
from script.controller import Controller
from script.layer_anim import *    # se usado em cenas


class Game: 
    def __init__(self):
        # --- Inicialização base ---
        pygame.init()
        pygame.mixer.init()

        # --- Ícone e título (tolerante a falhas) ---
        try:
            icon = pygame.image.load("assets/menu/Icon.png")
            pygame.display.set_icon(icon)
        except Exception as e:
            print(f"[WARN] Ícone não carregado: {e}")

        pygame.display.set_caption("Guardiões de Pindorama")

        # --- Janela principal (redimensionável) ---
        flags = pygame.RESIZABLE | pygame.DOUBLEBUF
        self.display = pygame.display.set_mode((BASE_WIDTH, BASE_HEIGHT), flags)

        # --- Tela virtual (mantém proporção fixa, ex.: 1280x720) ---
        self.virtual_screen = pygame.Surface((BASE_WIDTH, BASE_HEIGHT))

        # --- Clock / FPS ---
        self.clock = pygame.time.Clock()

        # --- Estado de tela cheia ---
        self.fullscreen = False

        # --- Cena inicial ---
        self.scene = Login()
        if hasattr(self.scene, "on_enter"):
            try:
                self.scene.on_enter()
            except Exception as e:
                print(f"[WARN] Erro em scene.on_enter(): {e}")

        # --- Controle (joystick) ---
        self.controller = Controller()

        # (Opcional) Otimizar fila de eventos permitidos
        # pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP, pygame.JOYAXISMOTION,
        #                           pygame.JOYBUTTONDOWN, pygame.JOYBUTTONUP, pygame.VIDEORESIZE])

    def toggle_fullscreen(self):
        """Alterna janela <-> fullscreen, preservando flags adequados."""
        if self.fullscreen:
            flags = pygame.RESIZABLE | pygame.DOUBLEBUF
            self.display = pygame.display.set_mode((BASE_WIDTH, BASE_HEIGHT), flags)
            self.fullscreen = False
        else:
            # Fullscreen “nativo”; mantemos a tela virtual + letterboxing para preservar proporção.
            self.display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.DOUBLEBUF)
            self.fullscreen = True

    def switch_scene_if_needed(self):
        """Gerencia troca de cenas com hooks (on_exit/on_enter) e validação básica."""
        if not self.scene:
            return

        next_scene = getattr(self.scene, "next", None)
        if next_scene and next_scene is not self.scene:
            # Hook de saída
            if hasattr(self.scene, "on_exit"):
                try:
                    self.scene.on_exit()
                except Exception as e:
                    print(f"[WARN] Erro em scene.on_exit(): {e}")

            # Troca
            self.scene = next_scene

            # Hook de entrada da nova cena
            if hasattr(self.scene, "on_enter"):
                try:
                    self.scene.on_enter()
                except Exception as e:
                    print(f"[WARN] Erro em nova_scene.on_enter(): {e}")

    def run(self):
        try:
            while True:
                # --- dt em segundos (p/ movimento e animações consistentes) ---
                dt = self.clock.tick(FPS) / 1000.0  # limita e já retorna delta

                # (Opcional) Atualizações do controlador por frame (poll de eixos etc.)
                if hasattr(self.controller, "update"):
                    try:
                        self.controller.update()
                    except Exception as e:
                        print(f"[WARN] Controller.update() falhou: {e}")

                # --- Processa eventos ---
                for event in pygame.event.get():
                    # Fecha na cruz da janela
                    if event.type == pygame.QUIT:
                        return  # sai do loop principal

                    # F11 -> alternar fullscreen
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
                        self.toggle_fullscreen()
                        continue  # evita enviar esse evento para a cena

                    # 🎮 Traduz joystick -> teclado (quando aplicável)
                    try:
                        controller_event = self.controller.process_event(event)
                    except Exception as e:
                        print(f"[WARN] Controller.process_event falhou: {e}")
                        controller_event = None

                    # Usa o evento traduzido, se existir
                    effective_event = controller_event or event

                    # Repassa para a cena atual
                    if self.scene and hasattr(self.scene, "handle_events"):
                        try:
                            self.scene.handle_events(effective_event)
                        except Exception as e:
                            print(f"[WARN] Erro em scene.handle_events: {e}")

                # --- Atualiza lógica da cena ---
                if self.scene and hasattr(self.scene, "update"):
                    try:
                        # Passe dt para permitir movimentos/anim. frame-rate independentes
                        # (Se sua implementação atual não aceita dt, ignore o argumento.)
                        self.scene.update(dt) if self.scene.update.__code__.co_argcount >= 2 else self.scene.update()
                    except Exception as e:
                        print(f"[WARN] Erro em scene.update: {e}")

                # --- Desenho ---
                self.virtual_screen.fill("black")
                if self.scene and hasattr(self.scene, "draw"):
                    try:
                        self.scene.draw(self.virtual_screen)
                    except Exception as e:
                        print(f"[WARN] Erro em scene.draw: {e}")

                # --- Troca de cena (se solicitado pela cena) ---
                self.switch_scene_if_needed()

                # --- Letterboxing (centraliza a tela virtual) ---
                current_width, current_height = self.display.get_size()
                scale = min(current_width / BASE_WIDTH, current_height / BASE_HEIGHT)
                new_w, new_h = int(BASE_WIDTH * scale), int(BASE_HEIGHT * scale)
                offset_x = (current_width - new_w) // 2
                offset_y = (current_height - new_h) // 2

                scaled = pygame.transform.scale(self.virtual_screen, (new_w, new_h))
                self.display.fill("black")
                self.display.blit(scaled, (offset_x, offset_y))

                pygame.display.flip()

        except SystemExit:
            # Encerramento normal (ex.: return no loop)
            pass

        except Exception:
            print("\n[ERRO FATAL NO GAME LOOP]")
            traceback.print_exc()
            pygame.time.delay(1200)

        finally:
            pygame.quit()
            sys.exit()


# --- Bootstrap ---
if __name__ == "__main__":
    game = Game()
    game.run()
