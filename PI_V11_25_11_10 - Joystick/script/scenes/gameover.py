import pygame
from script.core.obj import Obj
from script.scenes.menus.title import Title
from .base import Scene

# Criando Tela de Game Over
class GameOver(Scene):
    """Classe para a tela de Game Over."""
    
    def __init__(self):
        super().__init__()  # Chama o construtor da classe base
        
        self.img = Obj("assets/gameOver.png", [0, 0], [self.all_sprites])  # Carrega a imagem de Game Over
        
    def handle_events(self, event):
        """Gerencia eventos de entrada do usuário na tela de Game Over."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                self.change_scene(Title())  # Muda para a tela inicial            
        return super().handle_events(event)
    
    def back_to_title(self):
        from .menus.title import Title   # ✅ import tardio
        self.change_scene(Title())
    
    def draw(self, surface):
        """Desenha a tela de Game Over."""
        self.img.draw(surface)