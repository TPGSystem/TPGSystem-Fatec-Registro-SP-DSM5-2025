import pygame, sys, json  # Importa as bibliotecas necessárias
import random
from script.obj import *  # Importa todas as classes do módulo obj
from script.setting import *  # Importa todas as configurações do módulo setting

# Criando Classes para estruturar o Jogo:
# Criando Cenas
class Scene:
    """Classe base para todas as cenas do jogo."""
    
    def __init__(self, font_path="assets/font/Primitive.ttf", font_size=36):
        pygame.init()  # Certifique-se de que o Pygame esteja inicializado
        
        self.next = self  # Inicializa a próxima cena como a cena atual
        self.display = pygame.display.get_surface()  # Obtém a superfície de exibição atual
        self.all_sprites = pygame.sprite.Group()  # Cria um grupo de sprites
        
        self.fade = Fade("black")  # Cria um efeito de fade inicial
        self.sound_click = pygame.mixer.Sound("assets/sounds/click.ogg")  # Carrega o som de clique
        self.sound_click.set_volume(0.25)  # Ajusta o volume para 25%
        
        self.option_data = self.load_file("teste.json")  # Carrega as opções do jogo de um arquivo JSON
        
        # Inicialização da fonte
        self.font = pygame.font.Font(font_path, font_size)  # Define a fonte a ser utilizada
        
    def start_music(self):
        """Inicia a música de fundo."""
        loop = -1  # Loop infinito para a música
        pygame.mixer.music.load("assets/sounds/music1.mp3")  # Carrega a música de fundo
        
        if self.option_data["music_set_volume"] != 0:                
            pygame.mixer.music.play(loop)  # Toca a música
            pygame.mixer.music.set_volume(self.option_data["music_set_volume"])  # Define o volume da música

    # Identificando Eventos
    def handle_events(self, event):
        """Trata os eventos da cena atual."""
        pass  # As subclasses podem sobrescrever esse método para lidar com teclado/mouse
                
    # "Desenhar" as informações na Cena
    def draw(self, display):
        """Desenha todos os sprites e o efeito de fade na tela."""
        self.all_sprites.draw(display)  # Desenha todos os sprites
        self.fade.draw(display)  # Desenha o efeito de fade
    
    # Atualizando as Informações na Tela            
    def update(self):
        """Atualiza todos os sprites e o efeito de fade."""
        self.all_sprites.update()  # Atualiza todos os sprites
        self.fade.update()  # Atualiza o efeito de fade
        
    # Direcionando o sistema para próximas Telas/Cena/Fase    
    def change_scene(self, next_scene):
        """Altera a cena atual para a próxima cena especificada."""
        self.next = next_scene
        
    # Salvando Dados (Options, Level, GameOver) - json
    def save_file(self, arquivo, dados):
        """Salva dados em um arquivo JSON."""
        with open(arquivo, "w") as dados_do_arquivo:
            json.dump(dados, dados_do_arquivo)  # Salva os dados no arquivo
            print("OK")  # Mensagem de confirmação
    
    # Carregando Dados Salvo - json        
    def load_file(self, arquivo):
        """Carrega dados de um arquivo JSON."""
        with open(arquivo, "r") as dados_do_arquivo:
            dados = json.load(dados_do_arquivo)  # Carrega os dados do arquivo
            
        return dados  # Retorna os dados carregados
    
    
# Criando Tela de Login de Usuário
class Login(Scene):
    """Classe para a tela de Login."""
    
    def __init__(self):
        super().__init__()  # Chama o construtor da classe base
        
        # Carregando imagens de fundo e botões
        self.background = Obj("assets/login/background.png", [0, 0], [self.all_sprites])
        self.form_body = Obj("assets/login/FormBody.png", [428, 55], [self.all_sprites])
        self.login_button = Obj("assets/login/Button.png", [541, 460], [self.all_sprites])  # Botão de Login
                
        # Configuração de fontes
        self.title_font = pygame.font.Font(None, 36)  # Fonte para o título da tela
        self.label_font = pygame.font.Font(None, 24)  # Fonte para as labels de texto
        self.font = pygame.font.Font(None, 24)  # Fonte para campos de entrada
                
        # Campos de entrada
        self.RA_rect = pygame.Rect(470, 235, 340, 40)  # Campo de RA
        self.password_rect = pygame.Rect(470, 337, 340, 40)  # Campo de Senha
        self.active_field = None  # Para controlar qual campo está ativo
        self.login_button_rect = self.login_button.rect  # Retângulo do botão de login
        self.active_field = "RA"  # Inicia com o campo RA como ativo
        self.RA_text = ""
        self.password_text = ""
        
        # Cores para campos de entrada
        self.color_active = pygame.Color('dodgerblue')
        self.color_inactive = pygame.Color('gray')
        
        # Dados de login simulados (pode ser integrado com um banco de dados)
        #self.correct_login = "RA123456"
        #self.correct_password = "123"
    
    def validate_login(self):
        """Valida se o RA e Senha correspondem aos dados cadastrados."""
        return self.RA_text == self.correct_login and self.password_text == self.correct_password
    
    def handle_events(self, event):
        """Gerencia eventos de entrada do usuário."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                # Apenas redireciona para a próxima tela ao pressionar Enter
                self.change_scene(Title())  # Redireciona para a próxima tela (Título)
        
        
        #Código Desativado para acesso sem Login e Senha
        #if event.type == pygame.KEYDOWN:
            #if event.key == pygame.K_TAB:  # Quando TAB é pressionado, alterna o campo
                #if self.active_field == "RA":
                    #self.active_field = "Senha"  # Muda para o campo de Senha
                #elif self.active_field == "Senha":
                    #self.active_field = "Login"  # Muda para o botão de login
                #elif self.active_field == "Login":
                    #self.active_field = "RA"  # Muda de volta para o campo RA
            #elif self.active_field == "RA":
                #if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:  # Salta para o campo de senha
                    #self.active_field = "Senha"
                #elif event.key == pygame.K_BACKSPACE:
                    #self.RA_text = self.RA_text[:-1]
                #else:
                    #self.RA_text += event.unicode
            #elif self.active_field == "Senha":
                #if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER: # Verifica o login ao pressionar Enter
                    #if self.validate_login():
                        #self.change_scene(Title())  # Redireciona para a tela de título
                    #else:
                        #print("RA ou Senha Incorretos!")  # Mensagem de erro
                #elif event.key == pygame.K_BACKSPACE:
                    #self.password_text = self.password_text[:-1]
                #else:
                    #self.password_text += event.unicode
            #elif self.active_field == "Login":  # Se o foco estiver no botão de login
                #if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:  # Verifica o login ao pressionar Enter
                    #if self.validate_login():
                        #self.change_scene(Title())  # Redireciona para a tela de título
                    #else:
                        #print("RA ou Senha Incorretos!")  # Mensagem de erro
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
        # Opcional: se você quiser permitir o clique no botão para avançar
            if self.login_button.rect.collidepoint(event.pos):
                self.change_scene(Title())  # Redireciona para a próxima tela (Título)
            
        
        #Código Desativado para acesso sem Login e Senha
        #elif event.type == pygame.MOUSEBUTTONDOWN:
            # Verifica se o clique foi em algum dos campos de texto
            #if self.RA_rect.collidepoint(event.pos):
                #self.active_field = "RA"
            #elif self.password_rect.collidepoint(event.pos):
                #self.active_field = "Senha"
            #elif self.login_button_rect.collidepoint(event.pos):
                #self.active_field = "Login"
            #else:
                #self.active_field = None
            
            # Verifica clique no botão de login
            #if self.login_button.rect.collidepoint(event.pos):
                #if self.validate_login():
                    #self.change_scene(Title())  # Redireciona para a tela de título
                #else:
                    #print("RA ou Senha Incorretos!")  # Mensagem de erro
        
        return super().handle_events(event)
        
    def draw(self, surface):
        """Renderiza a tela de login."""
        surface.fill((0, 0, 0))  # Limpa a tela com uma cor de fundo

        # Desenha todos os sprites (background e botões)
        self.all_sprites.draw(surface)

        # Título da tela
        title_surface = self.title_font.render("Venha para a Aventura!", True, pygame.Color(BLACK_COLOR))
        title_rect = title_surface.get_rect(center=(surface.get_width() // 2, 120))  # Centraliza no eixo X e ajusta o eixo Y
        surface.blit(title_surface, title_rect.topleft)  # Usa o canto superior esquerdo do retângulo

        # Labels para os campos de entrada
        RA_label_surface = self.label_font.render("Digite seu RA:", True, pygame.Color(BLACK_COLOR))
        RA_label_rect = RA_label_surface.get_rect(topleft=(470, 209))  # Define posição inicial do texto RA
        surface.blit(RA_label_surface, RA_label_rect.topleft)

        password_label_surface = self.label_font.render("Digite sua Senha:", True, pygame.Color(BLACK_COLOR))
        password_label_rect = password_label_surface.get_rect(topleft=(470, 310))  # Define posição inicial do texto Senha
        surface.blit(password_label_surface, password_label_rect.topleft)

        # Desenha campos de texto
        RA_color = self.color_active if self.active_field == "RA" else self.color_inactive
        password_color = self.color_active if self.active_field == "Senha" else self.color_inactive

        pygame.draw.rect(surface, RA_color, self.RA_rect, 2)  # Contorno do campo RA
        pygame.draw.rect(surface, password_color, self.password_rect, 2)  # Contorno do campo Senha

        # Renderiza o texto digitado
        RA_surface = self.font.render(self.RA_text, True, pygame.Color(BLACK_COLOR))
        password_surface = self.font.render("*" * len(self.password_text), True, pygame.Color(BLACK_COLOR))  # Oculta senha com asteriscos

        surface.blit(RA_surface, (self.RA_rect.x + 5, self.RA_rect.y + 5))
        surface.blit(password_surface, (self.password_rect.x + 5, self.password_rect.y + 5))
        
        # Destacar o botão de login quando estiver focado
        if self.active_field == "Login":
            pygame.draw.rect(surface, self.color_active, self.login_button_rect, 2)
        
    def update(self):
        """Atualiza a lógica da tela."""
        self.all_sprites.update()
        
# Criando Tela Inicial do Jogo
class Title(Scene):
    """Classe para a tela inicial do jogo."""
    
    def __init__(self):
        super().__init__()  # Chama o construtor da classe base
        
        # Criação de objetos de fundo e outros elementos da tela
        self.bg = Obj("assets/menu/Fundo.png", [0, 0], [self.all_sprites], size=(1400, 850))
        self.bg_mold = Obj("assets/menu/Moldura.png", [0, 0], [self.all_sprites])
        self.title = Obj("assets/menu/Titulo.png", [535, 50], [self.all_sprites], size=(700, 285))
        self.char1 = Obj("assets/menu/Indigena.png", [185, -10], [self.all_sprites], size=(450, 770))
        self.char2 = Obj("assets/menu/Bandeirantes.png", [12, 155], [self.all_sprites], size=(320, 575))
        self.char3 = Obj("assets/menu/Africano.png", [-240, 280], [self.all_sprites], size=(825, 650))
        self.star_text = Obj("assets/menu/Jogar.png", [822, 385], [self.all_sprites], size=(225, 80))
        self.options_text = Obj("assets/menu/Opcoes.png", [822, 485], [self.all_sprites], size=(275, 80))
        self.exit_text = Obj("assets/menu/Sair.png", [822, 585], [self.all_sprites], size=(175, 75))
        self.indicator = Obj("assets/menu/Cursor.png", [695, 385], [self.all_sprites], size=(110, 70))  # Cursor
        self.indicator_dir = 1  # Direção do movimento do cursor
        self.indicator_choose = 0  # Opção atualmente selecionada
        
        # Variáveis de movimento do BG
        self.bg_pos = [0, 0]  # Posição inicial do fundo
        self.bg_target = (-120, 0)  # Primeira posição alvo
        self.bg_vel = 1  # Velocidade de movimento do fundo

        # Pré-carregar a Música na memória e a opção de Tela Salva
        self.start_music()  # Inicia a música
        self.start_screen()  # Configura a tela inicial
        
    def start_screen(self):    
        """Configura a tela inicial com base nas opções salvas."""
        if self.option_data["display_text_values"] == "Fullscreen" and self.option_data["start"] == "on":
            pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # Muda para tela cheia
            self.option_data["start"] = "off"  # Atualiza o estado
            self.save_file("teste.json", self.option_data)  # Salva as opções

    def handle_events(self, event):
        """Gerencia eventos de entrada do usuário na tela inicial."""
        # Verifica se o evento recebido é uma tecla pressionada
        if event.type == pygame.KEYDOWN or event.type == pygame.K_KP_ENTER:
            # Chama a função para definir a opção selecionada com base no evento
            self.indicator_set_option(event)
            # Chama a função para atualizar a posição do indicador baseado no evento
            self.indicator_position(event)

    def indicator_set_option(self, event):
        """Define a opção selecionada com base na tecla pressionada."""
        if (event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER) and self.indicator_choose == 0:
            self.change_scene(Control())  # Muda para a cena de seleção de personagem
        if (event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER) and self.indicator_choose == 1:
            self.change_scene(Option())  # Muda para a cena de opções
        elif (event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER) and self.indicator_choose == 2:
            self.option_data["start"] = "on"  # Atualiza o estado
            self.save_file("teste.json", self.option_data)  # Salva os dados
            pygame.quit()  # Encerra o Pygame
            sys.exit()  # Sai do programa

    def indicator_position(self, event):
        """Atualiza a posição do indicador com base nas teclas pressionadas."""
        if event.key == pygame.K_DOWN or event.key == pygame.K_s:
            self.sound_click.play()  # Toca o som de clique
            if self.indicator_choose <= 1:
                self.indicator_choose += 1  # Move para a próxima opção
                if self.indicator_choose == 0:
                    self.indicator.rect.y = 384  # Atualiza a posição do cursor
                elif self.indicator_choose == 1:
                    self.indicator.rect.y = 484
                elif self.indicator_choose == 2:
                    self.indicator.rect.y = 584
                        
        elif event.key == pygame.K_UP or event.key == pygame.K_w:
            self.sound_click.play()  # Toca o som de clique
            if self.indicator_choose > 0:
                self.indicator_choose -= 1  # Move para a opção anterior
                if self.indicator_choose == 0:
                    self.indicator.rect.y = 384
                elif self.indicator_choose == 1:
                    self.indicator.rect.y = 484
                elif self.indicator_choose == 2:
                    self.indicator.rect.y = 584
     
    # Função auxiliar para mover o fundo até o alvo lentamente
    def move_towards_target(self, current, target, vel):
        """Move a posição atual em direção à posição alvo com a velocidade especificada."""
        if current < target:
            return min(current + vel, target)  # Move para frente até alcançar o alvo
        elif current > target:
            return max(current - vel, target)  # Move para trás até alcançar o alvo
        return current  # Retorna a posição atual se já estiver no alvo
            
    # Animando Cursor                            
    def update(self):
        """Atualiza a animação do cursor e o fundo."""
        self.indicator_animation()  # Atualiza a animação do cursor
    
        # Atualiza a animação do fundo
        return self.bg_animation()
    
    def bg_animation(self):
        """Movimenta o fundo de acordo com a lógica definida."""
        x, y = self.bg_pos  # Posições atuais do fundo
        
        # Movimentação do fundo entre as posições definidas
        if self.bg_target == (-120, 0):  # Movimento para a esquerda até x = -120
            x = self.move_towards_target(x, -120, self.bg_vel)
            if x == -120:
                self.bg_target = (-120, -130)  # Agora move para cima até y = -130
        
        elif self.bg_target == (-120, -130):  # Movimento para cima até y = -130
            y = self.move_towards_target(y, -130, self.bg_vel)
            if y == -130:
                self.bg_target = (0, -130)  # Agora move para a direita até x = 0
        
        elif self.bg_target == (0, -130):  # Movimento para a direita até x = 0
            x = self.move_towards_target(x, 0, self.bg_vel)
            if x == 0:
                self.bg_target = (0, 0)  # Agora move para baixo até y = 0
        
        elif self.bg_target == (0, 0):  # Movimento para baixo até y = 0
            y = self.move_towards_target(y, 0, self.bg_vel)
            if y == 0:
                self.bg_target = (-120, 0)  # Volta a mover para a esquerda, reiniciando o ciclo

        self.bg_pos = [x, y]  # Atualiza a posição do fundo
        self.bg.rect.topleft = self.bg_pos  # Define a nova posição do fundo
                
        return super().update()  # Chama o método update da classe pai

    def indicator_animation(self):
        """Anima o movimento do cursor."""
        self.indicator.rect.x += self.indicator_dir  # Move o cursor
        if self.indicator.rect.x > 705:  # Verifica os limites da animação
            self.indicator_dir *= -1  # Inverte a direção
        elif self.indicator.rect.x < 685:  # Verifica os limites da animação
            self.indicator_dir *= -1  # Inverte a direção

# Criando Tela de Opções
class Option(Scene):
    """Classe para a tela de opções."""
    
    def __init__(self):
        super().__init__()  # Chama o construtor da classe base
            
        # Criação de objetos de fundo e outros elementos da tela
        self.bg = Obj("assets/menu/Fundo2.png", [0, 0], [self.all_sprites], size=(1280, 720))
        self.bg_mold = Obj("assets/menu/Moldura.png", [0, 0], [self.all_sprites])
        self.title = Obj("assets/menu/Titulo.png", [50, 50], [self.all_sprites], size=(500, 210))
        self.text_options = Obj("assets/menu/Opcoes.png", [850, 65], [self.all_sprites], size=(350, 100))
 
        # Criação de textos para opções de som e tela
        self.sound_text = Text(100, "Som:", VENETIAN_RED_COLOR, [360, 320], [self.all_sprites])
        self.sound_option_text = Text(60, self.option_data["sound_text_values"], YELLOW_COLOR, [670, 360], [self.all_sprites])
        self.sound_text_values = ["Desligado", "Minimo", "Maximo"]  # Opções de som
        self.sound_text_choose = self.option_data["sound_text_choose"]  # Opção de som selecionada
                
        self.display_text = Text(100, "Tela:", VENETIAN_RED_COLOR, [360, 450], [self.all_sprites])
        self.display_option_text = Text(60, self.option_data["display_text_values"], YELLOW_COLOR, [670, 490], [self.all_sprites])
        self.display_text_values = ["Window", "Fullscreen"]  # Opções de tela
        self.display_text_choose = self.option_data["display_text_choose"]  # Opção de tela selecionada
        
        self.apply_text = Text(60, "Aplicar:", TANGO_MANGA_COLOR, [508, 580], [self.all_sprites])
        
        # Inicialização do cursor
        self.indicator = Obj("assets/menu/Cursor.png", [217, 350], [self.all_sprites], size=(110, 70))  # Imagem do cursor
        self.indicator_dir = 1  # Direção do movimento do cursor
        self.indicator_choose = 0  # Opção atualmente selecionada
        
    def indicator_set_option(self, event):
        """Define a opção selecionada com base na tecla pressionada."""
        # Alternar opções de som
        if (event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER) and self.indicator_choose == 0:
            if self.sound_text_choose < 2:
                self.sound_text_choose += 1  # Move para a próxima opção
            else:
                self.sound_text_choose = 0  # Retorna para a primeira opção
                
            self.option_data["sound_text_choose"] = self.sound_text_choose
            self.option_data["sound_text_values"] = self.sound_text_values[self.sound_text_choose]
                        
            # Atualiza o texto da opção de som
            self.sound_option_text.update_text(self.sound_text_values[self.sound_text_choose])
            
            # Ajusta a música de acordo com a seleção
            if self.sound_text_choose == 0:
                pygame.mixer.music.stop()  # Para a música
                self.option_data["music_set_volume"] = 0
            elif self.sound_text_choose == 1:
                self.option_data["music_set_volume"] = 0.05
                pygame.mixer.music.play(-1)  # Toca a música em loop
                pygame.mixer.music.set_volume(self.option_data["music_set_volume"])  # Ajusta o volume
            elif self.sound_text_choose == 2:
                self.option_data["music_set_volume"] = 0.1
                pygame.mixer.music.set_volume(0.1)  # Ajusta o volume

        # Alternar opções de tela
        elif (event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER) and self.indicator_choose == 1:
            if self.display_text_choose < 1:
                self.display_text_choose += 1  # Move para a próxima opção
            else:
                self.display_text_choose = 0  # Retorna para a primeira opção
                
            self.display_option_text.update_text(self.display_text_values[self.display_text_choose])  # Atualiza o texto da opção de tela
            
            self.option_data["display_text_choose"] = self.display_text_choose
            self.option_data["display_text_values"] = self.display_text_values[self.display_text_choose]
                       
            # Aplica as mudanças na tela
            if self.display_text_choose == 0:
                pygame.display.set_mode((BASE_WIDTH, BASE_HEIGHT), pygame.RESIZABLE)  # Modo janela
            elif self.display_text_choose == 1:
                pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # Modo tela cheia
                
        elif (event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER) and self.indicator_choose == 2:
            self.save_file("Teste.json", self.option_data)  # Salva as opções
            self.change_scene(Title())  # Retorna para a tela inicial
    
    def indicator_position(self, event):
        """Atualiza a posição do indicador com base nas teclas pressionadas."""
        if event.key == pygame.K_DOWN or event.key == pygame.K_s:
            self.sound_click.play()  # Toca o som de clique
            if self.indicator_choose <= 1:
                self.indicator_choose += 1  # Move para a próxima opção
                if self.indicator_choose == 0:
                    self.indicator.rect.x = 217
                    self.indicator.rect.y = 350
                elif self.indicator_choose == 1:
                    self.indicator.rect.x = 217
                    self.indicator.rect.y = 480
                elif self.indicator_choose == 2:
                    self.indicator.rect.x = 365
                    self.indicator.rect.y = 570
                        
        elif event.key == pygame.K_UP or event.key == pygame.K_w:
            self.sound_click.play()  # Toca o som de clique
            if self.indicator_choose > 0:
                self.indicator_choose -= 1  # Move para a opção anterior
                if self.indicator_choose == 0:
                    self.indicator.rect.x = 217
                    self.indicator.rect.y = 350
                elif self.indicator_choose == 1:
                    self.indicator.rect.x = 217
                    self.indicator.rect.y = 480
                elif self.indicator_choose == 2:
                    self.indicator.rect.x = 365
                    self.indicator.rect.y = 570
                    
    def handle_events(self, event):
        """Gerencia eventos de entrada do usuário na tela de opções."""
        if event.type == pygame.KEYDOWN or event.type == pygame.K_KP_ENTER:
            self.indicator_position(event)  # Atualiza a posição do indicador
            self.indicator_set_option(event)  # Atualiza a opção selecionada
        return super().handle_events(event)  # Chama o método handle_events da classe pai
    
    def indicator_animation(self):
        """Anima o movimento do cursor."""
        self.indicator.rect.x += self.indicator_dir  # Move o cursor
        if 207 <= self.indicator.rect.x <= 227:  # Verifica os limites da animação
            if self.indicator.rect.x >= 227 or self.indicator.rect.x <= 207:
                self.indicator_dir *= -1  # Inverte a direção
        elif 355 <= self.indicator.rect.x <= 375:  # Verifica os limites da animação
            if self.indicator.rect.x >= 375 or self.indicator.rect.x <= 355:
                self.indicator_dir *= -1  # Inverte a direção
            
    def update(self):
        """Atualiza a animação do cursor e a tela."""
        self.indicator_animation()  # Atualiza a animação do cursor
        return super().update()  # Chama o método update da classe pai
 
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
        
# Seleção de Personagem
class Char_Select(Scene):
    """Classe para a tela de seleção de personagens."""
    
    def __init__(self):
        super().__init__()  # Chama o construtor da classe base
        
        
        # Fundo e Moldura
        try:
            self.bg = Obj("assets/charSelect/Fundo2.png", [0, 0], [self.all_sprites])  # Fundo da seleção
            self.bg_mold = Obj("assets/charSelect/Moldura.png", [-28, -20], [self.all_sprites], size=(1344, 756))  # Moldura da tela
        except pygame.error as e:
            print(f"Erro ao carregar a imagem de fundo ou moldura: {e}")  # Exibe erro caso a imagem não carregue

        # Inicialização do cursor
        self.cursor_pos = [0, 0]  # Posição inicial [linha, coluna]
        self.cursor = Obj("assets/charSelect/IndChar.png", [35, 45], [self.all_sprites], size=(203, 235))  # Imagem do cursor
        self.cursor_choose = 0  # Índice do personagem selecionado
                
        # Local dos Status do Personagem
        self.plate = Obj("assets/charSelect/placa.png", [733, 353], [self.all_sprites], size=(500, 310))  # Placa para status
        
        # Estrutura de dados para armazenar informações dos personagens
        self.characters = [
            {
                "image_selected": "assets/charSelect/Indígena_M_C.png",
                "image_unselected": "assets/charSelect/Indígena_M_PB.png",
                "pose": "assets/charSelect/Pose_Indigena1.png",
                "position": [67, 82],
                "pose_position": [320, 100],
                "size_selected": (140, 178),
                "size_unselected": (125, 159),
                "pose_size": (469, 569),
                "history": "assets/charSelect/Hist_IndM.png",
                "status_image": "assets/charSelect/StatusInd.png"
            },
            {
                "image_selected": "assets/charSelect/Indígena_F_PB.png",
                "image_unselected": "assets/charSelect/Indígena_F_PB.png",
                "pose": "assets/charSelect/Pose_Indigena2.png",
                "position": [217, 82],
                "pose_position": [371, 140],
                "size_selected": (140, 178),
                "size_unselected": (125, 159),
                "pose_size": (324, 535),
                "history": "assets/charSelect/Hist_Block.png",
                "status_image": "assets/charSelect/StatusOff.png"
            },
            {
                "image_selected": "assets/charSelect/Bandeirante_M_C.png",
                "image_unselected": "assets/charSelect/Bandeirante_M_PB.png",
                "pose": "assets/charSelect/Pose_Bandeirantes1.png",
                "position": [67, 267],
                "pose_position": [325, 120],
                "size_selected": (140, 178),
                "size_unselected": (125, 159),
                "pose_size": (396, 553),
                "history": "assets/charSelect/Hist_EurM.png",
                "status_image": "assets/charSelect/StatusEur.png"
            },
            {
                "image_selected": "assets/charSelect/Bandeirante_F_PB.png",
                "image_unselected": "assets/charSelect/Bandeirante_F_PB.png",
                "pose": "assets/charSelect/Pose_Bandeirantes2.png",
                "position": [217, 267],
                "pose_position": [371, 120],
                "size_selected": (140, 178),
                "size_unselected": (125, 159),
                "pose_size": (324, 550),
                "history": "assets/charSelect/Hist_Block.png",
                "status_image": "assets/charSelect/StatusOff.png"
            },
            {
                "image_selected": "assets/charSelect/Africano_M_C.png",
                "image_unselected": "assets/charSelect/Africano_M_PB.png",
                "pose": "assets/charSelect/Pose_Africano1.png",
                "position": [67, 454],
                "pose_position": [260, 110],
                "size_selected": (140, 178),
                "size_unselected": (125, 159),
                "pose_size": (529, 567),
                "history": "assets/charSelect/Hist_AfrM.png",
                "status_image": "assets/charSelect/StatusAfr.png"
            },
            {
                "image_selected": "assets/charSelect/Africana_F_PB.png",
                "image_unselected": "assets/charSelect/Africana_F_PB.png",
                "pose": "assets/charSelect/Pose_Africano2.png",
                "position": [217, 454],
                "pose_position": [360, 85],
                "size_selected": (140, 178),
                "size_unselected": (125, 159),
                "pose_size": (342, 588),
                "history": "assets/charSelect/Hist_Block.png",
                "status_image": "assets/charSelect/StatusOff.png"
            },
        ]
        
        # Carregar a imagem do primeiro personagem ao iniciar
        self.load_character(self.cursor_choose)
        
        # Matriz de posições do cursor
        self.cursor_positions = [
            [35, 45], [180, 45],
            [35, 232], [180, 232],
            [35, 420], [180, 420]
        ]

    def load_character(self, index):
        """Carrega a imagem do personagem selecionado."""
        # Limpa os sprites antigos antes de carregar novos
        self.all_sprites.empty()

        for i, character in enumerate(self.characters):
            # Carregar a imagem destacada (selecionada) para o personagem ativo
            if i == index:
                Obj(character["image_selected"], character["position"], [self.all_sprites], size=character["size_selected"])
                
            else:
                # Carregar a imagem não destacada (não selecionada)
                Obj(character["image_unselected"], character["position"], [self.all_sprites], size=character["size_unselected"])

    def handle_events(self, event):
        """Gerencia eventos de entrada do usuário na tela de seleção de personagens."""
        if event.type == pygame.KEYDOWN:
            # Verifica se a tecla Enter foi pressionada
            if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                # Salvar o personagem selecionado
                self.option_data["selected_character"] = self.cursor_choose
                self.save_file("teste.json", self.option_data)  # Salva os dados
                
                if self.cursor_choose == 0:  # Se o primeiro personagem for selecionado
                    self.change_scene(Map())  # Muda para a cena do mapa

            # Movimento do cursor para baixo
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                if self.cursor_choose + 2 < len(self.cursor_positions):  # Permite mover até o último personagem
                    self.cursor_choose += 2  # Move para o próximo personagem na coluna
                self.cursor.rect.y = self.cursor_positions[self.cursor_choose][1]  # Atualiza a posição do cursor
                self.load_character(self.cursor_choose)  # Carrega o personagem na nova posição

            # Movimento do cursor para cima
            elif event.key == pygame.K_UP or event.key == pygame.K_w:
                if self.cursor_choose - 2 >= 0:  # Permite mover para cima se não estiver na primeira linha
                    self.cursor_choose -= 2  # Move para o personagem anterior na coluna
                self.cursor.rect.y = self.cursor_positions[self.cursor_choose][1]  # Atualiza a posição do cursor
                self.load_character(self.cursor_choose)  # Carrega o personagem na nova posição

            # Movimento do cursor para a direita
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                if self.cursor_choose % 2 == 0 and self.cursor_choose + 1 < len(self.cursor_positions):  # Limita à primeira coluna
                    self.cursor_choose += 1  # Move para a direita
                self.cursor.rect.x = self.cursor_positions[self.cursor_choose][0]  # Atualiza a posição do cursor
                self.load_character(self.cursor_choose)  # Carrega o personagem na nova posição

            # Movimento do cursor para a esquerda
            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                if self.cursor_choose % 2 == 1:  # Limita à segunda coluna
                    self.cursor_choose -= 1  # Move para a esquerda
                self.cursor.rect.x = self.cursor_positions[self.cursor_choose][0]  # Atualiza a posição do cursor
                self.load_character(self.cursor_choose)  # Carrega o personagem na nova posição
    
    def draw(self, screen):
        """Desenha a cena de seleção de personagens na tela."""
               
        # Desenhar primeiro o fundo
        self.bg.draw(screen)
        
        # Desenha todos os personagens e seus status
        super().draw(screen)  # Chama o método draw da classe pai
        self.plate.draw(screen)  # Desenha a placa na tela
        
        # Desenhar a imagem de status do personagem
        self.draw_status_image(screen, self.characters[self.cursor_choose]["status_image"])
        
        # Desenhar a imagem do histórico do personagem
        self.draw_history(screen, self.characters[self.cursor_choose]["history"])
        
        # Desenha a pose do personagem atual na frente
        current_character = self.characters[self.cursor_choose]
        pose_image = Obj(current_character["pose"], current_character["pose_position"], [self.all_sprites], size=current_character["pose_size"])
        pose_image.draw(screen)  # Desenha a pose na tela

        # Desenha o cursor na tela
        # Desenha o efeito de fade primeiro
        self.cursor.draw(screen)
        self.bg_mold.draw(screen)  # Desenha a moldura sobre o fundo
                
    def draw_history(self, screen, history_image_path):
        """Carrega e desenha a imagem do histórico do personagem na tela."""
        
        # Desenha o efeito de fade primeiro
        status_image = Obj(history_image_path, [740, 60], [self.all_sprites], size=(500, 290))  # Ajuste o tamanho conforme necessário
        status_image.draw(screen)  # Desenha a imagem de status na tela
         
    def draw_status_image(self, screen, status_image_path):
        """Carrega e desenha a imagem de status do personagem na tela."""
        # Desenha o efeito de fade primeiro
        status_image = Obj(status_image_path, [760, 380], [self.all_sprites], size=(450, 240))  # Ajuste o tamanho conforme necessário
        status_image.draw(screen)  # Desenha a imagem de status na tela


# Criando Tela de Mapa
class Map(Scene):
    """Classe para a tela do mapa."""
    
    def __init__(self):
        super().__init__()  # Chama o construtor da classe pai
        
        # Fundo e Moldura
        try:
            self.mar = Obj("assets/mapSelect/Mar.jpg", [0, 0], [self.all_sprites], size=(1280, 720))  # Imagem do mar
            self.papiro = Obj("assets/mapSelect/00Papiro.png", [0, 0], [self.all_sprites], size=(1280, 720))  # Imagem do papiro
            self.bgMap = Obj("assets/mapSelect/02Mapa_NovaPindorama_Fundo.png", [0, 0], [self.all_sprites], size=(1280, 720))  # Fundo do mapa
            self.contMap = Obj("assets/mapSelect/01Mapa_NovaPindorama_Contorno.png", [0, 0], [self.all_sprites], size=(1280, 720))  # Contorno do mapa
            self.bg_mold = Obj("assets/charSelect/Moldura.png", [-28, -20], [self.all_sprites], size=(1340, 753))  # Moldura da tela
        except pygame.error as e:
            print(f"Erro ao carregar a imagem de fundo ou moldura: {e}")  # Exibe erro caso a imagem não carregue

        # Estrutura de dados para armazenar informações das áreas
        self.areas = self.initialize_areas()  # Inicializa as áreas do mapa
                   
        # Inicialização do cursor
        self.cursor = Obj("assets/mapSelect/Cursor.png", [1070, 100], [self.all_sprites], size=(30, 48))  # Imagem do cursor
        self.cursor_choose = 0  # Índice da área selecionada
        self.completed_areas_status = [False] * len(self.areas)  # Inicializa todas as áreas como não completadas  

        # Matriz de posições do cursor
        self.cursor_positions = [area["cursor_position"] for area in self.areas]
        
        # Carrega a imagem da primeira área do mapa ao iniciar
        self.load_area(self.cursor_choose)

        # Inicializa a próxima cena como None
        self.next = None   
            
    def initialize_areas(self):
        """Inicializa as áreas do mapa com suas respectivas informações."""
        return [
            {
                "image_selected": "assets/mapSelect/00Vilarejo_Canaa.png",
                "area_completed": "assets/mapSelect/00Vilarejo_Canaa_Complete.png",
                "position": [0, 0], #(1502) - Cananéia (1070, 100)
                "cursor_position": (1070, 100)
            },
            {
                "image_selected": "assets/mapSelect/01Vila_Enseada_Rio.png",
                "area_completed": "assets/mapSelect/01Vila_Enseada_Rio_Complete.png",
                "position": [0, 0], #(1535) - Iguape (500, 130)
                "cursor_position": (500, 130)
            },
            {
                "image_selected": "assets/mapSelect/02Povoado_Cadastro.png",
                "area_completed": "assets/mapSelect/02Povoado_Cadastro_Complete.png",
                "position": [0, 0], #(1650) - Registro (650, 240)
                "cursor_position": (650, 240)
            },
            {
                "image_selected": "assets/mapSelect/03Vilarejo_Grandes_Passaros.png",
                "area_completed": "assets/mapSelect/03Vilarejo_Grandes_Passaros_Complete.png",
                "position": [0, 0], #(1750) - Pariquera-Açu (760, 180)
                "cursor_position": (760, 180)
            },
            {
                "image_selected": "assets/mapSelect/04Vale_Luz_Sombra.png",
                "area_completed": "assets/mapSelect/04Vale_Luz_Sombra_Complete.png",
                "position": [0, 0], #(1750) - Eldorado (850, 370)
                "cursor_position": (850, 370)
            },
            {
                "image_selected": "assets/mapSelect/05Freguesia_Rio_Peixes.png",
                "area_completed": "assets/mapSelect/05Freguesia_Rio_Peixes_Complete.png",
                "position": [0, 0], #(1820) - Juquiá (450, 310)
                "cursor_position": (450, 310)
            },
            {
                "image_selected": "assets/mapSelect/06Vilarejo_Praia_Pequena.png",
                "area_completed": "assets/mapSelect/06Vilarejo_Praia_Pequena_Complete.png",
                "position": [0, 0], #(1845) - Miracatu (350, 230)
                "cursor_position": (350, 230)
            },
            {
                "image_selected": "assets/mapSelect/07Vila_Passaro_Vermelho.png",
                "area_completed": "assets/mapSelect/07Vila_Passaro_Vermelho_Complete.png",
                "position": [0, 0], #(1860) - Jacupiranga (880, 200)
                "cursor_position": (880, 200)
            },
            {
                "image_selected": "assets/mapSelect/08Vilarinho_Pedras_Fluem.png",
                "area_completed": "assets/mapSelect/08Vilarinho_Pedras_Fluem_Complete.png",
                "position": [0, 0], #(1880) - Itariri (250, 100)
                "cursor_position": (250, 100)
            },
            {
                "image_selected": "assets/mapSelect/09Barragem_Arco_Iris.png",
                "area_completed": "assets/mapSelect/09Barragem_Arco_Iris_Complete.png",
                "position": [0, 0], #(1880) - Sete Barras (600, 380)
                "cursor_position": (600, 380)
            },
            {
                "image_selected": "assets/mapSelect/10Vale_Alecrins.png",
                "area_completed": "assets/mapSelect/10Vale_Alecrins_Complete.png",
                "position": [0, 0], #(1910) - Pedro de Toledo (170, 160)
                "cursor_position": (170, 160)
            },
            {
                "image_selected": "assets/mapSelect/11Bosque_Cajas.png",
                "area_completed": "assets/mapSelect/11Bosque_Cajas_Complete.png",
                "position": [0, 0], #(1960) - Cajati (960, 260)
                "cursor_position": (960, 260)
            },
        ]
        
               
    def load_area(self, index):
        """Carrega a imagem da área selecionada."""
        # Limpa os sprites antigos antes de carregar novos
        self.all_sprites.empty()

        # Carrega a imagem da área selecionada
        area = self.areas[index]
        area_image = area["image_selected"] if not self.completed_areas_status[index] else area["area_completed"]
        
        # Cria um novo objeto para a área carregada
        Obj(area_image, area["position"], [self.all_sprites])  # Cria um objeto da área no grupo de sprites

        # Atualiza a posição do cursor para a nova área
        self.update_cursor_position()

    def mark_area_as_completed(self):
        """Marca a área atual como completada."""
        self.completed_areas_status[self.cursor_choose] = True  # Atualiza o status da área atual

    def handle_events(self, event):
        """Gerencia a entrada do usuário para navegar entre as áreas."""
        super().handle_events(event)  # Chama o método da classe pai para tratar eventos
        
        if event.type == pygame.KEYDOWN:  # Verifica se uma tecla foi pressionada
            if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:  # Se a tecla pressionada for 'Enter'
                if self.cursor_choose == 0:  # Se a primeira posição estiver selecionada
                    # Verifica se a área não foi completada
                    if not self.completed_areas_status[self.cursor_choose]:  
                        selected_area = self.areas[self.cursor_choose]["image_selected"]  # Obtém a imagem da área selecionada
                        print(f"Área selecionada: {selected_area}")  # Exibe a área selecionada no console
                        self.change_scene(Level())  # Muda para a cena do nível correspondente
                    else:
                        print("Esta área já foi completada.")  # Mensagem se a área já foi completada
                else:
                    print("Esta área não pode ser selecionada.")  # Mensagem se a área não for a primeira

            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:  # Se a tecla pressionada for 'esquerda' ou 'a'
                # Lógica para mover o cursor para a esquerda
                self.cursor_choose = (self.cursor_choose - 1) % len(self.cursor_positions)  # Move para a posição anterior
                self.update_cursor_position()  # Atualiza a posição do cursor

            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:  # Se a tecla pressionada for 'direita' ou 'd'
                # Lógica para mover o cursor para a direita
                self.cursor_choose = (self.cursor_choose + 1) % len(self.cursor_positions)  # Move para a próxima posição
                self.update_cursor_position()  # Atualiza a posição do cursor

    def update_cursor_position(self):
        """Atualiza a posição do cursor com base na área selecionada."""
        cursor_x, cursor_y = self.cursor_positions[self.cursor_choose]  # Pega as coordenadas da posição atual do cursor
        self.cursor.rect.topleft = (cursor_x, cursor_y)  # Atualiza a posição do cursor na tela

    def confirm_selection(self):
        """Confirma a seleção da área atual."""
        if not self.completed_areas_status[self.cursor_choose]:  # Verifica se a área não foi completada
            selected_area = self.areas[self.cursor_choose]["image_selected"]  # Obtém a imagem da área selecionada
            print(f"Área selecionada: {selected_area}")  # Exibe a área selecionada
            self.next = Level(selected_area)  # Muda para a cena do nível correspondente
        else:
            print("Esta área já foi completada.")  # Mensagem se a área já foi completada

    def draw(self, screen):
        """Desenha a cena atual na tela."""
        self.mar.draw(screen)  # Desenha a imagem do mar
        self.papiro.draw(screen)  # Desenha a imagem do papiro
        self.bgMap.draw(screen)  # Desenha o fundo do mapa
        self.contMap.draw(screen)  # Desenha o contorno do mapa
        self.bg_mold.draw(screen)  # Desenha a moldura da tela
        super().draw(screen)  # Chama o método da classe pai para desenhar o fundo
        self.load_area(self.cursor_choose)  # Carrega a área atual
        self.cursor.draw(screen)  # Desenha o cursor na tela


# Criando Tela de Nível
class Level(Scene):
    """Classe para a tela de nível."""
    
    def __init__(self, player_data=None, hud_data=None): 
        super().__init__()  # Chama o construtor da classe base
        
        # Criação do chão
        self.ground = Ground(0, 400, 800, 20)  # x, y, largura, altura
        self.all_sprites.add(self.ground)  # Adiciona o chão ao grupo de sprites

        # Criação dos objetos na cena
        self.img_a = Obj("assets/levelSprite/level_1_1a.png", [0, 0], [self.all_sprites])  # Fundo da fase
        self.hudbk = Hud("assets/charsSprite/player/Hud/Hud_Char_Fundo.png", [25, 25], [self.all_sprites], (640, 360))
        self.img_b = Obj("assets/levelSprite/level_1_1b.png", [0, 0], [self.all_sprites])  # Fundo da fase
        
        # HUD com dados anteriores (se houver)
        self.hud = Hud("assets/charsSprite/player/Hud/Hud_Char_Contorno.png", [25, 25], [self.all_sprites], (640, 360))
        if hud_data:
            self.hud.gold = hud_data.get("gold", 0)
            self.hud.life = hud_data.get("life", 25)
            self.hud.lives = hud_data.get("lives", 3)
            self.hud.xp = hud_data.get("xp", 0)

        # Player com dados anteriores (se houver)
        if player_data:
            self.player = Player(
                image_path=player_data.get("image_path", "assets/charsSprite/player/indigenaM/R0.png"),
                position=player_data.get("position", [100, 250]),
                groups=[self.all_sprites],
                size=player_data.get("size", (200, 200)),
                life=player_data.get("life", 25),
                lives=player_data.get("lives", 3),
                xp=player_data.get("xp", 0)
            )
        else:
            self.player = Player("assets/charsSprite/player/indigenaM/R0.png", [100, 250], [self.all_sprites], (200, 200)) # O Player agora se alinha ao chão

        # Define os buracos apenas nesta fase específica
        hole_rect = pygame.Rect(520, GROUND_LEVEL-10, 100, 400)  # (x, y, largura, altura)
        self.player.set_holes([hole_rect])  # Envia os buracos para o jogador

        # Sincroniza a HUD com o Player
        self.hud.update_lives(self.player.lives)
        
        self.npc = NPC_Cacique("assets/charsSprite/npcs/Cacique/CR1.png", [1000, 285], [self.all_sprites], (200, 200)) # O NPC agora se alinha ao chão
        
        # Fonte para o ChatBox
        font = pygame.font.Font(None, 30)  # Fonte padrão
        self.chatbox = ChatBox(font, (75, 250), (800, 400))  # ChatBox na parte inferior

        # Controle de fluxo Diálogos e questões
        self.dialogue = Dialogo_1_1.falas[:5]  # Primeiro conjunto de diálogos
        self.questions = Questoes_1_1.perguntas  # Todas as questões
        self.final_dialogue = Dialogo_1_1.falas[5:]  # Últimos diálogos
        self.current_question = 0  # Índice da questão atual
        self.dialogue_stage = 0  # 0: Diálogo inicial, 1: Questões, 2: Diálogo final
        self.dialogue_finished = False  # Controle para saber se o diálogo terminou
        self.confirming_answer = False  # Indica se está no processo de confirmação
        self.selected_option = None  # Guarda a opção selecionada para confirmar
        self.exit_enabled = False  # Sinaliza quando o player pode sair para o Level_1_2
        
        #Gold e Conversão
        self.gold_reward = 0  # Quantidade de ouro por resposta correta (ajuste conforme necessário)
        self.points_to_gold_conversion = 2  # 1 ponto = 10 Gold (ajuste conforme necessário)
        
        self.questions = Questoes_1_1.perguntas[:]
        random.shuffle(self.questions)  # Embaralha as perguntas
           

    def handle_events(self, event):
        """Gerencia eventos de entrada do usuário na tela de nível."""
        self.player.events(event)

        if event.type == pygame.KEYDOWN:  # Certifique-se de que é um evento de tecla
            # Inicia o diálogo com o NPC
            if event.key == pygame.K_e and self.player.rect.colliderect(self.npc.rect) and not self.chatbox.is_active():
                if self.dialogue_stage == 0:  # Diálogo inicial
                    # Converte o diálogo para uma lista de strings no formato desejado
                    formatted_dialogue = [f"{speaker} {message}" for speaker, message in Dialogo_1_1.falas[:5]]
                    self.chatbox.display_messages(formatted_dialogue)
                    self.chatbox.active = True
                elif self.dialogue_stage == 2:  # Diálogo final
                    # Limpa qualquer dado residual das questões
                    self.chatbox.options = []  # Limpa as opções
                    self.chatbox.title = ""  # Limpa o título
                    self.chatbox.question = ""  # Limpa a pergunta

                    # Exibe o diálogo final
                    formatted_dialogue = [f"{speaker} {message}" for speaker, message in self.final_dialogue]
                    self.chatbox.display_messages(formatted_dialogue)
                    self.chatbox.active = True

            # Avança no diálogo ou responde à questão
            elif event.key == pygame.K_RETURN and self.chatbox.is_active():
                if self.chatbox.options:  # Responde à questão
                    selected_option = self.chatbox.select_option()
                    current_question = self.questions[self.current_question]
                    if selected_option == current_question["resposta_correta"]:
                        print("Resposta correta!")
                        points = current_question.get("pontos", 0)  # Obtém os pontos da questão
                        if points > 0:  # Verifica se a questão tem pontos
                            gold_reward = points * self.points_to_gold_conversion  # Converte pontos para gold
                            self.hud.update_gold(self.hud.gold + gold_reward)  # Atualiza o ouro no HUD
                            print(f"Você ganhou {gold_reward} de gold!")
                        else:
                            print("Esta questão não tem pontos definidos.")

                    else:
                        print("Resposta errada.")

                    # Avança para a próxima questão ou finaliza as perguntas
                    self.current_question += 1
                    if self.current_question < len(self.questions):
                        question_data = self.questions[self.current_question]
                        
                        # Embaralha as alternativas antes de exibi-las
                        shuffled_options = question_data["opcoes"][:]
                        random.shuffle(shuffled_options)  # Embaralha as alternativas
                        
                        self.chatbox.display_question(
                            question_data["titulo"],
                            question_data["pergunta"],  # Texto da pergunta
                            shuffled_options  # Alternativas embaralhadas
                        )
                    else:
                        # Finaliza as perguntas e ativa o diálogo final
                        self.dialogue_stage = 2  # Passa para o diálogo final
                        self.chatbox.options = []  # Limpa as opções
                        self.chatbox.title = ""  # Limpa o título
                        self.chatbox.question = ""  # Limpa a pergunta

                        formatted_dialogue = [f"{speaker} {message}" for speaker, message in self.final_dialogue]
                        self.chatbox.display_messages(formatted_dialogue)
                        self.chatbox.active = True
                else:
                    self.chatbox.next_message()

                    # Quando o diálogo inicial termina, inicia as questões
                    if self.chatbox.current_message >= len(self.chatbox.messages) and self.dialogue_stage == 0:
                        self.dialogue_stage = 1  # Avança para a etapa de questões
                        question_data = self.questions[self.current_question]
                        
                        # Embaralha as alternativas antes de exibi-las
                        shuffled_options = question_data["opcoes"][:]
                        random.shuffle(shuffled_options)  # Embaralha as alternativas
                        
                        self.chatbox.display_question(
                            question_data["titulo"],
                            question_data["pergunta"],
                            shuffled_options
                        )
                        self.chatbox.active = True
                        
                    # Verificar para Colocar o Score Ponts aqui, como Estágio 2 e retornar para o Diálogo como Estágio 3   

                    # Quando o diálogo final termina, desativa o chatbox
                    elif self.chatbox.current_message >= len(self.chatbox.messages) and self.dialogue_stage == 2:
                        self.chatbox.active = False
                        self.exit_enabled = True

            # Navegação entre opções
            elif (event.key == pygame.K_UP or event.key == pygame.K_w) and self.chatbox.options:
                self.chatbox.previous_option()
            elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and self.chatbox.options:
                self.chatbox.next_option()

            return super().handle_events(event)

    def update(self):
        """Atualiza o estado da cena, incluindo o jogador e animações."""        
        self.player.check_death()  # <- Verifica e reduz a vida se necessário
        self.hud.update_life(self.player.life)  # Atualiza os pontos de vida
        self.hud.update_lives(self.player.lives)  # Atualiza o número de vidas
        self.hud.update_xp(self.player.xp)  # Atualiza o XP (caso necessário)
        self.player.update()  # Atualiza o jogador
        self.npc.update()  # Atualiza o NPC Cacique
        super().update()  # Atualiza os outros objetos da cena
        self.all_sprites.update()
        
        # Se o jogador concluiu o diálogo e saiu pela direita, muda de fase
        if self.exit_enabled and self.player.rect.x >= 1150:
            print("[DEBUG] Transição de fase - vidas atuais:", self.player.lives)
            self.change_scene(Level_1_2(
                player_data={
                    "image_path": self.player.image_path,
                    "position": [0, 250],
                    "size": self.player.size,
                    "life": self.player.life,
                    "lives": self.player.lives,
                    "xp": self.player.xp
                },
                hud_data={
                    "gold": self.hud.gold,
                    "life": self.player.life,
                    "lives": self.player.lives,
                    "xp": self.player.xp
                }
        ))

        # Verifique se o jogador morreu e mude para a tela de Game Over
        if self.player.lives <= 0:
            self.change_scene(GameOver())  # Muda para a cena de Game Over

    def draw(self, screen):
        """Desenha a cena e o jogador na tela."""
        screen.fill((0, 0, 0))  # Limpa a tela com fundo preto
        
        # Desenha a primeira parte do fundo
        screen.blit(self.img_a.image, self.img_a.rect)

        # Desenha todos os objetos da cena, incluindo o fundo
        self.all_sprites.draw(screen)
        
        # Desenha o jogador e o NPC
        screen.blit(self.npc.image, self.npc.rect)
        screen.blit(self.player.image, self.player.rect)
        
        # Desenha a segunda parte do fundo
        screen.blit(self.img_b.image, self.img_b.rect)

        # Desenha os disparos do jogador
        for shot in self.player.shots:
            shot.draw(screen)
            
        # Desenha buracos apenas quando o chat não estiver ativo
#        if not self.chatbox.is_active():
#           for hole in self.player.holes:
#                pygame.draw.rect(screen, (255, 0, 0), hole, 2)
        
        # Desenha o Hud (Background e Contorno)
        screen.blit(self.hud.image, self.hud.rect)  # Desenho do HUD
        
        # Desenha a chatbox (se ativa)
        self.chatbox.draw(screen)
        
        pygame.display.update()  # Atualiza a tela
        
        
# Criando Tela de Nível
class Level_1_2(Level):
    """Classe para a tela de nível."""
    
    def __init__(self, player_data=None, hud_data=None): 
        super().__init__(player_data, hud_data)

        # Criação do chão
        self.ground = Ground(0, 400, 800, 20)
        self.all_sprites.add(self.ground)

        # Fundo da fase
        self.img = Obj("assets/levelSprite/level_1_2.png", [0, 0], [self.all_sprites])
        self.hudbk = Hud("assets/charsSprite/player/Hud/Hud_Char_Fundo.png", [25, 25], [self.all_sprites], (640, 360))
        
        # Criação da HUD do Boss
        self.boss_hud = BossHud("assets/charsSprite/bosses/Hud_Mapinguari.png", (0, 0), (1280, 720))

        # Criação do jogador com dados recebidos da fase anterior
        if player_data:
            self.player = Player(
                image_path=player_data.get("image_path", "assets/charsSprite/player/indigenaM/R0.png"),
                position=player_data.get("position", [100, 250]),
                groups=[self.all_sprites],
                size=player_data.get("size", (200, 200)),
                life=player_data.get("life", 25),
                lives=player_data.get("lives", 3),
                xp=player_data.get("xp", 0)
            )
        else:
            self.player = Player("assets/charsSprite/player/indigenaM/R0.png", [100, 250], [self.all_sprites], (200, 200))

        # Criação da HUD (sem valores ainda)
        self.hud = Hud("assets/charsSprite/player/Hud/Hud_Char_Contorno.png", [25, 25], [self.all_sprites], (640, 360))
        
        # Atualiza a HUD com os dados recebidos da fase anterior (se houver)
        self.hud.life = self.player.life
        self.hud.lives = self.player.lives
        self.hud.xp = self.player.xp
        if hud_data:
            self.hud.gold = hud_data.get("gold", 0)

        print("[DEBUG] Player.lives ao entrar:", self.player.lives)
        print("[DEBUG] HUD.lives após update:", self.hud.lives)

        # Boss
        self.boss = Boss_Mapinguari([850, 100], [self.all_sprites], size=(400, 400))

        # Fonte e chatbox
        #font = pygame.font.Font(None, 30)
        self.chatbox = None
        # Forçar para valor que nunca entra no diálogo
        self.dialogue_stage = -1
        
        self.boss_name_font = pygame.font.Font("assets/font/Primitive.ttf", 28)  # Tamanho da fonte: 40
        self.boss_name_text = self.boss_name_font.render("Mapinguari", True, (0, 0, 0))  # Branco
        self.boss_name_pos = (880, 580)  # Posição no canto superior direito (ajuste conforme a tela)

        # Controle de diálogo e questões
        self.dialogue = Dialogo_1_1.falas[:5]
        self.questions = Questoes_1_1.perguntas
        self.final_dialogue = Dialogo_1_1.falas[5:]
        self.current_question = 0
        self.dialogue_stage = 0
        self.dialogue_finished = False
        self.confirming_answer = False
        self.selected_option = None
        self.exit_enabled = False

        self.gold_reward = 0
        self.points_to_gold_conversion = 2

        self.questions = Questoes_1_1.perguntas[:]
        random.shuffle(self.questions)
           

    def handle_events(self, event):
        """Gerencia eventos de entrada do usuário na tela de nível."""
        self.player.events(event)

        if event.type == pygame.KEYDOWN:  # Certifique-se de que é um evento de tecla
            # Inicia o diálogo com o NPC
            if event.key == pygame.K_e and self.player.rect.colliderect(self.boss.rect) and not self.chatbox.is_active():
                if self.dialogue_stage == 0:  # Diálogo inicial
                    # Converte o diálogo para uma lista de strings no formato desejado
                    formatted_dialogue = [f"{speaker} {message}" for speaker, message in Dialogo_1_1.falas[:5]]
                    self.chatbox.display_messages(formatted_dialogue)
                    self.chatbox.active = True
                elif self.dialogue_stage == 2:  # Diálogo final
                    # Limpa qualquer dado residual das questões
                    self.chatbox.options = []  # Limpa as opções
                    self.chatbox.title = ""  # Limpa o título
                    self.chatbox.question = ""  # Limpa a pergunta

                    # Exibe o diálogo final
                    formatted_dialogue = [f"{speaker} {message}" for speaker, message in self.final_dialogue]
                    self.chatbox.display_messages(formatted_dialogue)
                    self.chatbox.active = True

            # Avança no diálogo ou responde à questão
            elif event.key == pygame.K_RETURN and self.chatbox.is_active():
                if self.chatbox.options:  # Responde à questão
                    selected_option = self.chatbox.select_option()
                    current_question = self.questions[self.current_question]
                    if selected_option == current_question["resposta_correta"]:
                        print("Resposta correta!")
                        points = current_question.get("pontos", 0)  # Obtém os pontos da questão
                        if points > 0:  # Verifica se a questão tem pontos
                            gold_reward = points * self.points_to_gold_conversion  # Converte pontos para gold
                            self.hud.update_gold(self.hud.gold + gold_reward)  # Atualiza o ouro no HUD
                            print(f"Você ganhou {gold_reward} de gold!")
                        else:
                            print("Esta questão não tem pontos definidos.")

                    else:
                        print("Resposta errada.")
                    # Avança para a próxima questão ou finaliza as perguntas
                    self.current_question += 1
                    if self.current_question < len(self.questions):
                        question_data = self.questions[self.current_question]
                        
                        # Embaralha as alternativas antes de exibi-las
                        shuffled_options = question_data["opcoes"][:]
                        random.shuffle(shuffled_options)  # Embaralha as alternativas
                        
                        self.chatbox.display_question(
                            question_data["titulo"],
                            question_data["pergunta"],  # Texto da pergunta
                            shuffled_options  # Alternativas embaralhadas
                        )
                    else:
                       # Finaliza as perguntas e ativa o diálogo final
                        self.dialogue_stage = 2  # Passa para o diálogo final
                        self.chatbox.options = []  # Limpa as opções
                        self.chatbox.title = ""  # Limpa o título
                        self.chatbox.question = ""  # Limpa a pergunta

                        formatted_dialogue = [f"{speaker} {message}" for speaker, message in self.final_dialogue]
                        self.chatbox.display_messages(formatted_dialogue)
                        self.chatbox.active = True
                else:
                    self.chatbox.next_message()

                    # Quando o diálogo inicial termina, inicia as questões
                    if self.chatbox.current_message >= len(self.chatbox.messages) and self.dialogue_stage == 0:
                        self.dialogue_stage = 1  # Avança para a etapa de questões
                        question_data = self.questions[self.current_question]
                        
                        # Embaralha as alternativas antes de exibi-las
                        shuffled_options = question_data["opcoes"][:]
                        random.shuffle(shuffled_options)  # Embaralha as alternativas
                        
                        self.chatbox.display_question(
                            question_data["titulo"],
                            question_data["pergunta"],
                            shuffled_options
                        )
                        self.chatbox.active = True
                        
                    # Verificar para Colocar o Score Ponts aqui, como Estágio 2 e retornar para o Diálogo como Estágio 3   

                    # Quando o diálogo final termina, desativa o chatbox
                    elif self.chatbox.current_message >= len(self.chatbox.messages) and self.dialogue_stage == 2:
                        self.chatbox.active = False
                        self.exit_enabled = True  # Libera a saída do jogador após o diálogo final

            # Navegação entre opções
            elif (event.key == pygame.K_UP or event.key == pygame.K_w) and self.chatbox.options:
                self.chatbox.previous_option()
            elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and self.chatbox.options:
                self.chatbox.next_option()

            return super().handle_events(event)

    def update(self):
        """Atualiza o estado da cena, incluindo o jogador e animações."""        
        # Atualiza os dados do HUD com base no estado atual do jogador
        self.hud.update_life(self.player.life)
        self.hud.update_lives(self.player.lives)
        self.hud.update_xp(self.player.xp)

        # Atualiza os sprites do jogador e do NPC
        self.player.update()
        self.boss.update()

        # Atualiza todos os outros sprites
        super().update()
        self.all_sprites.update()

        # Quando o diálogo final tiver sido concluído e o jogador andar até a borda da tela...
        if self.exit_enabled and self.player.rect.x >= 1150:
            # Troca para a mesma fase (ou próxima), passando os dados atualizados
            self.change_scene(Level_1_2(
                player_data={
                    "image_path": self.player.image_path,
                    "position": [0, 250],  # Reinicia no início da nova fase
                    "groups": [self.all_sprites],
                    "size": self.player.size,
                    "life": self.player.life,
                    "lives": self.player.lives,
                    "xp": self.player.xp
                },
                hud_data={
                    "gold": self.hud.gold,
                    "life": self.player.life,
                    "lives": self.player.lives,
                    "xp": self.player.xp
                }
            ))

        # Se o jogador ficar sem vidas, muda para a tela de Game Over
        if self.player.lives <= 0:
            self.change_scene(GameOver())

    def draw(self, screen):
        """Desenha a cena e o jogador na tela."""
        screen.fill((0, 0, 0))  # Limpa a tela com fundo preto

        # Desenha todos os objetos da cena, incluindo o fundo
        self.all_sprites.draw(screen)
        
        # Desenha o jogador e o NPC
        
        screen.blit(self.player.image, self.player.rect)

        # Desenha os disparos do jogador
        for shot in self.player.shots:
            shot.draw(screen)
        
        # Desativado: não usa chatbox no momento
        # if self.chatbox and self.chatbox.is_active():
        #     self.chatbox.draw(screen)

        
        # Desenha o Hud (Background e Contorno)
        screen.blit(self.hud.image, self.hud.rect)  # Desenho do HUD
        
        # Desenha o HUD do Boss (Mapinguari)
        screen.blit(self.boss_hud.image, self.boss_hud.rect)
        
        # Escreve o nome do Boss na tela
        screen.blit(self.boss_name_text, self.boss_name_pos)
        
        pygame.display.update()  # Atualiza a tela
           
               
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
    
    def draw(self, surface):
        """Desenha a tela de Game Over."""
        self.img.draw(surface)
    

