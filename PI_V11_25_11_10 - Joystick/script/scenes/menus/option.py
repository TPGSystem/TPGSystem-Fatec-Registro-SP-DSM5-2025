import pygame
from ..base import Scene
from script.core.obj import Obj
from script.core.text import Text
from script.setting import *
from .title import Title


# Criando Tela de Opções
class Option(Scene):
    """Classe para a tela de opções."""
    
    def __init__(self):
        super().__init__()  # Chama o construtor da classe base
            
        # Criação de objetos de fundo e outros elementos da tela
        self.bg = Obj("assets/menu/Fundo2.png", [0, 0], [self.all_sprites], size=(1280, 720))
        self.bg_mold = Obj("assets/menu/Moldura_V2.png", [0, 0], [self.all_sprites])
        self.title = Obj("assets/menu/Titulo.png", [50, 50], [self.all_sprites], size=(500, 210))
        self.text_options = Obj("assets/menu/Opcoes.png", [850, 65], [self.all_sprites], size=(350, 100))
 
        # Criação de textos para opções de som e tela
        self.sound_text = Text(100, "Som:", VENETIAN_RED_COLOR, [360, 320], [self.all_sprites])
        self.sound_option_text = Text(60, self.option_data["sound_text_values"], YELLOW_COLOR, [670, 360], [self.all_sprites])
        self.sound_text_values = ["Desligado", "Minimo", "Maximo"]  # Opções de som
        self.sound_text_choose = self.option_data["sound_text_choose"]  # Opção de som selecionada
                
        self.display_text = Text(100, "Tela:", VENETIAN_RED_COLOR, [360, 450], [self.all_sprites])
        self.display_option_text = Text(60, self.option_data["display_text_values"], YELLOW_COLOR, [670, 490], [self.all_sprites])
        self.display_text_values = ["Window", "Fullscreen"]  # Opções de tela
        self.display_text_choose = self.option_data["display_text_choose"]  # Opção de tela selecionada
        
        self.apply_text = Text(60, "Aplicar:", TANGO_MANGA_COLOR, [508, 580], [self.all_sprites])
        
        # Inicialização do cursor
        self.indicator = Obj("assets/menu/Cursor.png", [217, 350], [self.all_sprites], size=(110, 70))  # Imagem do cursor
        self.indicator_dir = 1  # Direção do movimento do cursor
        self.indicator_choose = 0  # Opção atualmente selecionada
        
    def indicator_set_option(self, event):
        """Define a opção selecionada com base na tecla pressionada."""
        # Alternar opções de som
        if (event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER) and self.indicator_choose == 0:
            if self.sound_text_choose < 2:
                self.sound_text_choose += 1  # Move para a próxima opção
            else:
                self.sound_text_choose = 0  # Retorna para a primeira opção
                
            self.option_data["sound_text_choose"] = self.sound_text_choose
            self.option_data["sound_text_values"] = self.sound_text_values[self.sound_text_choose]
                        
            # Atualiza o texto da opção de som
            self.sound_option_text.update_text(self.sound_text_values[self.sound_text_choose])
            
            # Ajusta a música de acordo com a seleção
            if self.sound_text_choose == 0:
                pygame.mixer.music.stop()  # Para a música
                self.option_data["music_set_volume"] = 0
            elif self.sound_text_choose == 1:
                self.option_data["music_set_volume"] = 0.05
                pygame.mixer.music.play(-1)  # Toca a música em loop
                pygame.mixer.music.set_volume(self.option_data["music_set_volume"])  # Ajusta o volume
            elif self.sound_text_choose == 2:
                self.option_data["music_set_volume"] = 0.1
                pygame.mixer.music.set_volume(0.1)  # Ajusta o volume

        # Alternar opções de tela
        elif (event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER) and self.indicator_choose == 1:
            if self.display_text_choose < 1:
                self.display_text_choose += 1  # Move para a próxima opção
            else:
                self.display_text_choose = 0  # Retorna para a primeira opção
                
            self.display_option_text.update_text(self.display_text_values[self.display_text_choose])  # Atualiza o texto da opção de tela
            
            self.option_data["display_text_choose"] = self.display_text_choose
            self.option_data["display_text_values"] = self.display_text_values[self.display_text_choose]
                       
            # Aplica as mudanças na tela
            if self.display_text_choose == 0:
                pygame.display.set_mode((BASE_WIDTH, BASE_HEIGHT), pygame.RESIZABLE)  # Modo janela
            elif self.display_text_choose == 1:
                pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # Modo tela cheia
                
        elif (event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER) and self.indicator_choose == 2:
            self.save_file("teste.json", self.option_data)  # Salva as opções
            self.change_scene(Title())  # Retorna para a tela inicial
    
    def indicator_position(self, event):
        """Atualiza a posição do indicador com base nas teclas pressionadas."""
        if event.key == pygame.K_DOWN or event.key == pygame.K_s:
            self.sound_click.play()  # Toca o som de clique
            if self.indicator_choose <= 1:
                self.indicator_choose += 1  # Move para a próxima opção
                if self.indicator_choose == 0:
                    self.indicator.rect.x = 217
                    self.indicator.rect.y = 350
                elif self.indicator_choose == 1:
                    self.indicator.rect.x = 217
                    self.indicator.rect.y = 480
                elif self.indicator_choose == 2:
                    self.indicator.rect.x = 365
                    self.indicator.rect.y = 570
                        
        elif event.key == pygame.K_UP or event.key == pygame.K_w:
            self.sound_click.play()  # Toca o som de clique
            if self.indicator_choose > 0:
                self.indicator_choose -= 1  # Move para a opção anterior
                if self.indicator_choose == 0:
                    self.indicator.rect.x = 217
                    self.indicator.rect.y = 350
                elif self.indicator_choose == 1:
                    self.indicator.rect.x = 217
                    self.indicator.rect.y = 480
                elif self.indicator_choose == 2:
                    self.indicator.rect.x = 365
                    self.indicator.rect.y = 570
                    
    def handle_events(self, event):
        """Gerencia eventos de entrada do usuário na tela de opções."""
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_DOWN, pygame.K_s, pygame.K_UP, pygame.K_w):
                self.indicator_position(event)
            if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                self.indicator_set_option(event)
        return super().handle_events(event)
    
    def indicator_animation(self):
        """Anima o movimento do cursor."""
        self.indicator.rect.x += self.indicator_dir  # Move o cursor
        if 207 <= self.indicator.rect.x <= 227:  # Verifica os limites da animação
            if self.indicator.rect.x >= 227 or self.indicator.rect.x <= 207:
                self.indicator_dir *= -1  # Inverte a direção
        elif 355 <= self.indicator.rect.x <= 375:  # Verifica os limites da animação
            if self.indicator.rect.x >= 375 or self.indicator.rect.x <= 355:
                self.indicator_dir *= -1  # Inverte a direção
            
    def update(self):
        """Atualiza a animação do cursor e a tela."""
        self.indicator_animation()  # Atualiza a animação do cursor
        return super().update()  # Chama o método update da classe pai