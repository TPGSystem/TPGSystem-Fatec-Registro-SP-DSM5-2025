import pygame, random
from ..base import Scene, PauseInventoryOverlay
from .level_base import Level
from script.core.obj import Obj
from script.world.ground import Ground
from script.actors.player import Player
from script.ui.hud import Hud
from script.combat.projectiles import Shot
from script.actors.bosses.mapinguari import Boss_Mapinguari
from script.ui.boss_hud import BossHud
from script.layer_anim import LayerStack, StaticLayer, FlipLayer
from script.setting import *
from script.game_state import STATE
from script.data.dialogs.dialog_1_1 import Dialogo_1_1
from script.data.quizzes.questions_1_1 import Questoes_1_1
from ..map.map_scene import Map
from ..gameover import GameOver


# Criando Tela de Nível
class Level_1_2(Level):
    """Classe para a tela de nível."""
    
    def __init__(self, player_data=None, hud_data=None): 
        super().__init__(player_data, hud_data)

        # Criação do chão
        self.ground = Ground(0, 400, 800, 20)
        self.all_sprites.add(self.ground)
        
        self.layers = LayerStack()

        # Fundo da fase
        #self.img = Obj("assets/levelSprite/level_1_2.png", [0, 0], [self.all_sprites])
        self.hudbk = Hud("assets/charsSprite/player/Hud/Hud_Char_Fundo.png", [25, 25], [self.all_sprites], (640, 360))
        
        # --- BOSS: Mapinguari (5 de vida) ---
        self.boss = Boss_Mapinguari([850, 100], [self.all_sprites], size=(400, 400))
        self.boss.life = 5            # redundante se o Boss já inicia com 5, mas deixo explícito
        self.boss.max_life = 5
        
        
        # --- HUD do Boss (mostra 5→0) ---
        # Posição/tamanho exemplo; ajuste se precisar alinhar com seu layout
        self.boss_hud = BossHud(position=(0,0), size=(1280, 720))
        self.boss_hud.set(self.boss.life)  # começa em 5

        # --- FLAGS/ESTADO DE MORTE DO BOSS ---
        self.boss_dying = False          # entrou na sequência de morte?
        self.boss_corpse = None          # Surface da imagem de cadáver (com alpha)
        self.boss_corpse_rect = None     # Rect para posicionar
        self.boss_corpse_alpha = 255     # começa opaco
        self.boss_corpse_fade_frames = 180   # ~3s @60fps
        self._boss_corpse_timer = 0

        # --- PRÉ-CARREGA A ARTE DO CADÁVER ---
        try:
            corpse_img = pygame.image.load(
                "assets/charsSprite/bosses/Mapinguari_D.png"
            ).convert_alpha()
            # escala para o mesmo tamanho do boss
            corpse_img = pygame.transform.scale(corpse_img, (400, 400))
            self.boss_corpse = corpse_img
        except Exception as e:
            print("[WARN] Não foi possível carregar Mapinguari_D.png:", e)
            self.boss_corpse = None
                
        
        # --- Amarra a HUD ao Boss: toda vez que a vida mudar, a HUD troca sozinha ---
        # (o Boss expõe 'on_life_change' que chamamos com o valor atual; se o seu Boss não tiver, removemos esta linha)
        if hasattr(self.boss, "on_life_change"):
            self.boss.on_life_change = self.boss_hud.set
            
        # (opcional) Debug
        print(f"[DEBUG] Boss criado com {self.boss.life} HP; HUD ajustada.")            
        
                
        # --- ADICIONE: Flags de Controle ---
        self.boss_defeated = False
        self.exit_enabled = False
                
        
        self.layers = LayerStack()
        
        # ---------- CAMADAS DO CENÁRIO (LEVEL_1_2) ----------
        base_path = "assets/levelSprite/"   # use este prefixo simples (imagens na raiz de levelSprite)

        # 1) FUNDO ABSOLUTO → BACK
        self.layers.add("level_1_2a",
            StaticLayer(f"{base_path}level_1_2a.png", z=0, plane="back", pos=(0,0))
        )

        # ==== Player / Boss são desenhados entre BACK e FRONT ====

        # 4) PAR INTERCALADO → FRONT (fica NA FRENTE do player/boss)
        #    ATENÇÃO: ajuste os nomes exatamente como estão nos arquivos:
        #    se seus arquivos são "level_1_2AA.png" (AA maiúsculo) e "level_1_2ab.png", use assim:
        flip_AA = f"{base_path}level_1_2AA.png"  # ou "level_1_2aa.png" se for tudo minúsculo
        flip_ab = f"{base_path}level_1_2ab.png"

        self.layers.add("level_1_2AA_ab",
            FlipLayer(flip_AA, flip_ab, fps=4.0, z=10, plane="front", pos=(0,0))
        )

        # 5) CAMADA FRONTAL ESTÁTICA → FRONT
        self.layers.add("level_1_2b",
            StaticLayer(f"{base_path}level_1_2b.png", z=20, plane="front", pos=(0,0))
        )

        # Relógio p/ delta-time das animações de layer
        self._layers_last_ticks = pygame.time.get_ticks()

        # Criação do jogador com dados recebidos da fase anterior
        if player_data:
            self.player = Player(
                image_path=player_data.get("image_path", "assets/charsSprite/player/indigenaM/R0.png"),
                position=player_data.get("position", [100, 250]),
                groups=[self.all_sprites],
                size=player_data.get("size", (200, 200)),
                life=player_data.get("life", 25),
                lives=player_data.get("lives", 3),
                xp=player_data.get("xp", 0)
            )
        else:
            self.player = Player("assets/charsSprite/player/indigenaM/R0.png", [100, 250], [self.all_sprites], (200, 200))

        # Criação da HUD (sem valores ainda)
        self.hud = Hud("assets/charsSprite/player/Hud/Hud_Char_Contorno.png", [25, 25], [self.all_sprites], (640, 360))
        
        # Atualiza a HUD com os dados recebidos da fase anterior (se houver)
        self.hud.life = self.player.life
        self.hud.lives = self.player.lives
        self.hud.xp = self.player.xp
        if hud_data:
            self.hud.gold = hud_data.get("gold", 0)

        print("[DEBUG] Player.lives ao entrar:", self.player.lives)
        print("[DEBUG] HUD.lives após update:", self.hud.lives)

        

        # Fonte e chatbox
        #font = pygame.font.Font(None, 30)
        self.chatbox = None
        # Forçar para valor que nunca entra no diálogo
        self.dialogue_stage = -1
        
        self.boss_name_font = pygame.font.Font("assets/font/Primitive.ttf", 28)  # Tamanho da fonte: 40
        self.boss_name_text = self.boss_name_font.render("Mapinguari", True, (0, 0, 0))  # Branco
        self.boss_name_pos = (880, 600)  # Posição no canto superior direito (ajuste conforme a tela)
        
        self.disable_auto_exit = True  # <- impede a lógica do Level base de rodar aqui

        # Controle de diálogo e questões
        self.dialogue = Dialogo_1_1.falas[:5]
        self.questions = Questoes_1_1.perguntas
        self.final_dialogue = Dialogo_1_1.falas[5:]
        self.current_question = 0
        self.dialogue_stage = 0
        self.dialogue_finished = False
        self.confirming_answer = False
        self.selected_option = None
        self.exit_enabled = False

        self.gold_reward = 0
        self.points_to_gold_conversion = 2

        self.questions = Questoes_1_1.perguntas[:]
        random.shuffle(self.questions)
        
        # Fonte de pausa
        self.font = FONT_BIG
           

    def handle_events(self, event):
        """Gerencia eventos de entrada do usuário na tela de nível (player e chatbox desacoplados)."""
        # 0) Overlay de pausa tem prioridade total
        if self.overlay:
            self.overlay.handle_events(event)
            return

        # 1) ESC abre o menu de pausa (e consome o evento)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.open_pause_menu()
            return

        # 2) SEMPRE repassar o evento para o Player primeiro
        #    (garante que setas/A-D/W-S etc. funcionem para o player independentemente de chatbox)
        if event.type in (pygame.KEYDOWN, pygame.KEYUP):
            self.player.events(event)

        # 3) Helpers seguros para chatbox
        def cb_exists() -> bool:
            return self.chatbox is not None

        def cb_active() -> bool:
            return cb_exists() and bool(getattr(self.chatbox, "active", False))

        def cb_has_options() -> bool:
            return cb_exists() and bool(getattr(self.chatbox, "options", []))

        # 4) Ações de diálogo (somente se você realmente estiver usando chatbox)
        if event.type == pygame.KEYDOWN:
            # 4.1) Iniciar diálogo (E perto do boss), com todas as checagens
            if (event.key == pygame.K_e
                and self.player.rect.colliderect(self.boss.rect)
                and cb_exists()
                and hasattr(self.chatbox, "is_active")
                and not self.chatbox.is_active()):
                if self.dialogue_stage == 0:
                    # formata falas iniciais
                    if hasattr(self.chatbox, "display_messages"):
                        formatted_dialogue = [f"{speaker}: {message}" for speaker, message in Dialogo_1_1.falas[:5]]
                        self.chatbox.display_messages(formatted_dialogue)
                        self.chatbox.active = True
                elif self.dialogue_stage == 2:
                    # limpa resíduos + mostra falas finais
                    if cb_exists():
                        if hasattr(self.chatbox, "options"):  self.chatbox.options = []
                        if hasattr(self.chatbox, "title"):    self.chatbox.title = ""
                        if hasattr(self.chatbox, "question"): self.chatbox.question = ""
                    if hasattr(self.chatbox, "display_messages"):
                        formatted_dialogue = [f"{speaker}: {message}" for speaker, message in self.final_dialogue]
                        self.chatbox.display_messages(formatted_dialogue)
                        self.chatbox.active = True

            # 4.2) Avançar diálogo / responder questão (Enter) — só se chatbox ativa
            elif event.key == pygame.K_RETURN and cb_active():
                if cb_has_options():
                    # respondendo questão
                    if hasattr(self.chatbox, "select_option"):
                        selected_option = self.chatbox.select_option()
                    else:
                        selected_option = None

                    current_question = self.questions[self.current_question]
                    if selected_option == current_question["resposta_correta"]:
                        print("Resposta correta!")
                        points = current_question.get("pontos", 0)
                        if points > 0:
                            gold_reward = points * self.points_to_gold_conversion
                            self.hud.update_gold(self.hud.gold + gold_reward)
                            print(f"Você ganhou {gold_reward} de gold!")
                        else:
                            print("Esta questão não tem pontos definidos.")
                    else:
                        print("Resposta errada.")

                    # próxima questão ou diálogo final
                    self.current_question += 1
                    if self.current_question < len(self.questions):
                        q = self.questions[self.current_question]
                        shuffled = q["opcoes"][:]
                        random.shuffle(shuffled)
                        if hasattr(self.chatbox, "display_question"):
                            self.chatbox.display_question(q["titulo"], q["pergunta"], shuffled)
                    else:
                        self.dialogue_stage = 2
                        if cb_exists():
                            if hasattr(self.chatbox, "options"):  self.chatbox.options = []
                            if hasattr(self.chatbox, "title"):    self.chatbox.title = ""
                            if hasattr(self.chatbox, "question"): self.chatbox.question = ""
                        if hasattr(self.chatbox, "display_messages"):
                            formatted_dialogue = [f"{speaker}: {message}" for speaker, message in self.final_dialogue]
                            self.chatbox.display_messages(formatted_dialogue)
                            self.chatbox.active = True
                else:
                    # avançar falas
                    if hasattr(self.chatbox, "next_message"):
                        self.chatbox.next_message()

                    # terminou falas iniciais -> começa perguntas
                    if (cb_exists() and
                        hasattr(self.chatbox, "current_message") and
                        hasattr(self.chatbox, "messages") and
                        self.chatbox.current_message >= len(self.chatbox.messages) and
                        self.dialogue_stage == 0):
                        self.dialogue_stage = 1
                        q = self.questions[self.current_question]
                        shuffled = q["opcoes"][:]
                        random.shuffle(shuffled)
                        if hasattr(self.chatbox, "display_question"):
                            self.chatbox.display_question(q["titulo"], q["pergunta"], shuffled)
                            self.chatbox.active = True

                    # terminou falas finais -> libera saída
                    elif (cb_exists() and
                        hasattr(self.chatbox, "current_message") and
                        hasattr(self.chatbox, "messages") and
                        self.chatbox.current_message >= len(self.chatbox.messages) and
                        self.dialogue_stage == 2):
                        self.chatbox.active = False
                        self.exit_enabled = True
                        
                        # quando liberar a saída, permite que o player atravesse a borda
                        setattr(self.player, "exit_mode", True)

            # 4.3) Navegação da chatbox com W/S (setas continuam livres para o Player)
            elif event.key == pygame.K_w and cb_has_options():
                if hasattr(self.chatbox, "previous_option"):
                    self.chatbox.previous_option()
            elif event.key == pygame.K_s and cb_has_options():
                if hasattr(self.chatbox, "next_option"):
                    self.chatbox.next_option()

            # 4.4) Confirmar também com Espaço ou E (além de Enter)
            elif event.key in (pygame.K_SPACE, pygame.K_e) and cb_active():
                if hasattr(self.chatbox, "confirm"):
                    self.chatbox.confirm()

            # 4.5) (Opcional) fechar chatbox com ESC
            elif event.key == pygame.K_ESCAPE and cb_exists():
                # se tiver um método próprio:
                if hasattr(self, "close_dialog"):
                    self.close_dialog()
                else:
                    # fallback seguro
                    self.chatbox = None

        # 5) deixe o restante da cadeia da cena (se necessário)
    #    return super().handle_events(event)
        
    def open_pause_menu(self):
        """Abre o menu de pausa com overlay de inventário."""
        if not self.overlay:
            from script.setting import FONT_BIG, FONT_SMALL  # ✅ deve importar aqui também
            self.overlay = PauseInventoryOverlay(
                parent_scene=self,
                font=FONT_BIG,
                small_font=FONT_SMALL,
                on_resume=self.on_resume,
                on_shop=self.on_shop,
                on_main_menu=self.on_main_menu
            )

    def on_resume(self):
        print("[DEBUG] Jogo retomado.")
        self.overlay = None

    def on_shop(self):
        print("[DEBUG] A funcionalidade de escambo ainda será implementada.")

    def on_main_menu(self):
        print("[DEBUG] Retornando ao menu principal e resetando progresso...")
        from script.game_state import STATE
        STATE.reset()
        from ..menus.title import Title
        self.change_scene(Title())    

    def update(self):
        # ---- delta-time para animações de layer ----
        now = pygame.time.get_ticks()
        dt = (now - getattr(self, "_layers_last_ticks", now)) / 1000.0
        self._layers_last_ticks = now
        self.layers.update(dt)
        # --------------------------------------------

        # HUD do player
        self.hud.update_life(self.player.life)
        self.hud.update_lives(self.player.lives)
        self.hud.update_xp(self.player.xp)

        # Atualizações padrões (groups etc.)
        super().update()

        # --- DANO NO BOSS: tiros com linha de impacto (multi-hitbox) ---
        if not self.boss_defeated:
            for shot in list(self.player.shots):
                # Atualiza o projétil passando o boss (agora ele detecta sozinho)
                shot.update(self.boss)

                # Se o projétil ainda existe (não matou o boss nem colidiu), continua
                if shot.alive():
                    continue

                # Se o projétil colidiu, a função take_damage() do boss já foi chamada internamente
                print(f"[DEBUG] Boss HP: {self.boss.life}/{self.boss.max_life}")

               # --- Derrota do boss ---
                if getattr(self.boss, "life", 0) <= 0 and not self.boss_dying:
                    self.boss_defeated = True
                    self.exit_enabled = True
                    setattr(self.player, "exit_mode", True)

                    # 1) trava HUD em 0 e troca retrato para o cadáver
                    self._boss_hud_use_death_portrait()

                    # 2) prepara o cadáver no chão
                    if self.boss_corpse:
                        self.boss_corpse_rect = self.boss_corpse.get_rect()
                        # ancora no pé do boss vivo
                        self.boss_corpse_rect.midbottom = self.boss.rect.midbottom
                        # ↓ desce o corpo (ajuste o valor)
                        self.boss_corpse_rect.y += 40   # 40 px mais baixo
                        # reset do fade/timer…
                        self._boss_corpse_timer = 0
                        self.boss_corpse_alpha = 255
                        self.boss_dying = True

                    # 3) remove sprite ativo
                    try:
                        self.boss.kill()
                    except Exception:
                        pass

                    print("[DEBUG] Boss derrotado! HUD travada com retrato de morte.")
                    break

        # --- Fade-out do cadáver (3s) ---
        if self.boss_dying and self.boss_corpse and self.boss_corpse_rect:
            self._boss_corpse_timer += 1
            step = int(255 / max(1, self.boss_corpse_fade_frames))
            self.boss_corpse_alpha = max(0, self.boss_corpse_alpha - step)

                
        # --- Sincroniza HUD do boss em todo frame (safety net) ---
        if not self.boss_defeated:
            self.boss_hud.set(getattr(self.boss, "life", 0))

        #--- Se a HUD chegou a 0, some com o boss e mantenha a HUD em 0 na tela ---
        if not self.boss_defeated and getattr(self.boss_hud, "value", 5) == 0:
            self.boss_defeated = True
            self.exit_enabled = True
            setattr(self.player, "exit_mode", True)  # deixa atravessar a borda

            # trava visualmente a HUD em 0
            self.boss_hud.set(0)

            # remove APENAS o sprite do boss
            if self.boss and self.boss.alive():
                self.boss.kill()

            print("[DEBUG] HUD=0 → Boss removido; HUD 0 permanece na tela.")

        # --- sair pela direita -> volta para o mapa e marca a área como concluída ---
        if self.exit_enabled and self.player.rect.right >= BASE_WIDTH + 200:
            STATE.complete_area("Level_1_2")  # use o helper do GameState
            print("[DEBUG] Área Level_1_2 marcada como concluída:", STATE.completed_areas)

            # import tardio evita ciclos
            from ..map.map_scene import Map
            self.change_scene(Map())
            return
        
        
        # Game Over
        if self.player.lives <= 0:
            self.change_scene(GameOver())


    def _boss_hud_use_death_portrait(self):
        """Mantém a HUD do boss mostrando o retrato de morte."""
        death_path = "assets/charsSprite/bosses/Mapinguari_D.png"
        # vida 0 travada
        try:
            self.boss_hud.set(0)
        except Exception:
            pass

        # retrato (método canônico, se existir)
        if hasattr(self.boss_hud, "set_portrait"):
            try:
                self.boss_hud.set_portrait(death_path)
                return
            except Exception:
                pass

        # fallback 1: se a HUD expõe 'portrait_path'
        if hasattr(self.boss_hud, "portrait_path"):
            try:
                self.boss_hud.portrait_path = death_path
            except Exception:
                pass

        # fallback 2: se expõe 'portrait_surface' e tamanho
        try:
            surf = pygame.image.load(death_path).convert_alpha()
            # se a HUD usar um tamanho específico, ajuste aqui:
            # ex.: surf = pygame.transform.scale(surf, (w, h))
            if hasattr(self.boss_hud, "portrait_surface"):
                self.boss_hud.portrait_surface = surf
        except Exception:
            pass



    def draw(self, screen):
        """Desenha a cena e o jogador na tela."""
        screen.fill((0, 0, 0))  # Limpa a tela com fundo preto

        # 1) FUNDO -> desenha apenas os layers 'back' (aqui entra o Level_1_2a)
        #    (garanta no __init__ que você registrou: StaticLayer("level_1_2a", plane="back"))
        self.layers.draw_back(screen)


        # 2) BOSS ou CADÁVER
        if not getattr(self, "boss_defeated", False) and not self.boss_dying:
            screen.blit(self.boss.image, self.boss.rect)
        else:
            # se estiver na sequência de morte, desenha o cadáver com alpha
            if self.boss_dying and self.boss_corpse and self.boss_corpse_rect:
                try:
                    self.boss_corpse.set_alpha(self.boss_corpse_alpha)
                except Exception:
                    pass
                screen.blit(self.boss_corpse, self.boss_corpse_rect)

        
        # 3) PLAYER
        screen.blit(self.player.image, self.player.rect)


        # 4) LAYERS FRONTAIS -> par intercalado (AA<->ab) e depois a estática 'b'
        #    (ambos devem ter plane="front" no __init__)
        self.layers.draw_front(screen)


        # 5) Disparos do player (se quer que fiquem ATRÁS das máscaras frontais,
        #    mova este bloco para ANTES de self.layers.draw_front(screen))
        for shot in self.player.shots:
            shot.draw(screen)


        # 6) HUD do Player
        screen.blit(self.hud.image, self.hud.rect)


        # 7) HUD do Boss (por último: SEMPRE desenhar)
        if hasattr(self.boss_hud, "draw"):
            self.boss_hud.draw(screen)
        else:
            screen.blit(self.boss_hud.image, self.boss_hud.rect)

        # 🔹 Mantém o nome do boss mesmo após a derrota
        screen.blit(self.boss_name_text, self.boss_name_pos)
     

        # 8) Overlay (se ativo)
        if self.overlay:
            self.overlay.draw(screen)

        pygame.display.update()