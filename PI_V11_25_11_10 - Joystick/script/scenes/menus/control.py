import pygame
from ..base import Scene
from script.core.obj import Obj
from ..char_select.char_select import Char_Select


# Criando Tela de Controles
class Control(Scene):
    """Classe para a tela de Controle."""
    
    def __init__(self):
        super().__init__()  # Chama o construtor da classe base
        
        self.img = Obj("assets/Control.png", [0, 0], [self.all_sprites])  # Carrega a imagem de Game Over
        
    def handle_events(self, event):
        """Gerencia eventos de entrada do usuário na tela de Game Over."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                self.change_scene(Char_Select())  # Muda para a tela inicial            
        return super().handle_events(event)
    
    def draw(self, surface):
        """Desenha a tela de Game Over."""
        self.img.draw(surface)