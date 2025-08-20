import pygame, os
from script.setting import *

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
  
        
class Ground(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((0, 255, 0))  # Cor verde para o chão
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, surface):
        surface.blit(self.image, self.rect)  # Desenha a imagem do chão na tela


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
        
class BossHud(pygame.sprite.Sprite):
    def __init__(self, image_path, position=(0, 0), size=(200, 50)):
        super().__init__()
        self.original_image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.original_image, size)
        self.rect = self.image.get_rect(topleft=position)


class Shot(pygame.sprite.Sprite):
    """Classe para representar o projétil disparado pelo jogador."""

    def __init__(self, x, y, direction, groups, size=(80, 25)):
        super().__init__(groups)  # Adiciona o projétil ao(s) grupo(s) de sprites
        
        self.direction = direction  # Direção do disparo: 1 (direita), -1 (esquerda)
        self.speed = 5  # Velocidade com que o projétil se move

        # Carrega a imagem do projétil com transparência (alpha)
        image = pygame.image.load("assets/projectiles/Shot1.png").convert_alpha()

        # Redimensiona a imagem para o tamanho desejado
        image = pygame.transform.scale(image, size)

        # Espelha a imagem horizontalmente se o disparo for para a esquerda
        if direction == -1:
            image = pygame.transform.flip(image, True, False)

        # Define a imagem e a posição do projétil na tela
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self):
        """Atualiza a posição do projétil a cada frame."""
        
        # Move o projétil na direção desejada (multiplicando pela velocidade)
        self.rect.x += self.direction * self.speed

        # Remove o projétil se ele sair completamente da tela
        if self.rect.right < 0 or self.rect.left > BASE_WIDTH:
            self.kill()  # Remove da tela e do grupo de sprites

    def draw(self, surface):
        """Desenha o projétil na superfície (tela) fornecida.""" 
        surface.blit(self.image, self.rect.topleft)



class Player(Obj):
    """Classe para representar o jogador no jogo Guardiões de Pindorama."""

    def __init__(self, image_path, position, groups, size=(200, 200), life=100, lives=3, xp=0, has_hole=True):
        super().__init__(image_path, position, groups, size)
        self.image_path = image_path  # Salva o caminho da imagem para referência futura
        self.life = life
        self.lives = lives
        self.xp = xp
        self.size = size
        self.has_hole = has_hole  # <- NOVA PROPRIEDADE
        self.original_image = pygame.image.load("assets/charsSprite/player/indigenaM/R0.png").convert_alpha()
        self.image = pygame.transform.scale(self.original_image, size)
        self.rect = self.image.get_rect(topleft=position)
        self.in_hole = False
        self.facing_right = True
        self.is_dead = False
        self.fall_lock_x_range = None  # Guarda o intervalo do buraco

        self.vel = 5
        self.grav = 0.5
        self.jump_power = -15  # Velocidade inicial para o pulo
        self.is_jumping = False  # Verifica se está pulando
        self.on_ground = False  # Verifica se está no chão

        # Flags de direção e estado de movimento
        self.right = False
        self.left = False
        self.shots = pygame.sprite.Group()  # Grupo para armazenar os projéteis disparados
        self.shot_released = False  # Controla se já disparou a flecha neste ciclo
        self.current_frame = 0  # Controle do quadro atual da animação
        self.animation_speed = 5  # Velocidade de animação (controle de quadro)
        self.ticks = 0
        self.img = 0

        # Definindo as animações (idle, walk, shot, jump)
        self.animations = {
            "idle": [
                pygame.transform.scale(pygame.image.load(f"assets/charsSprite/player/indigenaM/R0.png"), size),
                pygame.transform.scale(pygame.image.load(f"assets/charsSprite/player/indigenaM/R1.png"), size)
            ],
            "walk": [
                pygame.transform.scale(pygame.image.load(f"assets/charsSprite/player/indigenaM/M{i}.png"), size)
                for i in range(8)
            ],
            "shot": [
                pygame.transform.scale(pygame.image.load(f"assets/charsSprite/player/indigenaM/S{i}.png"), size)
                for i in range(7)
            ],
            "jump": [
                pygame.transform.scale(pygame.image.load(f"assets/charsSprite/player/indigenaM/J{i}.png"), size)
                for i in range(17)
            ],            
        }

        # Animações espelhadas para esquerda
        self.animations["shot_left"] = [pygame.transform.flip(img, True, False) for img in self.animations["shot"]]
        self.animations["shot_right"] = self.animations["shot"]
        
        # Animações espelhadas para pulo
        self.animations["jump_left"] = [pygame.transform.flip(img, True, False) for img in self.animations["jump"]]
        self.animations["jump_right"] = self.animations["jump"]

        # Definindo o estado inicial
        self.state = "idle"
        self.image = self.animations[self.state][self.current_frame]  # Primeira Imagem
        self.rect = self.image.get_rect(topleft=position)  # Posição Inicial do jogador
        self.lives = lives  # Número de vidas (live)
        self.life = life  # Pontos de Vida (Zerou os pontos, perdeu uma Vida = Live)
        self.xp = 0  # Adicione esta linha para inicializar o XP
        self.gold = 0  # Exemplo de ouro
        self.dialog_active = False  # Flag para indicar se o diálogo está ativo
        self.dialog_npc = None  # Referência ao NPC com o qual está dialogando
    
    def update(self):
        """Atualiza o estado do jogador em cada quadro."""
        super().update()  # Chama o método da classe pai
        self.gravity()  # Aplica a gravidade
                        
        # Se o personagem estiver no buraco, desabilita o movimento
        if self.in_hole:
            self.right = False
            self.left = False

        # Se o personagem está atacando, ele não pode se mover
        if self.state != "shot":  # Só permite movimentação se não estiver atacando
            self.movements()  # Atualiza os movimentos laterais
        
        # Lógica para disparar o projétil
        self.shots.update()  # Atualiza todos os projéteis disparados

        # Animação baseada no estado do personagem
        if self.state == "shot":
            direction_anim = "shot_right" if self.facing_right else "shot_left"
            self.animate(direction_anim, 25, 7)
                        
        # Lógica de movimento e atualização
        if self.is_dead:
            return  # Se o personagem está morto, não faz mais nada

        # Verifica se o jogador está no diálogo
        if self.dialog_active:
            return  # Se o diálogo estiver ativo, o jogador não pode se mover   

        if self.check_death():  # Chama a função check_death
            if self.lives <= 0:
                self.die()  # Chama o método de morte se as vidas acabaram

    def gravity(self):
        """Aplica a gravidade ao jogador, verifica se caiu em buracos e trata colisão com o chão."""

        # Aplica gravidade
        self.vel += self.grav
        self.rect.y += self.vel

        # ⚠️ Verifica se há buracos definidos pela fase
        if hasattr(self, "holes"):
            for hole_rect in self.holes:
                # Se o centro inferior do jogador entra no buraco
                if hole_rect.collidepoint(self.rect.centerx, self.rect.bottom):
                    if not self.in_hole:
                        print("[DEBUG] Entrou no buraco!")
                        self.in_hole = True  # Marca que o jogador está caindo
                        self.fall_lock_x_range = (hole_rect.left, hole_rect.right)  # Salva os limites do buraco
                    break  # Não precisa verificar outros buracos

        # 🧊 Limita a velocidade de queda
        if self.vel >= 10:
            self.vel = 10

        # ✅ Só verifica colisão com o chão se NÃO estiver caindo em buraco
        if not self.in_hole:
            if self.rect.y >= GROUND_LEVEL - self.rect.height:
                self.rect.y = GROUND_LEVEL - self.rect.height
                self.vel = 0
                self.on_ground = True
                self.is_jumping = False
                
    def set_holes(self, hole_list):
        """Recebe uma lista de buracos (como retângulos) vindos da fase atual."""
        self.holes = hole_list
            
    def events(self, events):
        """Processa eventos de teclado para controlar o jogador."""
        if events.type == pygame.KEYDOWN:
            if events.key == pygame.K_d or events.key == pygame.K_RIGHT:
                self.right = True
            elif events.key == pygame.K_a or events.key == pygame.K_LEFT:
                self.left = True
            elif events.key == pygame.K_SPACE and self.on_ground:  # Verifica se está no chão antes de pular
                self.vel = self.jump_power  # Faz o jogador pular
                self.on_ground = False  # Marca como não está mais no chão
                self.is_jumping = True
                self.state = "jump"
                
            elif events.key == pygame.K_q:  # Tecla "Q" para disparar
                self.shot()  # Dispara o projétil
                self.state = "shot"  # Altera o estado para "shot" (disparo)
                    
            elif events.key == pygame.K_e:  # Tecla de ação para iniciar o diálogo
                if self.dialog_npc:  # Verifica se o jogador está perto de um NPC
                    self.start_dialogue(self.dialog_npc)
            
        elif events.type == pygame.KEYUP:
            if events.key == pygame.K_d or events.key == pygame.K_RIGHT:
                self.right = False
            elif events.key == pygame.K_a or events.key == pygame.K_LEFT:
                self.left = False
            elif events.key == pygame.K_q:  # Quando a tecla "Q" for solta, o jogador volta para o estado "idle"
                self.state = "idle"  # Retorna ao estado "idle" (sem disparo)
  
    def shot(self):
        """Dispara um projétil na direção do jogador e inicia a animação de ataque."""
        # Inicia a animação de "shot" no jogador
        self.state = "shot"  # Define o estado como "shot"
        self.current_frame = 0  # Reseta o quadro da animação

        # Atualiza a animação de disparo
        self.animate("shot", 25, 6)  # Chama animação de disparo
        
        self.shot_released = False  # Permite um novo disparo na nova animação
        
    def real_shot(self):
        """Dispara o projétil sincronizado com o frame da animação."""
        shot_y = self.rect.y + 60  # Ajuste fino conforme sprite
        if self.facing_right:
            shot_x = self.rect.x + 80  # Ajuste fino para a mão direita (experimente 130~150)
            shot = Shot(shot_x, shot_y, 1, self.shots, size=(80, 25))
        else:
            shot_x = self.rect.x + 30  # Ajuste fino para a mão esquerda (experimente 20~40)
            shot = Shot(shot_x, shot_y, -1, self.shots, size=(80, 25))
        self.shots.add(shot)
    
    def start_dialogue(self, npc):
        """Inicia o diálogo com o NPC."""
        self.dialog_active = True  # Ativa o diálogo
        print(f"{npc.__class__.__name__}: Bem-vindo, jovem guerreiro! O que procura?")
        # Aqui você pode adicionar mais lógicas para o diálogo, como exibir opções ou continuar com missões.
        # Durante o diálogo, o jogador não poderá se mover:
        self.is_moving = False  # Desativa o movimento do jogador

    def stop_dialogue(self):
        """Interrompe o diálogo."""
        self.dialog_active = False  # Desativa o diálogo
        self.is_moving = True  # Ativa novamente o movimento do jogador
        print("Diálogo finalizado.")            
    
    def movements(self):
        """Atualiza os movimentos laterais e a animação do jogador."""
        # Limite da tela (ajuste conforme o tamanho da tela)
        screen_width = 1280  # Largura da tela
        buffer = 75  # Permite ultrapassar 75px para fora dos limites da tela

        # Se o personagem está disparando (estado "shot")
        if self.state == "shot":
            # Define a direção do disparo e aplica a animação de disparo
            if self.facing_right:
                self.animate("shot_right", 25, 6)  # Animação de disparo para direita
            else:
                self.animate("shot-left", 25, 6)  # Animação de disparo para esquerda (pode usar uma animação específica para esquerda, se necessário)
            
            # Não altera a rotação da imagem durante o disparo
            # Não precisamos alterar a imagem aqui, pois a rotação é tratada fora dessa parte
            return  # Retorna, pois não precisamos fazer mais nada enquanto dispara
        
        # Movimento para a direita
        if self.right:
            next_x = self.rect.x + 2.8
            
            if self.in_hole:
                # Só permite movimento para a direita dentro do buraco
                if self.fall_lock_x_range and next_x + self.rect.width <= self.fall_lock_x_range[1]:
                    self.rect.x = next_x
            else:
                if next_x + self.rect.width - buffer < screen_width:
                    self.rect.x = next_x
            
            # Permite ultrapassar 75px além da borda direita
            if self.rect.x + self.rect.width - buffer < screen_width:
                self.facing_right = True  # Atualiza a direção para a direita
            self.state = "walk"  # Altera o estado para "walk"
            self.animate("walk", 15, 7)  # Chama animação de caminhada para direita

        # Movimento para a esquerda
        elif self.left:
            next_x = self.rect.x - 2.8
            
            if self.in_hole:
                # Só permite movimento para a esquerda dentro do buraco
                if self.fall_lock_x_range and next_x >= self.fall_lock_x_range[0]:
                    self.rect.x = next_x
            else:
                if next_x + buffer > 0:
                    self.rect.x = next_x
                        
            # Permite ultrapassar 75px além da borda esquerda
            if self.rect.x + buffer > 0:
                self.facing_right = False  # Atualiza a direção para a esquerda
            self.state = "walk"  # Altera o estado para "walk"
            self.animate("walk", 15, 7)  # Chama animação de caminhada para esquerda

        # Caso contrário, animação de espera (idle)
        else:
            self.state = "idle"  # Altera o estado para "idle"
            self.animate("idle", 100, 1)  # Animação de espera (idle)

        # Agora, aplica a rotação da imagem com base na direção (movimento ou idle)
        if self.facing_right:
            self.image = pygame.transform.flip(self.image, False, False)  # Direção direita
        else:
            self.image = pygame.transform.flip(self.image, True, False)  # Direção esquerda

        # Animação de Pulo
        if self.is_jumping:
            direction_anim = "jump_right" if self.facing_right else "jump_left"
            self.animate(direction_anim, 50, 17)

    def animate(self, name, ticks, limit):
        """Anima o personagem com uma sequência de imagens."""
        self.ticks += 1  # Incrementa o contador de ticks

        # Controla a troca de frames com base no número de ticks
        if self.ticks >= ticks:
            self.ticks = 0  # Reseta o contador de ticks
            self.img += 1  # Avança para o próximo quadro da animação

        # Verifique o número de quadros disponíveis para a animação atual
        frames = self.animations.get(name, [])  # Obtém os frames da animação
        num_frames = len(frames)

        # Se a animação não tiver quadros, não faz nada
        if num_frames == 0:
            return

        # Reseta para o primeiro quadro se chegar ao final
        if self.img >= num_frames:
            self.img = 0

        # Atualiza a imagem do personagem com o novo quadro da animação
        self.image = frames[self.img]
        self.rect = self.image.get_rect(topleft=self.rect.topleft)  # Atualiza a posição do sprite

        # Verifica se está na animação de disparo e no frame S4 (índice 4)
        if name.startswith("shot") and self.img == 4 and not self.shot_released:
            self.real_shot()  # Dispara a flecha
            self.shot_released = True  # Garante que só dispare uma vez neste ciclo

        # Reinicia o ciclo de disparo se chegar ao fim da animação
        if self.img >= num_frames - 1 and name.startswith("shot"):
            self.shot_released = False  # Permite novo disparo no próximo ciclo


    def check_death(self):
        """Verifica se o jogador passou da base da tela e trata a perda de vida."""
        
        # Só morre quando passa da base da tela
        if self.rect.y > BASE_HEIGHT:
            self.lives -= 1
            print(f"[DEBUG] Morreu. Vidas restantes: {self.lives}")
            if self.lives > 0:
                # Reposiciona em local seguro
                self.rect.x, self.rect.y = 100, 250
                self.vel = 0
                self.on_ground = False
                self.is_jumping = False
                self.in_hole = False  # Libera para próxima queda
                return True
            else:
                self.die()
                return False

        # Não morreu ainda
        return False
    
    def lose_life(self):
        """Chama a função para perder uma vida."""
        self.lives -= 1  # Diminui a quantidade de vidas
        if self.lives <= 0:
            self.die()  # Se não tiver mais vidas, chama a função de morte
    
    def die(self):
        """Define o estado do personagem como morto."""
        self.is_dead = True

         
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
            

class Boss_Mapinguari(Obj):
    """Classe para representar o Boss estático 'Mapinguari' com animação idle sempre virado para a esquerda."""

    def __init__(self, position, groups, size=(400, 400)):
        # Caminho base da imagem
        image_path = os.path.join("assets", "charsSprite", "bosses", "Mapinguari_1.png")
        super().__init__(image_path, position, groups, size)
        
        self.size = size
        self.state = "idle"
        self.current_frame = 0
        self.ticks = 0
        self.animation_speed = 40

        # Carrega animações
        self.animations = {"idle": []}

        # Para simular uma animação, carregue imagens diferentes ex: Mapinguari_1.png, Mapinguari_2.png
        for i in range(1, 3):  # Espera Mapinguari_1.png e Mapinguari_2.png
            path = os.path.join("assets", "charsSprite", "bosses", f"Mapinguari_{i}.png")
            img = pygame.image.load(path).convert_alpha()
            img = pygame.transform.scale(img, self.size)
            self.animations["idle"].append(img)

        # Define imagem inicial
        self.image = self.animations[self.state][self.current_frame]
        self.rect = self.image.get_rect(topleft=position)

    def update(self):
        """Atualiza a animação do boss."""
        self.animate(self.state)

    def animate(self, name):
        """Executa animação do boss."""
        self.ticks += 1
        if self.ticks >= self.animation_speed:
            self.ticks = 0
            self.current_frame = (self.current_frame + 1) % len(self.animations[name])
            self.image = self.animations[name][self.current_frame]
            self.rect = self.image.get_rect(topleft=self.rect.topleft)

    def interact(self, player):
        """Define interação do boss com o jogador (ex: início de combate)."""
        if self.rect.colliderect(player.rect):
            print("Mapinguari: VOCÊ ATRAVESSOU OS LIMITES! PREPARE-SE PARA LUTAR.")
            # Aqui você pode iniciar o combate, mostrar HUD de batalha, etc.
            

class ChatBox:
    """Classe para exibir mensagens de diálogo na tela."""

    def __init__(self, font, position, size):
        self.font = font  # Fonte padrão para diálogos
        self.small_font = pygame.font.Font(None, 24)  # Fonte menor para perguntas e alternativas
        self.position = position
        self.size = size
        self.rect = pygame.Rect(position, size)
        self.color = (BLACK_COLOR)
        self.text_color = (WHITE_COLOR)
        self.messages = []  # Lista de mensagens/questões
        self.current_message = 0  # Índice da mensagem atual
        self.active = False  # Indica se o chatbox está ativo
        self.option_index = 0  # Índice da opção selecionada
        self.score = 0  # Pontuação do jogador
        self.title = ""  # Título da pergunta
        self.question = ""  # Texto da pergunta
        self.options = []  # Opções de resposta
        self.correct_answers = []  # Respostas corretas das questões

    def display_messages(self, messages):
        """Ativa o chatbox com um conjunto de mensagens."""
        # Converte as mensagens para strings, se necessário
        self.messages = [str(msg) for msg in messages]
        self.current_message = 0
        self.active = True
        self.options = []  # Limpa opções de resposta

    def display_question(self, title, question, options):
        """Exibe uma pergunta com título e opções."""
        self.title = title  # Define o título da pergunta
        self.question = question if isinstance(question, str) else ' '.join(question)  # Garante que a pergunta seja string
        self.options = options  # Define as opções de resposta
        self.option_index = 0  # Reseta o índice da opção selecionada
        self.active = True  # Ativa o chatbox para exibição

    def next_message(self):
        """Avança para a próxima mensagem ou termina o diálogo."""
        if self.options:  # Se houver opções, não avança mais mensagens
            return
        self.current_message += 1
        if self.current_message >= len(self.messages):  # Termina o diálogo
            self.active = False  # Desativa o chatbox

    def validate_answer(self):
        """Valida a resposta do jogador e avança o diálogo."""
        if self.options and self.correct_answers:
            selected_option = self.options[self.option_index]
            if selected_option == self.correct_answers[0]:  # Verifica se está correto
                self.score += 1
                print("Resposta correta!")
            else:
                print("Resposta errada.")
            self.active = False  # Fecha a questão

    def previous_option(self):
        """Move para a opção anterior."""
        if self.options:
            self.option_index = (self.option_index - 1) % len(self.options)

    def next_option(self):
        """Move para a próxima opção."""
        if self.options:
            self.option_index = (self.option_index + 1) % len(self.options)
            
    def select_option(self):
        """Retorna a opção atualmente selecionada."""
        if self.options:  # Certifica-se de que há opções disponíveis
            return self.options[self.option_index]
        return None  # Caso não haja opções, retorna None        

    def is_active(self):
        """Verifica se o chatbox está ativo."""
        return self.active

    def draw(self, screen):
        """Desenha a chatbox e seu conteúdo na tela."""
        if not self.active:
            return  # Não desenha nada se o chatbox não estiver ativo

        # Desenhar o retângulo do chatbox
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)

        # Define a margem e calcula o espaço disponível
        margin = 20  # Margem de 20px em torno do texto
        available_height = self.rect.height - 2 * margin
        y_offset = self.rect.y + margin

        # Exibir título, se houver, e atualizar o espaço disponível
        if self.title:
            title_surface = self.font.render(self.title, True, self.text_color)
            screen.blit(title_surface, (self.rect.x + margin, y_offset))
            y_offset += 40  # Espaço após o título
            available_height -= 40

        # Exibir pergunta, se houver
        if self.question:
            wrapped_question = self.wrap_text(str(self.question), self.rect.width - 2 * margin)
            for line in wrapped_question:
                if available_height < 20:  # Verifica se há espaço para desenhar
                    break
                question_surface = self.font.render(line, True, self.text_color)
                screen.blit(question_surface, (self.rect.x + margin, y_offset))
                y_offset += 20  # Espaço entre as linhas da pergunta
                available_height -= 20

        # Exibir opções, se houver
        if self.options:
            y_offset += 20  # Espaço entre a pergunta e as opções
            available_height -= 20
            for i, option in enumerate(self.options):
                wrapped_option = self.wrap_text(str(option), self.rect.width - 2 * margin, self.small_font)
                for line in wrapped_option:
                    if available_height < 20:  # Verifica se há espaço para desenhar
                        break
                    color = (255, 255, 0) if i == self.option_index else self.text_color  # Amarelo para a opção selecionada
                    option_surface = self.small_font.render(line, True, color)
                    screen.blit(option_surface, (self.rect.x + margin, y_offset))
                    y_offset += 20  # Espaço entre as linhas da opção
                    available_height -= 20
                y_offset += 10  # Espaço extra entre as opções

        # Exibir mensagem atual (para diálogos simples)
        elif self.messages and self.current_message < len(self.messages):
            wrapped_message = self.wrap_text(self.messages[self.current_message], self.rect.width - 2 * margin)
            for line in wrapped_message:
                if available_height < 30:  # Verifica se há espaço para desenhar
                    break
                message_surface = self.font.render(line, True, self.text_color)
                screen.blit(message_surface, (self.rect.x + margin, y_offset))
                y_offset += 30  # Espaço entre as linhas
                available_height -= 30
                
    def wrap_text(self, text, max_width, font=None):
        """Divide o texto em múltiplas linhas para caber na largura da caixa."""
        if text is None:
            return []  # Retorna uma lista vazia se o texto for None
        if font is None:
            font = self.font  # Usa a fonte padrão se nenhuma for especificada
        words = text.split(' ')  # Garante que `text` seja uma string
        lines = []
        current_line = []

        for word in words:
            current_line.append(word)
            test_line = ' '.join(current_line)
            if font.size(test_line)[0] > max_width:
                current_line.pop()  # Remove a última palavra que excedeu
                lines.append(' '.join(current_line))
                current_line = [word]

        if current_line:  # Adiciona a última linha
            lines.append(' '.join(current_line))

        return lines
                
# Biblioteca de diálogos
class Dialogo_1_1:
    """Biblioteca contendo os diálogos da interação entre o jogador e o NPC."""
    falas = [
        ("Cacique:",
            "Jovem guerreiro, o momento é grave! O equilíbrio sagrado que protege nossa terra foi rompido!!!"),
        ("Jovem Guerreiro:",
            "Como isso poderia acontecer? O Ídolo guardava o espírito das nossas florestas e rios..."),
        ("Cacique:",
            "Forças sombrias o usurparam, e agora o equilíbrio natural se desfaz! As criaturas místicas, que antes viviam em harmonia conosco, tornaram-se ferozes e hostis! Seus ataques ameaçam nossa terra e até os guardiões ancestrais!"),
        ("Jovem Guerreiro:",
            "...precisamos recuperá-lo! Mas como enfrentar tamanha ameaça?"),            
        ("Cacique:",
            "Para isso, você deve provar que carrega a sabedoria dos nossos ancestrais! Somente aquele que compreende as tradições estará pronto para a missão! Passe por estes cinco testes, e verá se está preparado para seguir nesta jornada!!!"),
        ("Cacique:",
            "Agora você está pronto para entender: 'ESTA JORNADA NÃO É APENAS SUA'!!! Guerreiros de todas as culturas devem unir suas forças! Cada povo carrega saberes únicos que serão essenciais nesta missão! Juntos, restauraremos o sagrado em seu local de origem!!!"),
        ("Jovem Guerreiro:",
            "Seremos a voz dos antigos e a força dos Deuses! Recuperaremos o Ídolo e traremos a paz de volta!"),
        ("Cacique:",
            "Lembre-se, a força verdadeira não reside nos braços, mas na união dos corações e na sabedoria compartilhada! Vá e encontre outros guerreiros, juntos, tragam de volta a paz para nossa terra!!!"), 
    ]

# Biblioteca de questões
class Questoes_1_1:
    """Biblioteca contendo as questões e respostas do teste de conhecimento."""
    perguntas = [
        {
            "titulo": "Questão: O Som da Natureza:",
            "pergunta": "Nossa música é mais do que som: é uma oração viva, conectando-nos aos espíritos das matas e rios. Diga-me, jovem guerreiro, quais instrumentos nossos ancestrais utilizam para conversar com os deuses da natureza?",
            "opcoes": [
                "Instrumentos de sopro, moldados com bambu ou ossos, que imitam o vento e os animais.",
                "Instrumentos de percussão, feitos com troncos ocos e couro animal, que ressoam como o coração da terra.",
                "Instrumentos de corda, esculpidos com habilidade, ressoando melodias da alma humana.",
                "Instrumentos eletrônicos, que dependem da energia dos homens, não da natureza."
            ],
            "resposta_correta": "Instrumentos de sopro, moldados com bambu ou ossos, que imitam o vento e os animais.",
            "pontos": 10
        },
        {
            "titulo": "Questão: A Arte da Luta:",
            "pergunta": "A verdadeira força vem do espírito e da tradição. Qual luta ancestral herdamos, usada não só para defender, mas para honrar nossa cultura?",
            "opcoes": [
                "Jiu-jitsu, técnica de domínio pelo chão, mas de origem distante.",
                "Huka-Huka, combate de levantamentos e derrubadas.",
                "Capoeira, luta-dança de outras influências culturais.",
                "Boxe, a arte dos punhos, que veio de terras estrangeiras.",
            ],
            "resposta_correta": "Huka-Huka, combate de levantamentos e derrubadas.",
            "pontos": 10
        },
        {
            "titulo": "Questão: Escrita Ancestral:",
            "pergunta": "Antes da chegada de outros povos, nossos ancestrais já narraram histórias com símbolos vivos. Que forma de comunicação usamos para registrar saberes e tradições?",
            "opcoes": [
                "Faixas Decorativas com formas geométricas, linhas e tramas em estamparia de roupas, em que as cores também são classificadas como um sistema de código e escrita de acordo com a comunidade a que está vinculada.",
                "Caligrafia, uso de tintas e papiros para registro de palavras, usanto elementos simbólicos ou signos, que representam letras e números.",
                "Pedras com símbolos esculpidos que são conhecidas como 'Runas', sendo jogadas e dependendo da ordem e sequencia que caírem significa uma informação.",
                "Pinturas Corporais, com hachuras, linhas e tramas, que utilizam pigmentos naturais extraídos de minérios e vegetais, representando o nível de responsabilidade e importancia da pessoa dentro da comunidade que atua."
            ],
            "resposta_correta": "Pinturas Corporais, com hachuras, linhas e tramas, que utilizam pigmentos naturais extraídos de minérios e vegetais, representando o nível de responsabilidade e importancia da pessoa dentro da comunidade que atua.",
            "pontos": 20
        },
        {
            "titulo": "Questão: Palavras do Espírito Ancestral",
            "pergunta": "Nossa língua vive em palavras que muitos falam sem conhecer sua origem. Quais são as origens do coração da nossa terra?",
            "opcoes": [
                "Mesa, Relógio, Camiseta, Hospital, Cerveja.",
                "Zen, Quimono, Origami, Chá, Sushi.",
                "Igarapé, Jabuticaba, Caiçara, Mirim, Pindorama.",
                "Moleque, Maracatu, Caxixi, Fubá, Dendê."
            ],
            "resposta_correta": "Igarapé, Jabuticaba, Caiçara, Mirim, Pindorama.",
            "pontos": 30
        },
        {
            "titulo": "Questão: O Alimento da Terra:",
            "pergunta": "A terra nos sustenta e a comida que cultivamos reflete quem somos. Qual é a essência da nossa culinária, que fortalece o corpo e honra a tradição?",
            "opcoes": [
                "Mandioca, Milho, Peixe, Frutas, Carne.",
                "Milho, Feijão, Mandioca, Dendê, Couve.",
                "Peixe, Batata, Trigo, Azeite, Ervas.",
                "Peixe, Arroz, Algas, Shoyu, Tofu."
            ],
            "resposta_correta": "Mandioca, Milho, Peixe, Frutas, Carne.",
            "pontos": 30
        },
    ]
            
