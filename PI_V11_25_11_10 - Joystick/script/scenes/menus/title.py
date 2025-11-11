import pygame
import sys

from ..base import Scene # Importa a classe base de cena

# Imports de objetos e recursos essenciais
from script.core.obj import Obj
from script.setting import *


# Criando Tela Inicial do Jogo
class Title(Scene):
    """Classe para a tela inicial do jogo."""
    
    def __init__(self):
        super().__init__()  # Chama o construtor da classe base
        
        # Criação de objetos de fundo e outros elementos da tela
        self.bg = Obj("assets/menu/Fundo.png", [0, 0], [self.all_sprites], size=(1400, 850))
        self.bg_mold = Obj("assets/menu/Moldura_V2.png", [0, 0], [self.all_sprites])
        self.title = Obj("assets/menu/Titulo.png", [535, 50], [self.all_sprites], size=(700, 285))
        self.char1 = Obj("assets/menu/Indigena.png", [185, -10], [self.all_sprites], size=(450, 770))
        self.char2 = Obj("assets/menu/Bandeirantes.png", [12, 155], [self.all_sprites], size=(320, 575))
        self.char3 = Obj("assets/menu/Africano.png", [-240, 280], [self.all_sprites], size=(825, 650))
        self.star_text = Obj("assets/menu/Jogar.png", [822, 385], [self.all_sprites], size=(225, 80))
        self.options_text = Obj("assets/menu/Opcoes.png", [822, 485], [self.all_sprites], size=(275, 80))
        self.exit_text = Obj("assets/menu/Sair.png", [822, 585], [self.all_sprites], size=(175, 75))
        self.indicator = Obj("assets/menu/Cursor.png", [695, 385], [self.all_sprites], size=(110, 70))  # Cursor
        self.indicator_dir = 1  # Direção do movimento do cursor
        self.indicator_choose = 0  # Opção atualmente selecionada
        
        # Variáveis de movimento do BG
        self.bg_pos = [0, 0]  # Posição inicial do fundo
        self.bg_target = (-120, 0)  # Primeira posição alvo
        self.bg_vel = 1  # Velocidade de movimento do fundo

        # Pré-carregar a Música na memória e a opção de Tela Salva
        self.start_music()  # Inicia a música
        self.start_screen()  # Configura a tela inicial
        
    def start_screen(self):    
        """Configura a tela inicial com base nas opções salvas."""
        if self.option_data["display_text_values"] == "Fullscreen" and self.option_data["start"] == "on":
            pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # Muda para tela cheia
            self.option_data["start"] = "off"  # Atualiza o estado
            self.save_file("teste.json", self.option_data)  # Salva as opções

    def handle_events(self, event):
        """Gerencia eventos de entrada do usuário na tela inicial."""
        # Verifica se o evento recebido é uma tecla pressionada
        if event.type == pygame.KEYDOWN:
            # Enter (principal) ou Enter do keypad
            if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                self.indicator_set_option(event)
            # setas / WASD
            if event.key in (pygame.K_DOWN, pygame.K_s, pygame.K_UP, pygame.K_w):
                self.indicator_position(event)
        return super().handle_events(event)  # deixa o ESC subir para Scene

    def go_to_control(self):
        from script.scenes.menus.control import Control      # ✅ import tardio
        self.change_scene(Control())

    def go_to_options(self):
        from script.scenes.menus.option import Option        # ✅ import tardio
        self.change_scene(Option())

    def indicator_set_option(self, event):
        """Define a opção selecionada com base na tecla pressionada."""
        if (event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER) and self.indicator_choose == 0:
            from .control import Control
            self.change_scene(Control())  # Muda para a cena de seleção de personagem
        if (event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER) and self.indicator_choose == 1:
            from .option import Option          # ✅ import tardio
            self.change_scene(Option())  # Muda para a cena de opções
        elif (event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER) and self.indicator_choose == 2:
            self.option_data["start"] = "on"  # Atualiza o estado
            self.save_file("teste.json", self.option_data)  # Salva os dados
            pygame.quit()  # Encerra o Pygame
            sys.exit()  # Sai do programa

    def indicator_position(self, event):
        """Atualiza a posição do indicador com base nas teclas pressionadas."""
        if event.key == pygame.K_DOWN or event.key == pygame.K_s:
            self.sound_click.play()  # Toca o som de clique
            if self.indicator_choose <= 1:
                self.indicator_choose += 1  # Move para a próxima opção
                if self.indicator_choose == 0:
                    self.indicator.rect.y = 384  # Atualiza a posição do cursor
                elif self.indicator_choose == 1:
                    self.indicator.rect.y = 484
                elif self.indicator_choose == 2:
                    self.indicator.rect.y = 584
                        
        elif event.key == pygame.K_UP or event.key == pygame.K_w:
            self.sound_click.play()  # Toca o som de clique
            if self.indicator_choose > 0:
                self.indicator_choose -= 1  # Move para a opção anterior
                if self.indicator_choose == 0:
                    self.indicator.rect.y = 384
                elif self.indicator_choose == 1:
                    self.indicator.rect.y = 484
                elif self.indicator_choose == 2:
                    self.indicator.rect.y = 584
    
     
    # Função auxiliar para mover o fundo até o alvo lentamente
    def move_towards_target(self, current, target, vel):
        """Move a posição atual em direção à posição alvo com a velocidade especificada."""
        if current < target:
            return min(current + vel, target)  # Move para frente até alcançar o alvo
        elif current > target:
            return max(current - vel, target)  # Move para trás até alcançar o alvo
        return current  # Retorna a posição atual se já estiver no alvo
            
    # Animando Cursor                            
    def update(self):
        """Atualiza a animação do cursor e o fundo."""
        self.indicator_animation()  # Atualiza a animação do cursor
    
        # Atualiza a animação do fundo
        return self.bg_animation()
    
    def bg_animation(self):
        """Movimenta o fundo de acordo com a lógica definida."""
        x, y = self.bg_pos  # Posições atuais do fundo
        
        # Movimentação do fundo entre as posições definidas
        if self.bg_target == (-120, 0):  # Movimento para a esquerda até x = -120
            x = self.move_towards_target(x, -120, self.bg_vel)
            if x == -120:
                self.bg_target = (-120, -130)  # Agora move para cima até y = -130
        
        elif self.bg_target == (-120, -130):  # Movimento para cima até y = -130
            y = self.move_towards_target(y, -130, self.bg_vel)
            if y == -130:
                self.bg_target = (0, -130)  # Agora move para a direita até x = 0
        
        elif self.bg_target == (0, -130):  # Movimento para a direita até x = 0
            x = self.move_towards_target(x, 0, self.bg_vel)
            if x == 0:
                self.bg_target = (0, 0)  # Agora move para baixo até y = 0
        
        elif self.bg_target == (0, 0):  # Movimento para baixo até y = 0
            y = self.move_towards_target(y, 0, self.bg_vel)
            if y == 0:
                self.bg_target = (-120, 0)  # Volta a mover para a esquerda, reiniciando o ciclo

        self.bg_pos = [x, y]  # Atualiza a posição do fundo
        self.bg.rect.topleft = self.bg_pos  # Define a nova posição do fundo
                
        return super().update()  # Chama o método update da classe pai
    
    # ✅ use import tardio no método que volta ao título
    def back_to_title(self):
        from .title import Title
        self.change_scene(Title())

    def indicator_animation(self):
        """Anima o movimento do cursor."""
        self.indicator.rect.x += self.indicator_dir  # Move o cursor
        if self.indicator.rect.x > 705:  # Verifica os limites da animação
            self.indicator_dir *= -1  # Inverte a direção
        elif self.indicator.rect.x < 685:  # Verifica os limites da animação
            self.indicator_dir *= -1  # Inverte a direção