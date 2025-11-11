import pygame, random
from ..base import Scene
from script.core.obj import Obj
from script.setting import *
from ..map.map_scene import Map


class Char_Select(Scene):
    """Classe para a tela de seleção de personagens."""
    
    def __init__(self):
        super().__init__()  # Chama o construtor da classe base
        
        # Fundo e Moldura
        try:
            self.bg = Obj("assets/charSelect/Fundo2.png", [0, 0], [self.all_sprites])  # Fundo da seleção
            self.bg_mold = Obj("assets/charSelect/Moldura_V3.png", [0, 0], [self.all_sprites], size=(1280, 720))  # Moldura da tela
        except pygame.error as e:
            print(f"Erro ao carregar a imagem de fundo ou moldura: {e}")

        # Cursor
        self.cursor_pos = [0, 0]  # Posição inicial [linha, coluna]
        self.cursor = Obj("assets/charSelect/IndChar.png", [21, 14], [self.all_sprites], size=(192, 247)) # Imagem do cursor
        self.cursor_choose = 0 # Índice do personagem selecionado
        
        # (Opcional) Placa antiga — se quiser usar, descomente
        # self.plate = Obj("assets/charSelect/placa.png", [733, 353], [self.all_sprites], size=(500, 310))
        
        # Estrutura de dados para personagens (novo formato)
        self.characters = [
            # NOVO FORMATO (exemplo)
            {
                "image_selected": "assets/charSelect/IM_C.png",
                "position_img_sel": [48, 45],
                "size_position_img_sel": (138, 193),

                "image_unselected": "assets/charSelect/IM_PB.png",
                "position_img_unsel": [57, 57],
                "size_position_img_unsel": (120, 169),

                "pose": "assets/charSelect/IM_P.png",
                "position_pose": [251, 102],
                "size_pose": (550, 550),

                "description": "assets/charSelect/IM_D.png",
                "position_desc": [660, 18],
                "size_desc": (600, 372),

                "status": "assets/charSelect/IM_S.png",
                "position_status": [694, 381],
                "size_status": (550, 300)
            },
            {
                "image_selected": "assets/charSelect/IF_C.png",
                "position_img_sel": [190, 45],
                "size_position_img_sel": (138, 193),

                "image_unselected": "assets/charSelect/IF_PB.png",
                "position_img_unsel": [199, 57],
                "size_position_img_unsel": (120, 169),

                "pose": "assets/charSelect/IF_P.png",
                "position_pose": [251, 102],
                "size_pose": (550, 550),

                "description": "assets/charSelect/IF_D.png",
                "position_desc": [660, 18],
                "size_desc": (600, 372),

                "status": "assets/charSelect/IF_S.png",
                "position_status": [694, 381],
                "size_status": (550, 300)
            },
            {
                "image_selected": "assets/charSelect/EM_C.png",
                "position_img_sel": [48, 268],
                "size_position_img_sel": (138, 193),

                "image_unselected": "assets/charSelect/EM_PB.png",
                "position_img_unsel": [57, 280],
                "size_position_img_unsel": (120, 169),

                "pose": "assets/charSelect/EM_P.png",
                "position_pose": [251, 102],
                "size_pose": (550, 550),

                "description": "assets/charSelect/EM_D.png",
                "position_desc": [660, 18],
                "size_desc": (600, 372),

                "status": "assets/charSelect/EM_S.png",
                "position_status": [694, 381],
                "size_status": (550, 300)
            },
            {
                "image_selected": "assets/charSelect/EF_C.png",
                "position_img_sel": [190, 268],
                "size_position_img_sel": (138, 193),

                "image_unselected": "assets/charSelect/EF_PB.png",
                "position_img_unsel": [199, 280],
                "size_position_img_unsel": (120, 169),

                "pose": "assets/charSelect/EF_P.png",
                "position_pose": [251, 102],
                "size_pose": (550, 550),

                "description": "assets/charSelect/EF_D.png",
                "position_desc": [660, 18],
                "size_desc": (600, 372),

                "status": "assets/charSelect/EF_S.png",
                "position_status": [694, 381],
                "size_status": (550, 300)
            },
            {
                "image_selected": "assets/charSelect/AM_C.png",
                "position_img_sel": [48, 487],
                "size_position_img_sel": (138, 193),

                "image_unselected": "assets/charSelect/AM_PB.png",
                "position_img_unsel": [57, 499],
                "size_position_img_unsel": (120, 169),

                "pose": "assets/charSelect/AM_P.png",
                "position_pose": [203, 102],
                "size_pose": (550, 550),

                "description": "assets/charSelect/AM_D.png",
                "position_desc": [660, 18],
                "size_desc": (600, 372),

                "status": "assets/charSelect/AM_S.png",
                "position_status": [694, 381],
                "size_status": (550, 300)
            },
            {
                "image_selected": "assets/charSelect/AF_C.png",
                "position_img_sel": [190, 487],
                "size_position_img_sel": (138, 193),

                "image_unselected": "assets/charSelect/AF_PB.png",
                "position_img_unsel": [199, 499],
                "size_position_img_unsel": (120, 169),

                "pose": "assets/charSelect/AF_P.png",
                "position_pose": [251, 102],
                "size_pose": (550, 550),

                "description": "assets/charSelect/AF_D.png",
                "position_desc": [660, 18],
                "size_desc": (600, 372),

                "status": "assets/charSelect/AF_S.png",
                "position_status": [694, 381],
                "size_status": (550, 300)
            },
        ]

        # Grupo separado só para as miniaturas (evita apagar fundo/moldura/cursor)
        self.thumb_sprites = pygame.sprite.Group()

        # Carregar a imagem do primeiro personagem ao iniciar
        self.load_character(self.cursor_choose)
        
        # Matriz de posições do cursor (mantive a navegação 2x3 que você já usa)
        self.cursor_positions = [
            [21, 14], [163, 14],
            [21, 235], [163, 235],
            [21, 455], [163, 455]
        ]

    # -------------------- Helpers de compatibilidade --------------------
    def _thumb_fields(self, character, selected):
        """Retorna (img_path, pos, size) para a miniatura, compatível com os dois formatos."""
        if selected:
            # novo formato
            path = character.get("image_selected")
            pos  = character.get("position_img_sel")
            size = character.get("size_position_img_sel")
            # fallback antigo
            if pos is None:
                pos = character.get("position")
            if size is None:
                size = character.get("size_selected")
        else:
            path = character.get("image_unselected")
            pos  = character.get("position_img_unsel")
            size = character.get("size_position_img_unsel")
            if pos is None:
                pos = character.get("position")
            if size is None:
                size = character.get("size_unselected")
        return path, pos, size

    def _pose_fields(self, character):
        """Retorna (img_path, pos, size) da pose, compatível com os dois formatos."""
        path = character.get("pose")
        pos  = character.get("position_pose", character.get("pose_position"))
        size = character.get("size_pose", character.get("pose_size"))
        return path, pos, size

    def _desc_fields(self, character):
        """Retorna (img_path, pos, size) da descrição/histórico, compatível com os dois formatos."""
        path = character.get("description", character.get("history"))
        # padrão antigo usava [740, 60] e (500, 290) no seu draw_history
        pos  = character.get("position_desc", [740, 60])
        size = character.get("size_desc", (500, 290))
        return path, pos, size

    def _status_fields(self, character):
        """Retorna (img_path, pos, size) do status/placa de status, compatível com os dois formatos."""
        path = character.get("status", character.get("status_image"))
        # no seu draw_status_image: [760,380], (450,240)
        pos  = character.get("position_status", [760, 380])
        size = character.get("size_status", (450, 240))
        return path, pos, size

    # -------------------- Carregar sprites de miniaturas --------------------
    def load_character(self, index):
        """Recria APENAS as miniaturas conforme o personagem selecionado, mantendo fundo/moldura/cursor."""
        # limpa somente as thumbs
        for spr in list(self.thumb_sprites):
            spr.kill()
        self.thumb_sprites.empty()

        # recria thumbs (selecionada e não selecionadas)
        for i, character in enumerate(self.characters):
            # Carregar a imagem destacada (selecionada) para o personagem ativo
            selected = (i == index)
            img_path, pos, size = self._thumb_fields(character, selected)
            if not img_path or not pos or not size:
                continue
            Obj(img_path, pos, [self.thumb_sprites], size=size)

    # -------------------- Eventos --------------------
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
    
    # -------------------- Draw --------------------
    def draw(self, screen):
        """Desenha a cena de seleção de personagens na tela."""
        # 1) Fundo
        self.bg.draw(screen)

        # 2) Miniaturas
        self.thumb_sprites.draw(screen)

        # 3) Descrição
        current = self.characters[self.cursor_choose]
        desc_path, desc_pos, desc_size = self._desc_fields(current)
        if desc_path and desc_pos and desc_size:
            Obj(desc_path, desc_pos, [self.all_sprites], size=desc_size).draw(screen)

        # 4) Status
        status_path, status_pos, status_size = self._status_fields(current)
        if status_path and status_pos and status_size:
            Obj(status_path, status_pos, [self.all_sprites], size=status_size).draw(screen)

        # 5) Cursor
        self.cursor.draw(screen)

        # 6) Moldura
        self.bg_mold.draw(screen)

        # 7) **POSE POR ÚLTIMO** (fica acima de tudo)
        pose_path, pose_pos, pose_size = self._pose_fields(current)
        if pose_path and pose_pos and pose_size:
            Obj(pose_path, pose_pos, [self.all_sprites], size=pose_size).draw(screen)

        pygame.display.update()