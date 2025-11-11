import pygame
from script.setting import BASE_WIDTH, BASE_HEIGHT, BLUE_COLOR
from script.game_state import STATE

class PauseInventoryOverlay:
    """
    Classe responsável por exibir o menu de pausa/inventário
    sobre a cena atual do jogo.

    Contém três opções principais:
      - Retomar (volta ao jogo)
      - Escambo (abre loja)
      - Menu Inicial (retorna ao título e reseta o progresso)
    """

    def __init__(self, parent_scene, font, on_resume, on_shop, on_main_menu):
        # Referência para a cena "pai" (Level, Map, etc.)
        self.parent_scene = parent_scene

        # Caminho da fonte principal usada no menu
        primitive_path = "assets/font/Primitive.ttf"

        # Fonte principal (para títulos e opções)
        self.font = font or pygame.font.Font(primitive_path, 36)
        # Fonte menor (para inventário e subtítulos)
        self.small_font = pygame.font.Font(primitive_path, 24)

        # Callbacks (funções passadas pela cena principal)
        self.on_resume = on_resume        # Chamado ao escolher "Retomar"
        self.on_shop = on_shop            # Chamado ao escolher "Escambo"
        self.on_main_menu = on_main_menu  # Chamado ao escolher "Menu Inicial"

        # Opções do menu
        self.options = ["Retomar", "Escambo (Loja)", "Menu Inicial"]
        self.selected = 0  # índice da opção atualmente selecionada

        # Transparência do fundo escurecido
        self.bg_alpha = 180

        # Cria uma superfície de fallback segura, evitando erro de None
        surf = self.parent_scene.display or pygame.display.get_surface()
        if surf is None:
            # Se não existir nenhuma superfície, cria uma padrão
            surf = pygame.display.set_mode((BASE_WIDTH, BASE_HEIGHT))
            self.parent_scene.display = surf

        # Dimensões do painel
        W, H = surf.get_size()
        self.panel_width = int(W * 0.6)
        self.panel_height = int(H * 0.65)

        # Título do painel
        self.title_text = "Inventário & Pausa"

        # Carrega os itens do inventário (por enquanto, valores de exemplo)
        self.inventory_items = self._read_inventory()

    # -----------------------------------------------------------
    # Função auxiliar para simular o inventário do jogador
    # (você pode integrar com seu sistema real futuramente)
    # -----------------------------------------------------------
    def _read_inventory(self):
        return [
            {"nome": "Poção de Cura", "qtd": 2},
            {"nome": "Cogumelo de Energia", "qtd": 1},
            {"nome": "Flecha de Taquara", "qtd": 18},
            {"nome": "Moedas", "qtd": 37},
        ]

    # -----------------------------------------------------------
    # Captura e trata eventos de teclado dentro do overlay
    # -----------------------------------------------------------
    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_w):
                # Move seleção para cima
                self.selected = (self.selected - 1) % len(self.options)
                print(f"[DEBUG] Opção selecionada (↑): {self.options[self.selected]}")
                self.parent_scene.sound_click.play()

            elif event.key in (pygame.K_DOWN, pygame.K_s):
                # Move seleção para baixo
                self.selected = (self.selected + 1) % len(self.options)
                print(f"[DEBUG] Opção selecionada (↓): {self.options[self.selected]}")
                self.parent_scene.sound_click.play()

            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                # Confirma a opção atual
                self._activate_selected()

            elif event.key == pygame.K_ESCAPE:
                # ESC também retoma o jogo
                self.on_resume()

    # -----------------------------------------------------------
    # Executa a ação da opção selecionada
    # -----------------------------------------------------------
    def _activate_selected(self):
        """
        Executa a ação correspondente à opção selecionada.
        """
        option = self.options[self.selected]

        # 🟢 Retomar → fecha o menu e volta ao jogo
        if option == "Retomar":
            self.on_resume()

        # 🟠 Escambo → abre a loja
        elif option == "Escambo (Loja)":
            self.on_shop()

        # 🔴 Menu Inicial → limpa o progresso e volta ao título
        elif option == "Menu Inicial":
            try:
                # Limpa completamente o estado do jogo
                STATE.reset()
                print("[INFO] Progresso do jogo foi resetado. Retornando ao Menu Inicial.")

                # (Opcional) apagar save temporário, se existir
                # import os
                # if os.path.exists("save/temp_save.json"):
                #     os.remove("save/temp_save.json")

            except Exception as e:
                print(f"[ERRO] Falha ao resetar o estado do jogo: {e}")

            # Chama a função que leva de volta à tela inicial
            self.on_main_menu()

    # -----------------------------------------------------------
    # Atualização (placeholder para futuras animações)
    # -----------------------------------------------------------
    def update(self):
        pass

    # -----------------------------------------------------------
    # Desenha o overlay na tela
    # -----------------------------------------------------------
    def draw(self, display):
        try:
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

            # Áreas internas
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

            # 🧱 Bloco esquerdo: Inventário
            inv_title = self.small_font.render("Inventário", True, (210, 210, 210))
            display.blit(inv_title, (left_rect.x, left_rect.y))
            y = left_rect.y + 30
            for item in self.inventory_items:
                line = f"- {item['nome']} x{item['qtd']}"
                line_surf = self.small_font.render(line, True, (230, 230, 230))
                display.blit(line_surf, (left_rect.x + 8, y))
                y += 26

            # 🧭 Bloco direito: Opções
            opt_title = self.small_font.render("Opções", True, (210, 210, 210))
            display.blit(opt_title, (right_rect.x, right_rect.y))
            y = right_rect.y + 36

            for idx, opt in enumerate(self.options):
                selected = (idx == self.selected)
                color = BLUE_COLOR if selected else (100, 100, 100)

                # Texto da opção
                opt_surf = self.font.render(opt, True, color)
                display.blit(opt_surf, (right_rect.x + 8, y))

                # Setinha de seleção
                if selected:
                    arrow = self.font.render("▶", True, color)
                    display.blit(arrow, (right_rect.x - 36, y))

                y += 48

        except Exception:
            import traceback
            traceback.print_exc()
            # Caso haja erro no desenho, fecha o overlay para evitar travamento
            self.on_resume()