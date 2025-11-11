
# ============================================================
#  CHATBOX — Sistema de Diálogo e Perguntas
#  ----------------------------------------
#  Exibe mensagens ou perguntas interativas na tela,
#  com opções de resposta e navegação via teclado.
#  Pode ser usada tanto para diálogos narrativos quanto
#  para quizzes com pontuação.
# ============================================================

import pygame, os
from script.setting import *


class ChatBox:
    """Classe para exibir mensagens de diálogo e questões interativas na tela."""

    def __init__(self, font=None, position=(0, 0), size=(600, 200)):
        """
        Inicializa a caixa de diálogo na tela.

        Parâmetros:
          font      → fonte principal usada nos textos.
          position  → posição (x, y) da caixa no display.
          size      → tamanho da caixa (largura, altura).
        """
        # Usa a fonte padrão do projeto (Primitive.ttf) se nenhuma for passada
        self.font = pygame.font.Font(None, 32)
        # Fonte menor para opções de múltipla escolha
        self.small_font = pygame.font.Font(None, 24)

        # Define posição e tamanho da caixa
        self.position = position
        self.size = size
        self.rect = pygame.Rect(position, size)

        # Cores padrão (vêm do setting.py)
        self.color = BLACK_COLOR       # Cor de fundo da caixa
        self.text_color = WHITE_COLOR  # Cor dos textos

        # Armazena mensagens e estados de diálogo
        self.messages = []          # Lista de falas simples (modo diálogo)
        self.current_message = 0    # Índice da fala atual
        self.active = False         # Define se a caixa está sendo exibida

        # Controle de opções de resposta (modo pergunta)
        self.option_index = 0       # Índice da opção atualmente selecionada
        self.score = 0              # Pontuação acumulada
        self.title = ""             # Título da pergunta
        self.question = ""          # Texto da pergunta
        self.options = []           # Lista de opções de resposta
        self.correct_answers = []   # Lista de respostas corretas (1 ou mais)
        self.current_points = 1     # Pontos atribuídos por questão correta
        
        # --- Estado para quizzes (2 cliques de Enter) ---
        self.answer_submitted = False      # vira True após o 1º Enter
        self.selection_correct = None      # True/False depois de avaliar
        self.selected_option_text = None   # texto da opção escolhida
        self.correct_answers = []          # guarda a correta (primeira posição)
        self.current_points = 0            # pontos da questão atual (se usar)


    # ============================================================
    #  MÉTODOS DE CONTROLE DE MENSAGENS E QUESTÕES
    # ============================================================

    def display_messages(self, messages):
        """
        Exibe um conjunto de mensagens simples (modo diálogo).

        Parâmetro:
          messages → lista de strings com as falas ou textos.
        """
        self.messages = [str(m) for m in messages]
        self.current_message = 0
        self.active = True
        # Limpa dados de questão caso haja
        self.options = []
        self.correct_answers = []
        self.current_points = 1
        
         # Reset de estado visual/avaliação
        self.answer_submitted = False
        self.selection_correct = None
        self.selected_option_text = None

    def display_question(self, title, question, options, correct_answer=None, pontos=1):
        """
        Exibe uma pergunta com título e opções de resposta.

        Parâmetros:
          title          → título da pergunta.
          question       → enunciado da questão (string).
          options        → lista com alternativas possíveis.
          correct_answer → string com a resposta correta.
          pontos         → valor da questão (padrão: 1).
        """
        self.title = title
        self.question = question
        self.options = options[:] if options else []
        self.option_index = 0

        # guarda a correta na posição 0 (como lista)
        self.correct_answers = [correct_answer] if correct_answer is not None else []

        # pontos (se o teu HUD usar isso)
        self.current_points = pontos or 0

        # reset do estado visual/avaliação
        self.answer_submitted = False
        self.selection_correct = None
        self.selected_option_text = None

        # ativa a caixa de diálogo/pergunta
        self.active = True

    def next_message(self):
        """Avança para a próxima fala no modo de diálogo."""
        if self.options:  # se for uma questão, não muda a fala
            return
        self.current_message += 1
        if self.current_message >= len(self.messages):
            self.active = False  # encerra quando acabar

    def validate_answer(self):
        """
        Verifica se a opção selecionada é a resposta correta.
        Se acertar, soma a pontuação configurada em `current_points`.
        """
        if self.options and self.correct_answers:
            selected = self.options[self.option_index]
            if selected == self.correct_answers[0]:
                self.score += self.current_points
                print("✅ Resposta correta!")
            else:
                print("❌ Resposta errada.")
            self.active = False  # fecha a caixa após responder
            
    def submit_answer(self):
        """Marca a resposta selecionada, avalia (certa/errada) e mantém a caixa aberta
        para a confirmação (2º Enter)."""
        if not self.options or self.answer_submitted:
            return

        self.selected_option_text = self.options[self.option_index]
        correct = False
        if self.correct_answers:
            correct = (self.selected_option_text == self.correct_answers[0])

        self.selection_correct = bool(correct)
        if correct:
            self.score += self.current_points

        self.answer_submitted = True  # ativa o modo 'feedback visual'        

    def previous_option(self):
        """Seleciona a opção anterior no menu de respostas."""
        if self.options:
            self.option_index = (self.option_index - 1) % len(self.options)

    def next_option(self):
        """Seleciona a próxima opção no menu de respostas."""
        if self.options:
            self.option_index = (self.option_index + 1) % len(self.options)

    def select_option(self):
        """Retorna o texto da opção atualmente selecionada."""
        return self.options[self.option_index] if self.options else None

    def is_active(self):
        """Retorna True se a chatbox estiver ativa na tela."""
        return self.active

    # ============================================================
    #  RENDERIZAÇÃO VISUAL
    # ============================================================

    def draw(self, screen):
        """
        Desenha a caixa e todo o conteúdo (título, pergunta, opções, falas)
        na superfície informada (geralmente o display principal).
        """
        
        # Se a caixa não estiver ativa, não desenha nada
        if not self.active:
            return

        # --- Fundo da caixa (retângulo com borda) ---
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, WHITE_COLOR, self.rect, 2)

        # Margens e posicionamento vertical
        margin = 20
        available_width = self.rect.width - 2 * margin
        available_height = self.rect.height - 2 * margin
        y = self.rect.y + margin

        # --- 1) Título (cor padrão; se quiser azul, troque para LIGHT_SKY_BLUE) ---
        if self.title:
            surf = self.font.render(self.title, True, self.text_color)
            screen.blit(surf, (self.rect.x + margin, y))
            y += 40
            available_height -= 40

        # --- 2) Pergunta (Primitive + AZUL) ---
        if self.question:
            for line in self.wrap_text(str(self.question), available_width):
                if available_height < 20:
                    break
                surf = self.font.render(line, True, LIGHT_SKY_BLUE)  # 🔵 pergunta azul
                screen.blit(surf, (self.rect.x + margin, y))
                y += 24
                available_height -= 24

        # --- 3) Opções de resposta ---
        if self.options:
            y += 20
            available_height -= 20
            available_width = self.rect.width - 2 * margin

            if not self.answer_submitted:
                # Modo normal (antes de enviar): selecionada amarelo, demais branco
                for i, opt in enumerate(self.options):
                    color = (255, 255, 0) if i == self.option_index else WHITE_COLOR
                    wrapped = self.wrap_text(str(opt), available_width, self.small_font)

                    # desenha cada linha da alternativa
                    for line in wrapped:
                        if available_height < 20:
                            break
                        surf = self.small_font.render(line, True, color)
                        screen.blit(surf, (self.rect.x + margin, y))
                        y += 20        # ← altura da linha aumentada
                        available_height -= 20

                    # espaço extra entre alternativas (um "respiro" visual)
                    if i < len(self.options) - 1:
                        y += 10        # ← separação entre alternativas
                        available_height -= 10

            else:
                # Feedback após submissão (verde/vermelho)
                GREEN = (50, 220, 120)
                RED   = (220, 50, 50)
                to_render = []
                correct_text = self.correct_answers[0] if self.correct_answers else None
                chosen_text  = self.selected_option_text

                if self.selection_correct:
                    to_render = [(chosen_text, GREEN)]
                else:
                    if correct_text:
                        to_render.append((correct_text, GREEN))
                    if chosen_text and chosen_text != correct_text:
                        to_render.append((chosen_text, RED))

                for text_val, color in to_render:
                    wrapped = self.wrap_text(str(text_val), available_width, self.small_font)
                    for line in wrapped:
                        if available_height < 20:
                            break
                        surf = self.small_font.render(line, True, color)
                        screen.blit(surf, (self.rect.x + margin, y))
                        y += 25
                        available_height -= 25
                    # espaço extra entre as alternativas mostradas no feedback
                    y += 15
                    available_height -= 15


        # --- 4) Modo diálogo simples (sem opções): cores por personagem ---
        elif self.messages and self.current_message < len(self.messages):
            current_text = self.messages[self.current_message]

            # Detecta o falante de forma robusta (aceita " Player : ...", "Jogador: ...", etc.)
            speaker = current_text.split(":", 1)[0].strip().lower()

            # 🟢 Define cores diferentes conforme o personagem
            if current_text.startswith("Cacique") or current_text.startswith("Cacique"):
                color = LIGHT_SKY_BLUE  # Azul
            elif current_text.startswith("Player") or current_text.startswith("Jogador") or current_text.startswith("Jovem Guerreiro"):
                color = WATER_GREEN     # Verde
            else:
                color = self.text_color  # Cor padrão

            # Render das falas (Primitive por padrão)
            for line in self.wrap_text(current_text, available_width):
                if available_height < 30:
                    break
                surf = self.font.render(line, True, color)
                screen.blit(surf, (self.rect.x + margin, y))
                y += 30
                available_height -= 30
                
    def submit_answer(self):
        """Marca a opção selecionada, avalia e mantém a caixa aberta para confirmação (2º Enter)."""
        if not self.options or self.answer_submitted:
            return

        self.selected_option_text = self.options[self.option_index]
        correct = False
        if self.correct_answers:
            correct = (self.selected_option_text == self.correct_answers[0])

        self.selection_correct = bool(correct)
        # se você já controla score aqui, incremente usando self.current_points
        # ex.: if correct: self.score += self.current_points
        self.answer_submitted = True

    def was_answer_submitted(self):
        return bool(self.answer_submitted)

    def was_answer_correct(self):
        return bool(self.selection_correct)            


    # ============================================================
    #  UTILITÁRIOS DE TEXTO
    # ============================================================

    def wrap_text(self, text, max_width, font=None):
        """
        Divide o texto em múltiplas linhas para caber dentro da largura da caixa.

        Parâmetros:
          text      → string a ser quebrada.
          max_width → largura máxima em pixels.
          font      → fonte usada para medir o tamanho (opcional).
        """
        if text is None:
            return []

        font = font or self.font
        words = str(text).split()
        lines, line = [], []

        for w in words:
            # Testa o tamanho da linha atual + próxima palavra
            test = " ".join(line + [w])
            # Usa font.size() para medir largura em pixels
            if font.size(test)[0] > max_width:
                if line:
                    lines.append(" ".join(line))
                line = [w]
            else:
                line.append(w)

        # Adiciona a última linha restante
        if line:
            lines.append(" ".join(line))

        return lines
