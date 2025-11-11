import pygame
from ..base import Scene
from script.core.obj import Obj
from script.setting import *
from ..menus.title import Title


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