import pygame, os
from script.setting import *
from script.game_state import STATE  # 🔹 Importa o gerenciador de estado global

#Criação de Arquivo que vai receber imagens e posições,
# para poderem ser desenhados na tela

class Obj(pygame.sprite.Sprite):
    
    def __init__(self, img, pos, groups, size=None):
        super().__init__(groups)  # Inicializa a classe pai com os grupos
        self.image = pygame.image.load(img).convert_alpha()  # Carrega a imagem com suporte a transparência
        
        if size:
            self.image = pygame.transform.scale(self.image, size)  # Redimensiona a imagem se um tamanho for especificado
        self.rect = self.image.get_rect(topleft=pos)  # Define o retângulo da imagem na posição especificada
        self.visible = True  # Define a visibilidade padrão como True
    
    def update(self):
        """Atualiza a visibilidade do objeto."""
        if self.visible:
            self.image.set_alpha(255)  # Totalmente visível
        else:
            self.image.set_alpha(0)  # Invisível

    def draw(self, surface):
        """Desenha o objeto na superfície, se visível."""
        if self.visible:
            surface.blit(self.image, self.rect.topleft)  # Desenha a imagem na posição do retângulo

class Fade(Obj):
    """Classe para criar um efeito de desvanecimento."""
    
    def __init__(self, color):
        self.image = pygame.Surface((BASE_WIDTH, BASE_HEIGHT)).convert_alpha()  # Superfície para o efeito de fade
        self.image.fill(color)  # Preenche a superfície com a cor especificada
        self.image_alpha = 255  # Opacidade inicial
        self.speed_alpha = 5  # Velocidade de desvanecimento

    def draw(self, display):
        """Desenha a superfície de fade na tela."""
        display.blit(self.image, (0, 0))

    def update(self):
        """Atualiza a opacidade da superfície de fade."""
        if self.image_alpha > 1:
            self.image_alpha -= self.speed_alpha  # Reduz a opacidade

        self.image.set_alpha(self.image_alpha)  # Define a opacidade da superfície






                



            
