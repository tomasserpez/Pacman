from pygame.math import Vector2 as vec
#Configuraciónes de pantalla
TOP_BOTTOM_BUFFER = 50
WIDTH, HEIGHT = 610, 670
MAZE_WIDTH, MAZE_HEIGHT = WIDTH-TOP_BOTTOM_BUFFER, HEIGHT-TOP_BOTTOM_BUFFER
FPS = 60

ROWS = 30
COLS = 28

# Configuración de color
BLACK = (0,0,0)
RED = (208,22,22)
GREY = (170, 107, 107)
WHITE = (255,255,255)
PLAYER_COLOR = (190,194,15)

# Configuración de fuente
START_TEXT_SIZE = 16
START_FONT = 'arial black'

# # Configuración del jugador
# PLAYER_STARTING_POSITION = vec(1,1)

# Configuración del enemigo
