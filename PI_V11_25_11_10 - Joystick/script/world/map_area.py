import pygame
from script.core.obj import Obj

class Map(Obj):
    """Classe para representar uma área do mapa."""
    
    def __init__(self, image_selected, area_completed, position, cursor_position):
        self.image_selected = self.load_image(image_selected)  # Carrega a imagem quando a área está selecionada
        self.area_completed = self.load_image(area_completed)  # Carrega a imagem quando a área está completada
        self.position = position  # Posição da área no mapa
        self.cursor_position = cursor_position  # Posição do cursor sobre a área
        self.visible = True  # Define visibilidade padrão como True

    def load_image(self, img_path):
        """Carrega uma imagem a partir do caminho fornecido."""
        try:
            image = pygame.image.load(img_path).convert_alpha()  # Carrega a imagem com suporte a transparência
            return image  # Retorna a imagem carregada
        except pygame.error as e:
            print(f"Erro ao carregar a imagem {img_path}: {e}")  # Exibe erro caso a imagem não carregue
            return None  # Retorna None se a imagem falhar ao carregar

    def draw(self, surface, selected):
        """Desenha a área do mapa na superfície especificada."""
        if self.visible:  # Verifica se a área está visível
            if selected:
                surface.blit(self.image_selected, self.position)  # Desenha a imagem selecionada
            else:
                surface.blit(self.area_completed, self.position)  # Desenha a imagem completada

    def set_visible(self, visible):
        """Define a visibilidade da área."""
        self.visible = visible