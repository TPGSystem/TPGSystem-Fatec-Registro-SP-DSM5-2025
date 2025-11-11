import pygame, os
from script.core.obj import Obj

class Char(Obj):
    """Classe para representar um personagem no jogo."""
    
    def __init__(self, image_selected, image_unselected, pose, position, pose_position, size_selected, size_unselected, pose_size, status_image, status_position):
        self.image_selected = self.load_image(image_selected, size_selected)  # Carrega a imagem selecionada
        self.image_unselected = self.load_image(image_unselected, size_unselected)  # Carrega a imagem não selecionada
        self.pose = self.load_image(pose, pose_size)  # Carrega a pose do personagem
        self.position = position  # Posição do personagem
        self.pose_position = pose_position  # Posição da pose do personagem
        self.status_image = self.load_image(status_image, None)  # Carrega a imagem da placa de status
        self.status_position = status_position  # Posição da placa de status
        self.visible = True  # Define visibilidade padrão como True

    def load_image(self, img_path, size):
        """Carrega uma imagem a partir do caminho fornecido."""
        try:
            image = pygame.image.load(img_path).convert_alpha()  # Carrega a imagem com suporte a transparência
            return pygame.transform.scale(image, size) if size else image  # Redimensiona se o tamanho for especificado
        except pygame.error as e:
            print(f"Erro ao carregar a imagem {img_path}: {e}")  # Exibe erro caso a imagem não carregue
            return None  # Retorna None se a imagem falhar ao carregar

    def draw(self, surface, selected):
        """Desenha o personagem na superfície especificada."""
        if self.visible:  # Verifica se o personagem está visível
            if selected:
                surface.blit(self.image_selected, self.position)  # Desenha a imagem selecionada
                surface.blit(self.pose, self.pose_position)  # Desenha a pose do personagem
                surface.blit(self.status_image, self.status_position)  # Desenha a placa de status
            else:
                surface.blit(self.image_unselected, self.position)  # Desenha a imagem não selecionada

    def set_visible(self, visible):
        """Define a visibilidade do personagem."""
        self.visible = visible