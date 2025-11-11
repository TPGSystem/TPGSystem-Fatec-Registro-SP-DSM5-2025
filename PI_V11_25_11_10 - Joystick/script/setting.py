import os
import pygame

# --- Inicialização mínima segura ---
# Atenção: pygame.init() deve ser chamado no main antes de usar fontes/som.
pygame.font.init()

# =========================
# TELA / RESOLUÇÃO / FPS
# =========================
BASE_WIDTH  = 1280
BASE_HEIGHT = 720
VIRTUAL_SIZE = (BASE_WIDTH, BASE_HEIGHT)
ASPECT_RATIO = BASE_WIDTH / BASE_HEIGHT

FPS = 60

# =========================
# CAMINHOS / ASSETS
# =========================
ASSETS_DIR = "assets"
FONT_DIR   = os.path.join(ASSETS_DIR, "font")
IMG_DIR    = os.path.join(ASSETS_DIR, "menu")

FONT_PATH_PRIMARY = os.path.join(FONT_DIR, "Primitive.ttf")
ICON_PATH         = os.path.join(IMG_DIR, "Icon.png")


# =========================
# ALTURA DAS LINHAS NO CHATBOX
# =========================
LINE_H_OPT = 24        # altura de linha das alternativas (era 30)
GAP_BETWEEN_OPT = 8    # espaço entre alternativas (era 15)
TOP_GAP_OPT = 16       # respiro entre pergunta e o bloco de alternativas (era 25)

# =========================
# CORES (pygame.Color)
# =========================
BLACK            = pygame.Color(0, 0, 0)
WHITE            = pygame.Color(255, 255, 255)
BLUE             = pygame.Color(0, 0, 255)
SKY_BLUE         = pygame.Color(78, 196, 245)
LIGHT_SKY_BLUE   = pygame.Color(135, 206, 250)
WATER_GREEN      = pygame.Color(20, 252, 182)
GRAY             = pygame.Color(200, 200, 200)
YELLOW           = pygame.Color(245, 236, 79)
RED              = pygame.Color(255, 0, 0)
CARMINE          = pygame.Color(245, 78, 109)
PURPLE           = pygame.Color(100, 10, 166)
ORANGE           = pygame.Color(255, 136, 0)
VENETIAN_RED     = pygame.Color(198, 5, 5)
TANGO_MANGA      = pygame.Color(227, 119, 5)
DEEP_MAGENTA     = pygame.Color(222, 5, 199)

# Mantém compatibilidade com nomes antigos, se usados no projeto:
BLACK_COLOR = BLACK
WHITE_COLOR = WHITE
BLUE_COLOR = BLUE
LIGHT_SKY_BLUE_COLOR = LIGHT_SKY_BLUE
GRAY_COLOR = GRAY
YELLOW_COLOR = YELLOW
RED_COLOR = RED
PURPLE_COLOR = PURPLE
ORANGE_COLOR = ORANGE
VENETIAN_RED_COLOR = VENETIAN_RED
TANGO_MANGA_COLOR = TANGO_MANGA
DEEP_MAGENTA_COLOR = DEEP_MAGENTA

# =========================
# MUNDO / FÍSICA / NÍVEIS
# =========================
# GROUND_LEVEL relativo à altura base (ex.: 485 em 720 equivale ~67.36% da altura)
GROUND_LEVEL = int(BASE_HEIGHT * (485 / 720))

# Gravidade e velocidades padrão (ajuste conforme necessidade)
GRAVITY        = 2000.0   # px/s^2
JUMP_VELOCITY  = -900.0   # px/s  (valor negativo = para cima)
WALK_SPEED     = 240.0    # px/s
RUN_SPEED      = 360.0    # px/s
AIR_CONTROL    = 0.6      # fator [0..1]

# =========================
# TIPOGRAFIA (lazy + fallback)
# =========================
# Para evitar quebra caso a fonte não exista ou pygame.font não esteja pronto,
# use get_font(size) e cache interno.
__font_cache = {}

def _resolve_font_path():
    """Retorna um caminho de fonte válido (custom ou default)."""
    if os.path.isfile(FONT_PATH_PRIMARY):
        return FONT_PATH_PRIMARY
    # Fallback para fonte padrão do pygame
    default_name = pygame.font.get_default_font()
    return default_name

def get_font(size: int, bold: bool = False, italic: bool = False) -> pygame.font.Font:
    """
    Obtém uma fonte com cache. Garante fallback se a fonte custom não existir.
    Use: font = get_font(24)
    """
    key = (size, bold, italic)
    if key in __font_cache:
        return __font_cache[key]

    try:
        font_path = _resolve_font_path()
        font = pygame.font.Font(font_path, size)
        font.set_bold(bold)
        font.set_italic(italic)
    except Exception as e:
        print(f"[WARN] Falha ao carregar fonte ({e}). Usando fallback padrão.")
        font = pygame.font.SysFont(None, size, bold=bold, italic=italic)

    __font_cache[key] = font
    return font

# Compatibilidade com constantes antigas (se o projeto já referencia FONT_BIG/SMALL)
# Observação: são criadas tardiamente; se preferir, use get_font() diretamente nas cenas.
try:
    FONT_BIG   = get_font(36)
    FONT_SMALL = get_font(24)
except Exception:
    # Em casos raros (ex.: import antes de init), os getters voltarão a funcionar depois.
    FONT_BIG = None
    FONT_SMALL = None

# =========================
# INPUT / MAPEAMENTO (opcional)
# =========================
# Centralize chaves de input aqui se quiser padronizar controles entre cenas.
KEY_TOGGLE_FULLSCREEN = pygame.K_F11
