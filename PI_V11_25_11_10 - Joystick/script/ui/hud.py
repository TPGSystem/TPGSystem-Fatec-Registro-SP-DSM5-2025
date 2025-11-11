import pygame
from script.setting import BLACK_COLOR
from script.core.obj import Obj

class Hud(Obj):
    """Classe para representar o painel de Dados do Jogador: XP, Ouro, Vidas e Life."""

    def __init__(self, image_path, position, groups, size=(200, 200)):
        super().__init__(image_path, position, groups, size)
        self.size = size

        # Carregando imagens do HUD
        self.xp_bK = pygame.image.load("assets/charsSprite/player/Hud/Hud_Char_Fundo_XP.png").convert_alpha()
        self.xp_bar = pygame.image.load("assets/charsSprite/player/Hud/Hud_Char_Barra_XP.png").convert_alpha()
        self.hud_bk = pygame.image.load("assets/charsSprite/player/Hud/Hud_Char_Fundo.png").convert_alpha()
        self.hud_char_face = pygame.image.load("assets/charsSprite/player/Hud/Hud_Char_Face.png").convert_alpha()
        self.life_bar = pygame.image.load("assets/charsSprite/player/Hud/Hud_Life00PV.png").convert_alpha()
        self.contour_image = pygame.image.load("assets/charsSprite/player/Hud/Hud_Char_Contorno.png").convert_alpha()

        # Redimensionando imagens conforme o tamanho do HUD
        self.scaled_xp_background = pygame.transform.scale(self.xp_bK, size)
        self.scaled_xp_bar = pygame.transform.scale(self.xp_bar, size)
        self.scaled_background = pygame.transform.scale(self.hud_bk, size)
        self.scaled_hud_char_face = pygame.transform.scale(self.hud_char_face, size)
        self.scaled_life_bar = pygame.transform.scale(self.life_bar, size)
        self.scaled_contour = pygame.transform.scale(self.contour_image, size)

        # Carrega todas as imagens de pontos de vida (0 a 25)
        self.life_images = self.load_life_images()

        # Surface principal do HUD
        self.image = pygame.Surface(size, pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=position)

        # Inicialização de atributos
        self.life = 25        # Pontos de vida atuais
        self.max_life = 25    # Valor máximo de vida
        self.xp = 0
        self.max_xp = 100
        self.lives = 3        # Inicializa com 3 vidas (evita aparecer "None")
        self.gold = 0         # Inicializa com 0 de ouro

    def load_life_images(self):
        """Carrega as imagens dos pontos de vida de 0 a 25."""
        images = []
        for i in range(26):
            path = f"assets/charsSprite/player/Hud/Hud_Life{i:02d}PV.png"
            try:
                image = pygame.image.load(path).convert_alpha()
                scaled_image = pygame.transform.scale(image, self.size)
                images.append(scaled_image)
            except pygame.error as e:
                print(f"Erro ao carregar {path}: {e}")
                images.append(None)
        return images

    def update_life(self, life):
        """Atualiza os pontos de vida do jogador."""
        self.life = max(0, min(life, self.max_life))

    def update_lives(self, lives):
        """Atualiza o número de vidas restantes."""
        self.lives = max(0, lives)

    def update_xp(self, xp):
        """Atualiza a barra de experiência (XP)."""
        self.xp = max(0, min(xp, self.max_xp))

    def update_gold(self, gold):
        """Atualiza o valor de ouro exibido no HUD."""
        self.gold = max(0, min(gold, 9999))

    def compose_hud(self):
        """Compoe visualmente todas as camadas do HUD."""
        self.image.fill((0, 0, 0, 0))  # Limpa a tela com transparência

        # Fundo da barra de XP
        self.image.blit(self.scaled_xp_background, (0, 0))

        # Barra de XP proporcional
        xp_width = int((self.xp / self.max_xp) * self.size[0])
        xp_bar_rect = pygame.Rect(0, self.size[1] - 20, xp_width, 10)
        self.image.blit(self.scaled_xp_bar, xp_bar_rect, xp_bar_rect)

        # Desenha imagem da vida (se existir)
        if 0 <= self.life < len(self.life_images) and self.life_images[self.life]:
            self.image.blit(self.life_images[self.life], (0, 0))

        # Fundo principal do HUD
        self.image.blit(self.scaled_background, (0, 0))

        # Contorno do HUD
        self.image.blit(self.scaled_contour, (0, 0))

        # Rosto do personagem
        self.image.blit(self.scaled_hud_char_face, (0, 0))

        # Fonte padrão
        font = pygame.font.Font(None, 25)

        # Exibe o ouro (formato: 4 dígitos)
        gold_text = font.render(f"{self.gold:04d}", True, (BLACK_COLOR))
        self.image.blit(gold_text, (175, 40))  # Ajuste conforme seu layout

        # Exibe número de vidas, apenas se for inteiro
        if isinstance(self.lives, int):
            font = pygame.font.Font(None, 30)
            lives_text = font.render(str(self.lives), True, (BLACK_COLOR))
            self.image.blit(lives_text, (155, 60))

    def update(self):
        """Atualiza a interface do HUD a cada frame."""
        self.compose_hud()