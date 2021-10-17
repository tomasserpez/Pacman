import pygame, sys
from settings import *


pygame.init()
vec = pygame.math.Vector2

################################ CLASE PACMAN ###################################

class pacman:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = "inicio"
        self.cell_width = WIDTH//28
        self.cell_height = HEIGHT//30
        
        self.load()
        
    #Definimos la función para ejecutar la aplicación con un estado inicial para
    #que comience en la pantalla de inicio    
    def run(self):
        while self.running:
            if self.state == 'inicio':
                self.inicio_events()
                self.inicio_update()
                self.inicio_draw()
            elif self.state == 'juego':
                self.juego_events()
                self.juego_update()
                self.juego_draw()
            else:
                self.running = False
            self.clock.tick(FPS)
            
        pygame.quit()
        sys.exit()
############################## FUNCIONES DE AYUDA ###############################

    #Esta es la función encargada de imprimir en pantalla los textos centrados
    def draw_text(self, words, screen, position, size, color, font_name, center = False):
        font = pygame.font.SysFont(font_name, size)
        text = font.render(words, False, color)
        text_size = text.get_size()
        if center:
            position[0] = position[0] - text_size[0]//2
            position[1] = position[1] - text_size[1]//2
        screen.blit(text,position)
        
    def load(self):
        self.background = pygame.image.load('maze.png')
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
        
    def draw_grid(self):
        for x in range(WIDTH//self.cell_width):
            pygame.draw.line(self.screen, GREY, (x*self.cell_width, 0),(x*self.cell_width,HEIGHT))
        for x in range(HEIGHT//self.cell_height):
            pygame.draw.line(self.screen, GREY, (0, x*self.cell_height),(WIDTH, x*self.cell_height))

############################## FUNCIONES INICIALES ##############################

    #Esta es la función que se encarga de decidir que hacer por cada evento
    #en la pantalla de inicio    
    def inicio_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.state = "juego"
    
    def inicio_update(self):
        pass
    #Esta es la función encargada de "dibujar" la pantalla
    def inicio_draw(self):
        self.screen.fill(BLACK)
        self.draw_text('PRESIONE  ESPACIO', self.screen, [WIDTH//2, HEIGHT//2], START_TEXT_SIZE, (170,132,58), START_FONT, center = True)
        self.draw_text('1  SOLO  JUGADOR', self.screen, [WIDTH//2, HEIGHT//2+50], START_TEXT_SIZE, (49, 176, 170), START_FONT, center = True)
        self.draw_text('Proyecto final', self.screen, [WIDTH//2, HEIGHT//2+150], START_TEXT_SIZE, (255, 255, 255), START_FONT, center = True)
        self.draw_text('Tomás Serpez', self.screen, [WIDTH//2, HEIGHT//2+170], START_TEXT_SIZE, (255, 255, 255), START_FONT, center = True)
        self.draw_text('HIGH  SCORE', self.screen, [4,0], START_TEXT_SIZE, (255, 255, 255), START_FONT)
        pygame.display.update()



############################## FUNCIONES DEL JUEGO ##############################

    def juego_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    
    def juego_update(self):
        pass
    
    def juego_draw(self):
        self.screen.blit(self.background, (0,0))
        self.draw_grid()
        pygame.display.update()