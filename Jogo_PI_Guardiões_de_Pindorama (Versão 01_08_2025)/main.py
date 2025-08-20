import pygame, sys
from script.scenes import *
from script.setting import *
from script.obj import *

# Criando a Classe de Jogo
class Game:
        
    # Iniciando a Veblzrificação do Sistema
    def __init__(self):
        pygame.init()  # Inicializa todos os módulos do Pygame
        pygame.mixer.init()  # Inicializa o mixer de som do Pygame
        
        # Define o ícone da janela do jogo
        icon = pygame.image.load("assets/menu/Icon.png")  # Carrega o ícone
        pygame.display.set_icon(icon)  # Define o ícone da janela
        pygame.display.set_caption("Guardiões de Pindorama")  # Define o título da janela
        
        # Desenhando o Display de Jogo, com o título do jogo na janela
        self.display = pygame.display.set_mode((BASE_WIDTH, BASE_HEIGHT), pygame.RESIZABLE)  # Cria a tela do jogo
        self.clock = pygame.time.Clock()  # Cria um objeto Clock para controlar a taxa de quadros
        self.fullscreen = False  # Controle de estado de Tela Cheia
        
        # Inicializa a cena atual com a tela de título
        self.current_scene = Login()  # Definindo a cena inicial como Login
        
        # Inicializa o jogador
        image_path = "assets/charsSprite/player/indigenaM/R0.png"
        position = (100, 250)  # Exemplo de posição inicial
        groups = []  # Adicione os grupos de sprites se necessário
        self.player = Player(image_path, position, groups)
        
        # Informações da tela
        self.virtual_screen = pygame.Surface((BASE_WIDTH, BASE_HEIGHT))  # Cria uma superfície virtual
        
    def toggle_fullscreen(self):
        """Alterna entre o modo janela e o modo tela cheia."""
        if self.fullscreen:
            # Retorna ao modo janela redimensionável
            self.display = pygame.display.set_mode((BASE_WIDTH, BASE_HEIGHT), pygame.RESIZABLE)
            self.fullscreen = False
        else:
            # Alterna para o modo tela cheia de acordo com a resolução do monitor
            self.display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.fullscreen = True
            
    def handle_events(self):
        """Gerencia os eventos, como teclas pressionadas e outros."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Se o evento for de saída
                pygame.quit()  # Encerra o Pygame
                sys.exit()  # Sai do programa
            
            # Passa o evento para a cena atual
            self.current_scene.handle_events(event)
            
    def update(self):
        """Atualiza o estado do jogo, incluindo o jogador e as cenas."""
        # Atualiza o jogador
        self.player.update()
        
        # Verifica se o jogador perdeu todas as vidas
        if self.player.check_death():
            if self.player.is_dead:
                self.current_scene = GameOver()  # Muda para a cena de Game Over
       
    def render(self):
        """Desenha a tela do jogo e a cena atual."""
        # Limpa a tela
        self.virtual_screen.fill("black")  # Preenche a tela virtual com preto
                      
        # Renderiza a cena atual passando a `virtual_screen`
        if self.current_scene:  # Verifica se a cena atual é válida
            self.current_scene.draw(self.virtual_screen)  # Desenha a cena atual
            self.current_scene.update()  # Atualiza o estado da cena

            if self.current_scene.next is not None:
                self.current_scene = self.current_scene.next  # Atualiza para a próxima cena, se necessário
        
        # Escala a tela virtual para a proporção correta
        current_width = self.display.get_width()
        current_height = self.display.get_height()      
        
        # Calcula a escala proporcional
        scale_width = current_width / BASE_WIDTH
        scale_height = current_height / BASE_HEIGHT
        scale = min(scale_width, scale_height)  
                
        # Novo tamanho escalado mantendo a proporção
        new_width = int(BASE_WIDTH * scale)
        new_height = int(BASE_HEIGHT * scale)
        scaled_screen = pygame.transform.scale(self.virtual_screen, (new_width, new_height))
            
        # Centraliza a tela escalada
        x_offset = (current_width - new_width) // 2
        y_offset = (current_height - new_height) // 2
        self.display.fill("black")  # Preenche o fundo para evitar barras
        self.display.blit(scaled_screen, (x_offset, y_offset))
    
    def run(self):
        """Executa o loop principal do jogo."""
        try:
            while True:  # Loop principal do jogo
                self.handle_events()  # Gerencia os eventos do jogo
                self.update()  # Atualiza o jogo e as condições
                self.render()  # Renderiza a cena atual do jogo
                # Atualiza a tela
                pygame.display.update()  # Atualiza a tela principal
                self.clock.tick(FPS)  # Controla a taxa de quadros do jogo
        
        except KeyboardInterrupt:
            print("[Jogo] Encerrado pelo usuário.")
        
        finally:
            pygame.quit()
            sys.exit()
         

# Realizando Segurança, informando que a programação só
# funcionará se rodar a aplicação pelo Arquivo Main.py
if __name__ == "__main__":          
    game = Game()  # Cria uma instância da classe Game
    game.run()  # Executa o método run da instância do jogo


