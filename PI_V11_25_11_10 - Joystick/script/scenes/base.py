import pygame, sys, json  # Importa as bibliotecas necessárias
import random
from script.core.obj import *  # Importa todas as classes do módulo obj
from script.setting import *  # Importa todas as configurações do módulo setting
from script.layer_anim import LayerStack, StaticLayer, FlipLayer # Importa todas as configurações do módulo setting layer_anim
from script.game_state import STATE  # ← adiciona junto dos outros imports



# Criando Classes para estruturar o Jogo:
# Criando Cenas
class Fade:
    def __init__(self, color="black"):
        self.color = color
        self.alpha = 0
        self.enabled = False

    def update(self):
        if self.enabled:
            self.alpha = min(255, self.alpha + 5)

    def draw(self, display):
        if self.enabled and self.alpha > 0:
            W, H = display.get_size()
            #s = pygame.Surface((W, H), pygame.SRCALPHA)
            #s.fill((0, 0, 0, self.alpha))
            #display.blit(s, (0, 0))


class PauseInventoryOverlay:
    """
    Overlay de pausa/inventário que desenha por cima da cena.
    Opções:
      - Retomar
      - Escambo (Loja)
      - Menu Inicial
    """
    def __init__(self, parent_scene, font, small_font, on_resume, on_shop, on_main_menu):
        self.parent_scene = parent_scene
        self.font = font
        self.small_font = small_font
        self.on_resume = on_resume
        self.on_shop = on_shop
        self.on_main_menu = on_main_menu

        self.options = ["Retomar", "Escambo (Loja)", "Menu Inicial"]
        self.selected = 0

        # Visual
        self.bg_alpha = 180  # opacidade do fundo escuro
        W, H = self.parent_scene.display.get_size()
        self.panel_width = int(W * 0.6)
        self.panel_height = int(H * 0.65)

        self.title_text = "Inventário & Pausa"
        # Tenta usar a mesma fonte com tamanho menor; se falhar, usa default.
        try:
            # Se a cena usou um caminho de fonte custom, reaproveite:
            self.small_font = pygame.font.Font(self.font.name, 24)  # type: ignore
        except Exception:
            self.small_font = pygame.font.Font(None, 24)

        # Integração com inventário real (substitua por player.inventory se tiver)
        self.inventory_items = self._read_inventory()

    def _read_inventory(self):
        # Placeholder: substitua pelo seu inventário real
        return [
            {"nome": "Poção de Cura", "qtd": 2},
            {"nome": "Cogumelo de Energia", "qtd": 1},
            {"nome": "Flecha de Taquara", "qtd": 18},
            {"nome": "Moedas", "qtd": 37},
        ]

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_w):
                self.selected = (self.selected - 1) % len(self.options)
                self.parent_scene.sound_click.play()
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self.selected = (self.selected + 1) % len(self.options)
                self.parent_scene.sound_click.play()
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                self._activate_selected()
            elif event.key == pygame.K_ESCAPE:
                self.on_resume()
                

    def _activate_selected(self):
        option = self.options[self.selected]
        if option == "Retomar":
            self.on_resume()
        elif option == "Escambo (Loja)":
            self.on_shop()
        elif option == "Menu Inicial":
            self.on_main_menu()

    def update(self):
        # espaço para animações futuras
        pass

    def draw(self, display):
        W, H = display.get_size()

        # Fundo escurecido semi-transparente
        dim = pygame.Surface((W, H), pygame.SRCALPHA)
        dim.fill((0, 0, 0, self.bg_alpha))
        display.blit(dim, (0, 0))

        # Painel central
        panel_rect = pygame.Rect(0, 0, self.panel_width, self.panel_height)
        panel_rect.center = (W // 2, H // 2)
        pygame.draw.rect(display, (30, 30, 30), panel_rect, border_radius=16)
        pygame.draw.rect(display, (200, 200, 200), panel_rect, width=2, border_radius=16)

        # Título
        title_surf = self.font.render(self.title_text, True, (240, 240, 240))
        title_rect = title_surf.get_rect(center=(panel_rect.centerx, panel_rect.top + 50))
        display.blit(title_surf, title_rect)

        # Colunas: à esquerda inventário, à direita opções
        padding = 28
        col_gap = 24

        left_rect = pygame.Rect(
            panel_rect.left + padding,
            title_rect.bottom + 20,
            int(self.panel_width * 0.55),
            panel_rect.bottom - (title_rect.bottom + 20) - padding
        )
        right_rect = pygame.Rect(
            left_rect.right + col_gap,
            left_rect.top,
            panel_rect.right - padding - (left_rect.right + col_gap),
            left_rect.height
        )

        # Inventário (lista simples)
        inv_title = self.small_font.render("Inventário", True, (210, 210, 210))
        display.blit(inv_title, (left_rect.x, left_rect.y))
        y = left_rect.y + 30
        for item in self.inventory_items:
            line = f"- {item['nome']} x{item['qtd']}"
            line_surf = self.small_font.render(line, True, (230, 230, 230))
            display.blit(line_surf, (left_rect.x + 8, y))
            y += 26

        # Opções
        opt_title = self.small_font.render("Opções", True, (210, 210, 210))
        display.blit(opt_title, (right_rect.x, right_rect.y))
        y = right_rect.y + 36
        for idx, opt in enumerate(self.options):
            selected = (idx == self.selected)
            color = (255, 255, 255) if selected else (200, 200, 200)
            opt_surf = self.font.render(opt, True, color)
            display.blit(opt_surf, (right_rect.x + 8, y))

            if selected:
                arrow = self.font.render("▶", True, color)
                display.blit(arrow, (right_rect.x - 36, y))
            y += 48


class Scene:
    """Classe base para todas as cenas do jogo."""
    
    def __init__(self, font_path="assets/font/Primitive.ttf", font_size=36):
        pygame.init()
        
        self.next = self                         # cena seguinte
        self.display = pygame.display.get_surface()
        self.all_sprites = pygame.sprite.Group()
        
        self.fade = Fade("black")                # efeito de fade
        self.sound_click = pygame.mixer.Sound("assets/sounds/click.ogg")
        self.sound_click.set_volume(0.25)
        
        self.option_data = self.load_file("teste.json")
        self.font = pygame.font.Font(font_path, font_size)

        # Controle de pausa/overlay
        self.paused = False
        self.overlay = None

    # ====== MENU DE PAUSA / INVENTÁRIO ======
    def open_pause_menu(self):
        """Cria e exibe o overlay de pausa/inventário com robustez."""
        
        from .base import PauseInventoryOverlay  # local
        from script.setting import FONT_BIG, FONT_SMALL
        
        try:
            if self.overlay is not None:
                return

            # garante um display válido
            if not self.display:
                self.display = pygame.display.get_surface()

            def on_resume():
                self.sound_click.play()
                self.overlay = None
                self.paused = False
                vol = self.option_data.get("music_set_volume")
                if vol is not None and pygame.mixer.get_init():
                    pygame.mixer.music.set_volume(vol)

            def on_shop():
                self.sound_click.play()
                self.change_scene(EscamboScene())

            def on_main_menu():
                # Sempre resetar o progresso global antes de voltar ao Título
                from script.game_state import STATE
                from .menus.title import Title  # import local
                STATE.reset()
                self.change_scene(Title())

            # cria o overlay com fallback seguro de fonte
            self.overlay = PauseInventoryOverlay(
                parent_scene=self,
                font=FONT_BIG,
                small_font=FONT_SMALL,
                on_resume=on_resume,
                on_shop=on_shop,
                on_main_menu=on_main_menu
            )
            self.paused = True

            vol = self.option_data.get("music_set_volume")
            if vol is not None and pygame.mixer.get_init():
                pygame.mixer.music.set_volume(vol * 0.4)
        except Exception:
            import traceback; traceback.print_exc()
            # se der algo errado, não derrube o jogo: apenas desfaz o pause
            self.overlay = None
            self.paused = False

    def start_music(self):
        """Inicia música com checagens seguras."""
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            vol = self.option_data.get("music_set_volume", 0)
            pygame.mixer.music.load("assets/sounds/music1.mp3")
            if vol:
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(vol)
        except Exception:
            import traceback; traceback.print_exc()

    # ====== EVENTOS ======
    def handle_events(self, event):
        # se overlay ativo → ele consome os eventos e pronto
        if self.overlay:
            self.overlay.handle_events(event)
            return

        # abre com ESC
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.open_pause_menu()
            return
        # Subclasses tratam o resto

    # ====== DESENHO ======
    def draw(self, display):
        """Desenha sprites, fade e overlay."""
        self.all_sprites.draw(display)
        self.fade.draw(display)

        if self.overlay:
            self.overlay.draw(display)

    # ====== UPDATE ======
    def update(self):
        """Atualiza sprites, fade ou overlay."""
        if not self.paused:
            self.all_sprites.update()
            self.fade.update()
        else:
            if self.overlay:
                self.overlay.update()

    # ====== TROCA DE CENA ======
    def change_scene(self, next_scene):
        self.next = next_scene

    # ====== SALVAR / CARREGAR ======
    def save_file(self, arquivo, dados):
        with open(arquivo, "w") as dados_do_arquivo:
            json.dump(dados, dados_do_arquivo)
            print("OK")

    def load_file(self, arquivo):
        with open(arquivo, "r") as dados_do_arquivo:
            dados = json.load(dados_do_arquivo)
        return dados


# ====== CENAS DE PLACEHOLDER ======
class EscamboScene(Scene):
    def draw(self, display):
        super().draw(display)
        txt = self.font.render("ESCAMBO / LOJA (placeholder)", True, (255, 255, 0))
        display.blit(txt, (50, 50))


class MenuInicialScene(Scene):
    def draw(self, display):
        super().draw(display)
        txt = self.font.render("MENU INICIAL (placeholder)", True, (255, 255, 0))
        display.blit(txt, (50, 50))
