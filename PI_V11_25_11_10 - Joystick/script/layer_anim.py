# layer_anim.py
import pygame
from typing import Dict, Optional, Tuple

# ==============================================================
#  CAMADAS DE CENÁRIO (LAYER SYSTEM)
#  --------------------------------------------------------------
#  Este módulo provê um mini-sistema de camadas para cenários:
#    • BaseLayer: interface/contrato para camadas.
#    • StaticLayer: imagem estática (céu, montanha, chão fixo, etc.).
#    • FlipLayer: animação de 2 quadros (A/B) com base em FPS + dt.
#    • LayerStack: gerenciador de camadas (update/desenho ordenado).
#
#  ► Integração típica em Level(Scene):
#      self.layers = LayerStack()
#      self.layers.add("ceu", StaticLayer("assets/bg/sky.png", z=0, plane="back"))
#      self.layers.add("ondas", FlipLayer("onda1.png","onda2.png", fps=8, z=10, plane="back"))
#      ...
#      def update(self, dt): self.layers.update(dt)
#      def draw(self, screen):
#          self.layers.draw_back(screen)   # atrás do player
#          self.player.draw(screen)        # player
#          self.layers.draw_front(screen)  # frente do player
#
#  ► Sobre z/plane:
#      - plane controla se a camada aparece "atrás" (back) ou "na frente" (front) do player.
#      - z controla a profundidade dentro de cada plano (menor z = mais ao fundo).
#
#  ► Desempenho:
#      - Imagens são carregadas via pygame.image.load(...).convert_alpha().
#        Evite recriar layers a cada frame; crie-os uma vez e apenas atualize/draw.
#      - Use scale com parcimônia; preferir imagens já no tamanho final.
#      - FlipLayer depende de dt (segundos) para alternar A/B de forma estável em diferentes FPS.
#
# ==============================================================


# --------------------------------------------------------------
# 🔹 CLASSE BASE: serve de modelo para qualquer tipo de layer.
# --------------------------------------------------------------
class BaseLayer:
    def __init__(self, z: int, plane: str = "back",
                 pos: Tuple[int, int] = (0, 0),
                 alpha: Optional[int] = None):
        """
        Parâmetros:
          z     : Ordem de desenho dentro do mesmo 'plane'. Menor z desenha primeiro.
          plane : "back" (atrás do player) ou "front" (na frente do player).
          pos   : Posição (x, y) de desenho (sem offset/câmera).
          alpha : Transparência opcional [0..255]; None mantém alpha original do PNG.

        Observações:
          • 'visible' permite ligar/desligar a camada sem removê-la do stack.
          • Esta classe expõe 'update(dt)' e 'draw(surface)' para ser implementada
            ou sobrescrita em classes derivadas.
        """
        assert plane in ("back", "front")
        self.z = z
        self.plane = plane
        self.pos = list(pos)
        self.alpha = alpha
        self.visible = True  # pode desligar um layer sem removê-lo

    # Essas funções são sobrescritas nas classes filhas
    def update(self, dt: float): ...
    def draw(self, surface: pygame.Surface): ...


# --------------------------------------------------------------
# 🔹 CAMADA ESTÁTICA: exibe uma imagem fixa (sem animação)
# --------------------------------------------------------------
class StaticLayer(BaseLayer):
    """
    Representa uma camada estática (sem troca de frames).
    Exemplos: céu, montanhas, chão pintado, elementos do cenário sem animação.

    Boas práticas:
      • Use imagens já no tamanho correto para evitar custo de resize em tempo de execução.
      • Se precisar reaproveitar a mesma textura em múltiplos layers, considere um cache global.
    """
    def __init__(self, image_path: str, z: int,
                 plane: str = "back", pos=(0, 0),
                 alpha: Optional[int] = None,
                 scale: Optional[Tuple[int, int]] = None):
        super().__init__(z, plane, pos, alpha)

        # Carrega a imagem do disco; convert_alpha otimiza composição com transparência
        img = pygame.image.load(image_path).convert_alpha()

        # Redimensiona, se necessário (custo único na criação do layer)
        if scale:
            img = pygame.transform.smoothscale(img, scale)

        # Define transparência (opcional). Mantém o alpha original do PNG se None.
        if alpha is not None:
            img.set_alpha(alpha)

        # Guarda a imagem pronta para desenhar
        self.image = img

    def draw(self, surface: pygame.Surface):
        """Desenha a imagem, se estiver visível. Não aplica offset/câmera por padrão."""
        if self.visible:
            surface.blit(self.image, self.pos)


# --------------------------------------------------------------
# 🔹 CAMADA ANIMADA (FlipLayer)
# --------------------------------------------------------------
class FlipLayer(BaseLayer):
    """
    Camada que alterna entre duas imagens (frame A e frame B).
    Útil para micro-animações baratas: ondas do mar, queda d'água, folhas tremulando, tochas, etc.

    Funcionamento:
      • 'fps' define quantas trocas por segundo ocorrem (A↔B).
      • 'update(dt)' acumula tempo e alterna o índice do frame quando frame_time é atingido.
      • Mantém 'alpha' opcional aplicado aos dois frames.

    Notas:
      • Se precisar de >2 frames, crie uma classe animada dedicada ou generalize para uma lista de frames.
      • Se fps for 0, a animação pausa (permite "congelar" a camada).
    """
    def __init__(self, img_a: str, img_b: str, fps: float, z: int,
                 plane: str = "back", pos=(0, 0),
                 alpha: Optional[int] = None,
                 scale: Optional[Tuple[int, int]] = None,
                 start_on_b: bool = False):
        """
        img_a / img_b : caminhos das imagens que vão intercalar.
        fps           : trocas por segundo (ex.: 8 -> troca a cada 0,125s).
        start_on_b    : se True, inicia exibindo o segundo frame (B).
        Demais params : herdados de BaseLayer (z, plane, pos, alpha) + scale opcional.
        """
        super().__init__(z, plane, pos, alpha)

        # Carrega e prepara as duas imagens
        a = pygame.image.load(img_a).convert_alpha()
        b = pygame.image.load(img_b).convert_alpha()
        if scale:
            a = pygame.transform.smoothscale(a, scale)
            b = pygame.transform.smoothscale(b, scale)
        if alpha is not None:
            a.set_alpha(alpha)
            b.set_alpha(alpha)

        # Guarda os dois frames
        self.frames = [a, b]

        # Define a velocidade da animação
        self.fps = max(0.0, fps)  # clamp mínimo a 0
        self._time = 0.0          # tempo acumulado desde a última troca
        self._index = 1 if start_on_b else 0  # começa com o frame A (0) ou B (1)

    # --- métodos de controle ---
    def set_images(self, img_a: str, img_b: str, keep_phase: bool = True):
        """
        Troca as imagens A e B em tempo de execução (ex.: mudar para versão noturna).
        keep_phase=True mantém o quadro atual (não reseta a animação).
        Observação: reaplica o alpha atual do layer às novas imagens.
        """
        idx = self._index
        a = pygame.image.load(img_a).convert_alpha()
        b = pygame.image.load(img_b).convert_alpha()
        if self.alpha is not None:
            a.set_alpha(self.alpha)
            b.set_alpha(self.alpha)
        self.frames = [a, b]

        if not keep_phase:
            # reinicia a animação (volta para A e zera o tempo acumulado)
            self._index = 0
            self._time = 0.0
        else:
            # mantém o mesmo quadro atual
            self._index = idx

    def set_fps(self, fps: float):
        """Altera a velocidade da animação (0 pausa a troca de frames)."""
        self.fps = max(0.0, fps)

    def update(self, dt: float):
        """
        Atualiza o relógio interno e alterna entre as imagens
        com base no 'fps' (trocas por segundo).

        Parâmetros:
          dt : delta time em segundos (ex.: 1/60 ≈ 0.0167), vindo do loop principal.
        """
        if not self.visible or self.fps <= 0:
            return

        # Soma o tempo desde o último update e calcula o tempo por quadro
        self._time += dt
        frame_time = 1.0 / self.fps  # tempo por quadro até alternar A/B

        # Alterna entre A e B enquanto houver tempo acumulado suficiente
        while self._time >= frame_time:
            self._time -= frame_time
            self._index ^= 1  # troca 0 ↔ 1 (bitwise XOR)

    def draw(self, surface: pygame.Surface):
        """Desenha o frame atual na tela, respeitando 'visible' e a posição base."""
        if self.visible:
            surface.blit(self.frames[self._index], self.pos)


# --------------------------------------------------------------
# 🔹 LAYERSTACK — Gerencia todas as camadas do cenário
# --------------------------------------------------------------
class LayerStack:
    """
    O LayerStack é o gerenciador principal das camadas:
      - Registra layers por nome (strings únicas).
      - Atualiza todas as camadas (para animar FlipLayers via dt).
      - Desenha na ordem correta por plano ("back" e "front") e por z.

    Convenções:
      • Use nomes sem espaço para identificar camadas ("ceu", "montanha_1", "ondas").
      • 'add()' retorna o próprio layer, permitindo encadear ou ajustar propriedades.
    """
    def __init__(self):
        # Dicionário que armazena os layers por nome (nome -> BaseLayer)
        self._layers: Dict[str, BaseLayer] = {}

    def add(self, name: str, layer: BaseLayer):
        """Adiciona um novo layer ao stack e o identifica por nome (substitui se já existir)."""
        self._layers[name] = layer
        return layer  # retorna o próprio objeto para uso direto se quiser

    def get(self, name: str) -> Optional[BaseLayer]:
        """Retorna o layer pelo nome (útil para alterar propriedades depois)."""
        return self._layers.get(name)

    def update(self, dt: float):
        """
        Atualiza todas as camadas do stack.
        Importante: chame a partir do loop de cena com o mesmo dt usado no jogo.
        """
        for ly in self._layers.values():
            ly.update(dt)

    def draw_back(self, surface: pygame.Surface):
        """
        Desenha apenas as camadas que estão atrás do player (plane='back').
        Ordena por z (ascendente) para manter a profundidade correta.
        """
        for ly in sorted(
            (l for l in self._layers.values() if l.plane == "back"),
            key=lambda L: L.z
        ):
            ly.draw(surface)

    def draw_front(self, surface: pygame.Surface):
        """
        Desenha apenas as camadas da frente (plane='front'), também ordenadas por z.
        Útil para HUD de cenário, neblina frontal, vinhetas, partículas em 1º plano etc.
        """
        for ly in sorted(
            (l for l in self._layers.values() if l.plane == "front"),
            key=lambda L: L.z
        ):
            ly.draw(surface)
