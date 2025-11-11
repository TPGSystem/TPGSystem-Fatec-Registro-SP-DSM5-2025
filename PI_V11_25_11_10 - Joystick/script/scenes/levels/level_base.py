import pygame, random
from ..base import Scene, PauseInventoryOverlay
from script.core.obj import Obj
from script.world.ground import Ground
from script.ui.hud import Hud
from script.ui.boss_hud import BossHud
from script.actors.player import Player
from script.actors.npcs.cacique import NPC_Cacique
from script.ui.chatbox import ChatBox
from script.combat.projectiles import Shot
from script.setting import *
from script.layer_anim import LayerStack, StaticLayer, FlipLayer
from ..gameover import GameOver
from script.data.dialogs.dialog_1_1 import Dialogo_1_1
from script.data.quizzes.questions_1_1 import Questoes_1_1




# Criando Tela de Nível
class Level(Scene):
    """Classe para a tela de nível."""
    
    def __init__(self, player_data=None, hud_data=None): 
        super().__init__()  # Chama o construtor da classe base
        
        self.font = pygame.font.Font(None, 36)  # Fonte usada pelo menu de pausa
        
        # Criação do chão
        self.ground = Ground(0, 400, 800, 20)  # x, y, largura, altura
        self.all_sprites.add(self.ground)  # Adiciona o chão ao grupo de sprites

        # Criação dos objetos na cena - Iremos trocar por layers
        #self.img_a = Obj("assets/levelSprite/level_1_1a.png", [0, 0], [self.all_sprites])  # Fundo da fase
        self.hudbk = Hud("assets/charsSprite/player/Hud/Hud_Char_Fundo.png", [25, 25], [self.all_sprites], (640, 360))
        #self.img_b = Obj("assets/levelSprite/level_1_1b.png", [0, 0], [self.all_sprites])  # Fundo da fase
        
        # ---------- CAMADAS DO CENÁRIO (LEVEL_1_1) ----------
        self.layers = LayerStack()
        base_path = "assets/levelSprite/"

        # ORDEM: do fundo para a frente (como você definiu)

        # 1) level_1_1a (fundo absoluto) → BACK
        self.layers.add("level_1_1a",
            StaticLayer(f"{base_path}level_1_1a.png", z=0, plane="back", pos=(0,0))
        )

        # 2) level_1_1aa <-> level_1_1ab (intercalando) → BACK
        self.layers.add("level_1_1aa_ab",
            FlipLayer(f"{base_path}level_1_1aa.png", f"{base_path}level_1_1ab.png",
                    fps=4.0, z=10, plane="back", pos=(0,0))
        )

        # 3) level_1_1b → BACK
        self.layers.add("level_1_1b",
            StaticLayer(f"{base_path}level_1_1b.png", z=20, plane="back", pos=(0,0))
        )

        # 4) level_1_1c → BACK
        self.layers.add("level_1_1c",
            StaticLayer(f"{base_path}level_1_1c.png", z=30, plane="back", pos=(0,0))
        )

        # 5) level_1_1ca <-> level_1_1cb (intercalando) → BACK
        self.layers.add("level_1_1ca_cb",
            FlipLayer(f"{base_path}level_1_1ca.png", f"{base_path}level_1_1cb.png",
                    fps=5.0, z=40, plane="back", pos=(0,0))
        )

        # ==== (Player e NPC são desenhados entre back e front) ====

        # 6) level_1_1d → FRONT (após player/NPC)
        self.layers.add("level_1_1d",
            StaticLayer(f"{base_path}level_1_1d.png", z=10, plane="front", pos=(0,0))
        )

        # 7) level_1_1da <-> level_1_1db (intercalando) → FRONT
        self.layers.add("level_1_1ea_eb",
            FlipLayer(f"{base_path}level_1_1ea.png", f"{base_path}level_1_1eb.png",
                    fps=4.0, z=20, plane="front", pos=(0,0))
        )

        # 8) level_1_1ea <-> level_1_1eb (intercalando) → FRONT
        self.layers.add("level_1_1fa_fb",
            FlipLayer(f"{base_path}level_1_1fa.png", f"{base_path}level_1_1fb.png",
                    fps=5.0, z=30, plane="front", pos=(0,0))
        )

        # 9) level_1_1f → FRONT (última de todas)
        self.layers.add("level_1_1g",
            StaticLayer(f"{base_path}level_1_1g.png", z=40, plane="front", pos=(0,0))
        )

        # relógio para delta time das animações
        self._layers_last_ticks = pygame.time.get_ticks()
        # ----------------------------------------------------------
        
        
        # HUD com dados anteriores (se houver)
        self.hud = Hud("assets/charsSprite/player/Hud/Hud_Char_Contorno.png", [25, 25], [self.all_sprites], (640, 360))
        if hud_data:
            self.hud.gold = hud_data.get("gold", 0)
            self.hud.life = hud_data.get("life", 25)
            self.hud.lives = hud_data.get("lives", 3)
            self.hud.xp = hud_data.get("xp", 0)

        # Player com dados anteriores (se houver)
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
            self.player = Player("assets/charsSprite/player/indigenaM/R0.png", [100, 250], [self.all_sprites], (200, 200)) # O Player agora se alinha ao chão

        # Define os buracos apenas nesta fase específica
        hole_rect = pygame.Rect(520, GROUND_LEVEL-10, 100, 400)  # (x, y, largura, altura)
        self.player.set_holes([hole_rect])  # Envia os buracos para o jogador

        # Sincroniza a HUD com o Player
        self.hud.update_lives(self.player.lives)
        
        self.npc = NPC_Cacique("assets/charsSprite/npcs/Cacique/CR1.png", [1000, 285], [self.all_sprites], (200, 200)) # O NPC agora se alinha ao chão
        
        # Fonte para o ChatBox
        font = pygame.font.Font(None, 30)  # Fonte padrão
        self.chatbox = ChatBox(font, (75, 250), (800, 400))  # ChatBox na parte inferior

        # Controle de fluxo Diálogos e questões
        self.dialogue = Dialogo_1_1.falas[:5]  # Primeiro conjunto de diálogos
        self.questions = Questoes_1_1.perguntas  # Todas as questões
        self.final_dialogue = Dialogo_1_1.falas[5:]  # Últimos diálogos
        self.current_question = 0  # Índice da questão atual
        self.dialogue_stage = 0  # 0: Diálogo inicial, 1: Questões, 2: Diálogo final
        self.dialogue_finished = False  # Controle para saber se o diálogo terminou
        self.confirming_answer = False  # Indica se está no processo de confirmação
        self.selected_option = None  # Guarda a opção selecionada para confirmar
        self.exit_enabled = False  # Sinaliza quando o player pode sair para o Level_1_2
        
        # quando liberar a saída, permite que o player atravesse a borda
        setattr(self.player, "exit_mode", True)
        
        #Gold e Conversão
        self.gold_reward = 0  # Quantidade de ouro por resposta correta (ajuste conforme necessário)
        self.points_to_gold_conversion = 2  # 1 ponto = 10 Gold (ajuste conforme necessário)
        
        self.questions = Questoes_1_1.perguntas[:]
        random.shuffle(self.questions)  # Embaralha as perguntas
           

    def handle_events(self, event):
        """Gerencia eventos de entrada do usuário na tela de nível."""
        # ✅ Ativa o menu de pausa com ESC
        super().handle_events(event)

        # ⚠️ Se o overlay estiver ativo, não processa eventos do jogo
        if self.overlay:
            return

        # 🎮 Eventos do jogador
        self.player.events(event)

        # 🎯 Interações do jogador
        if event.type == pygame.KEYDOWN:

            # --- Inicia diálogo com o NPC ---
            if event.key == pygame.K_e and self.player.rect.colliderect(self.npc.rect) and not self.chatbox.is_active():
                if self.dialogue_stage == 0:  # Diálogo inicial
                    formatted_dialogue = [
                        f"{speaker.rstrip(':').strip()}: {str(message).lstrip(':').lstrip()}"
                        for speaker, message in Dialogo_1_1.falas[:5]
                    ]
                    self.chatbox.display_messages(formatted_dialogue)
                    self.chatbox.active = True

                elif self.dialogue_stage == 2:  # Diálogo final
                    # Limpa qualquer dado residual das questões
                    self.chatbox.options = []
                    self.chatbox.title = ""
                    self.chatbox.question = ""

                    formatted_dialogue = [
                        f"{speaker.rstrip(':').strip()}: {str(message).lstrip(':').lstrip()}"
                        for speaker, message in self.final_dialogue
                    ]
                    self.chatbox.display_messages(formatted_dialogue)
                    self.chatbox.active = True
                    return super().handle_events(event)

            # --- ENTER: avança diálogo ou processa questão ---
            elif event.key == pygame.K_RETURN and self.chatbox.is_active():

                # Se estamos exibindo PERGUNTA (há opções na tela)
                if self.chatbox.options:
                    current_question = self.questions[self.current_question]

                    # 1º Enter: submete e mostra feedback visual (sem avançar)
                    if not self.chatbox.was_answer_submitted():
                        self.chatbox.submit_answer()

                        # 💰 Recompensa em ouro se acertou
                        if self.chatbox.was_answer_correct():
                            points = current_question.get("pontos", 0)
                            if points and points > 0:
                                gold_reward = points * self.points_to_gold_conversion
                                self.hud.update_gold(self.hud.gold + gold_reward)
                                print(f"✅ Resposta correta! Você ganhou {gold_reward} de gold!")
                            else:
                                print("✅ Resposta correta, mas a questão não tinha pontos definidos.")
                        else:
                            print("❌ Resposta errada.")

                    # 2º Enter: avança para próxima etapa
                    else:
                        self.current_question += 1
                        if self.current_question < len(self.questions):
                            question_data = self.questions[self.current_question]

                            # Embaralha as alternativas
                            shuffled_options = question_data["opcoes"][:]
                            random.shuffle(shuffled_options)

                            self.chatbox.display_question(
                            question_data["titulo"],
                            question_data["pergunta"],
                            shuffled_options,
                            correct_answer=question_data["resposta_correta"],
                            pontos=question_data.get("pontos", 1)
                        )
                            
                        else:
                            # Finaliza as perguntas e ativa o diálogo final
                            self.dialogue_stage = 2
                            self.chatbox.options = []
                            self.chatbox.title = ""
                            self.chatbox.question = ""

                            formatted_dialogue = [
                                f"{speaker.rstrip(':').strip()}: {str(message).lstrip(':').lstrip()}"
                                for speaker, message in self.final_dialogue
                            ]
                            self.chatbox.display_messages(formatted_dialogue)
                            self.chatbox.active = True

                # Caso NÃO seja pergunta (modo diálogo)
                else:
                    self.chatbox.next_message()

                    # Quando o diálogo inicial termina → inicia as questões
                    if self.chatbox.current_message >= len(self.chatbox.messages) and self.dialogue_stage == 0:
                        self.dialogue_stage = 1
                        question_data = self.questions[self.current_question]

                        shuffled_options = question_data["opcoes"][:]
                        random.shuffle(shuffled_options)

                        self.chatbox.display_question(
                            question_data["titulo"],
                            question_data["pergunta"],
                            shuffled_options,
                            correct_answer=question_data["resposta_correta"],
                            pontos=question_data.get("pontos", 1)
                        )
                        self.chatbox.active = True

                    # Quando o diálogo final termina → libera saída
                    elif self.chatbox.current_message >= len(self.chatbox.messages) and self.dialogue_stage == 2:
                        self.chatbox.active = False
                        self.exit_enabled = True

            # --- Navegação entre opções ---
            elif (event.key == pygame.K_UP or event.key == pygame.K_w) and self.chatbox.options:
                self.chatbox.previous_option()
            elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and self.chatbox.options:
                self.chatbox.next_option()

    
                
    def open_pause_menu(self):
        """Abre o menu de pausa com overlay de inventário."""
        # Garante que o overlay só é criado se ainda não existir
        if not self.overlay:
            self.overlay = PauseInventoryOverlay(
                parent_scene=self,
                font=FONT_BIG,
                small_font=FONT_SMALL,
                on_resume=self.on_resume,
                on_shop=self.on_shop,
                on_main_menu=self.on_main_menu
            )

    def on_resume(self):
        """Fecha o menu de pausa e retoma o jogo."""
        print("[DEBUG] Jogo retomado.")
        self.overlay = None

    def on_shop(self):
        """Ação da opção 'Escambo (Loja)'."""
        print("[DEBUG] A funcionalidade de escambo ainda será implementada.")
        # Aqui você pode trocar a cena futuramente:
        # self.change_scene(Shop())

    def on_main_menu(self):
        print("[DEBUG] Retornando ao menu principal e resetando progresso...")
        from script.game_state import STATE
        STATE.reset()
        from ..menus.title import Title
        self.change_scene(Title())           


    def update(self):
        
        # ---- delta-time para animações de layers ----
        now = pygame.time.get_ticks()
        if not hasattr(self, "_layers_last_ticks"):
            self._layers_last_ticks = now
        dt = (now - self._layers_last_ticks) / 1000.0
        self._layers_last_ticks = now

        self.layers.update(dt)
        # --------------------------------------------
        
        """Atualiza o estado da cena, incluindo o jogador e animações."""        
        self.player.check_death()  # <- Verifica e reduz a vida se necessário
        self.hud.update_life(self.player.life)  # Atualiza os pontos de vida
        self.hud.update_lives(self.player.lives)  # Atualiza o número de vidas
        self.hud.update_xp(self.player.xp)  # Atualiza o XP (caso necessário)
        self.player.update()  # Atualiza o jogador
        self.npc.update()  # Atualiza o NPC Cacique
        super().update()  # Atualiza os outros objetos da cena
        self.all_sprites.update()
        
        # Se o jogador concluiu o diálogo e saiu pela direita, muda de fase
        if self.exit_enabled and self.player.rect.x >= 1280:
            print("[DEBUG] Transição de fase - vidas atuais:", self.player.lives)
            from .level_1_2 import Level_1_2
            self.change_scene(Level_1_2(
                player_data={
                    "image_path": self.player.image_path,
                    "position": [0, 250],
                    "size": self.player.size,
                    "life": self.player.life,
                    "lives": self.player.lives,
                    "xp": self.player.xp
                },
                hud_data={
                    "gold": self.hud.gold,
                    "life": self.player.life,
                    "lives": self.player.lives,
                    "xp": self.player.xp
                }
        ))

        # Verifique se o jogador morreu e mude para a tela de Game Over
        if self.player.lives <= 0:
            self.change_scene(GameOver())  # Muda para a cena de Game Over

    def draw(self, screen):
        """Desenha a cena e o jogador na tela."""
        screen.fill((0, 0, 0))  # Limpa a tela com fundo preto
        
        # 1) BACK (fundo e camadas intercaladas antes do player/NPC)
        self.layers.draw_back(screen)

        # 2) SPRITES (tudo que já existe nos seus grupos)
        self.all_sprites.draw(screen)

        # 3) Player e NPC explícitos (mantém seu comportamento atual)
        screen.blit(self.npc.image, self.npc.rect)
        screen.blit(self.player.image, self.player.rect)

        # 4) FRONT (camadas que ficam na frente de todos)
        self.layers.draw_front(screen)

        # 5) Disparos do player (se quer que fiquem na frente do front, deixe aqui;
        #    se quiser que fiquem "no meio", mova o loop para antes do draw_front)
        for shot in self.player.shots:
            shot.draw(screen)

        # 6) HUD (por cima de tudo)
        screen.blit(self.hud.image, self.hud.rect)

        # 7) Chatbox e Overlay (se ativos)
        self.chatbox.draw(screen)
        if self.overlay:
            self.overlay.draw(screen)

        pygame.display.update()