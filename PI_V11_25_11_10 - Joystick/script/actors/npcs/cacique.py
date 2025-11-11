import pygame
from script.core.obj import Obj

class NPC_Cacique(Obj):
    """Classe para representar o NPC estático 'Cacique' com animação idle sempre virado para a esquerda."""

    def __init__(self, image_path, position, groups, size=(200, 200)):
        super().__init__(image_path, position, groups, size)  # Adiciona o NPC ao grupo de sprites
        self.size = size
        self.original_image = pygame.image.load("assets/charsSprite/npcs/Cacique/CR0.png").convert_alpha()
        self.original_image = pygame.transform.flip(self.original_image, True, False)  # Inverte a imagem para a esquerda
        self.image = pygame.transform.scale(self.original_image, size)  # Redimensiona para 200x200
        self.rect = self.image.get_rect(topleft=position)  # Define a posição inicial do NPC
    
        # Inicializa o dicionário de animações
        self.animations = {
            "idle": []  # Inicializando a chave 'idle' com uma lista vazia
        }

        # Carregar imagens da animação idle
        for i in range(2):  # Assumindo que você tem 2 imagens para a animação idle
            img = pygame.image.load(f"assets/charsSprite/npcs/Cacique/CR{i}.png").convert_alpha()
            img = pygame.transform.flip(img, True, False)  # Inverte as imagens para a esquerda
            img = pygame.transform.scale(img, size)  # Redimensiona
            self.animations["idle"].append(img)  # Adiciona à lista de animação

        self.state = "idle"  # Estado inicial
        self.current_frame = 0  # Índice do quadro atual na lista de imagem
        self.image = self.animations[self.state][self.current_frame]  # Primeira imagem da animação
        self.rect = self.image.get_rect(topleft=position)  # Atualiza a posição do NPC
        
        # Inicializando o contador de ticks para animação
        self.ticks = 0  # Certifique-se de inicializar os ticks aqui!
        self.img = 0  # Índice da imagem atual para animação

    def update(self):
        """Atualiza o estado do NPC em cada quadro."""
        self.animate("idle", 100, 1)  # Atualiza a animação de respiração (idle)

    def animate(self, name, ticks, limit):
        """Anima o NPC com uma sequência de imagens."""
        self.ticks += 1  # Incrementa o contador de ticks

        # Controla a troca de frames com base no número de ticks
        if self.ticks >= ticks:
            self.ticks = 0  # Reseta o contador de ticks
            self.current_frame += 1  # Avança para o próximo quadro da animação

        # Verifica se a animação chegou ao fim e reseta o contador
        num_frames = len(self.animations[name])
        if self.current_frame >= num_frames:  # Porque temos apenas 2 imagens (0 e 1)
            self.current_frame = 0  # Reseta para a primeira imagem da animação

        # Atualiza a imagem do NPC com a nova animação
        self.image = pygame.transform.scale(self.animations[name][self.current_frame], self.size)

    def interact(self, player):
        """Interage com o jogador quando um evento específico ocorre."""
        # Exemplo de interação: quando o jogador está perto do Cacique
        if self.rect.colliderect(player.rect):  # Verifica se o jogador está próximo
            print("Cacique: Bem-vindo, jovem guerreiro. O que procura?")
            # Aqui, você pode disparar um evento específico ou diálogo
            # Exemplo: abrir um menu ou dar uma missão