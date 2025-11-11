import pygame

class Text(pygame.sprite.Sprite):
    """Classe para criar e renderizar texto na tela."""
    
    def __init__(self, font_size, text, color, pos, groups):
        super().__init__(groups)  # Inicializa a classe pai com os grupos
        
        self.color = color  # Define a cor do texto
        
        # Renderizando um texto na Tela
        self.font = pygame.font.Font("assets/font/Primitive.ttf", font_size)  # Carrega a fonte com o tamanho especificado
        self.image = self.font.render(text, True, self.color)  # Renderiza o texto
        self.rect = self.image.get_rect(topleft=pos)  # Define o retângulo da imagem na posição especificada
        
    def update_text(self, text):
        """Atualiza o texto exibido."""
        self.image = self.font.render(text, True, self.color)  # Renderiza o novo texto