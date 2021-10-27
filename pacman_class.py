import pygame, sys
from settings import *
from player_class import *
import random
from enemy_class import *
import copy

pygame.init()
vec = pygame.math.Vector2

################################ CLASE PACMAN ###################################

class pacman:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = "inicio"
        self.cell_width = MAZE_WIDTH//COLS
        self.cell_height = MAZE_HEIGHT//ROWS
        self.walls = []
        self.coins = []
        self.enemies = []
        self.enemy_position = []
        self.player_starting_position = []
        self.load()
        self.player = Player(self, vec(self.player_starting_position))
        self.make_enemies()
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
            elif self.state == 'game over':
                self.game_over_events()
                self.game_over_update()
                self.game_over_draw()
            elif self.state == 'win':
                self.win_events()
                self.win_update()
                self.win_draw()
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
        self.background = pygame.image.load('background.png')
        self.background = pygame.transform.scale(self.background, (MAZE_WIDTH, MAZE_HEIGHT))
        self.r = random.randint(1,255)
        self.g = random.randint(1,255)
        self.b = random.randint(1,255)
        # Abrimos el archivo con las coordenadas de cada pared
        #Creamos una lista en base a las coordenadas de las pared en formato vectorial
        with open("walls{}.txt".format(random.randint(0,1)), 'r') as file:
        #testwalls es un mapa de prueba para probar funcionalidad de victoria
        #with open("testwalls.txt", 'r') as file:
            for yindex, line in enumerate(file):
                for xindex, char in enumerate(line):
                    if char == "1":
                        self.walls.append(vec(xindex,yindex))
                    elif char == "C":
                        self.coins.append(vec(xindex,yindex))
                    elif char == "P":
                        self.player_starting_position = [xindex,yindex]
                    elif char in ["2","3","4","5"]:
                        self.enemy_position.append([xindex,yindex])
        
    def make_enemies(self):
        for index, position in enumerate(self.enemy_position):
            self.enemies.append(Enemy(self,vec(position), index))
        
    #Esta funcion nos va a servir para poder definir en un array que es cada seccion del mapa,
    #es decir, si es pared, camino o si hay una moneda.
    def draw_grid(self):
        for x in range(WIDTH//self.cell_width):
            pygame.draw.line(self.background, GREY, (x*self.cell_width, 0),(x*self.cell_width,HEIGHT))
        for x in range(HEIGHT//self.cell_height):
            pygame.draw.line(self.background, GREY, (0, x*self.cell_height),(WIDTH, x*self.cell_height))
    def draw_map(self):
        #DIBUJAMOS LAS PAREDES
        for wall in self.walls:
            pygame.draw.rect(self.background, (self.r,self.g,self.b),(wall.x*self.cell_width,wall.y*self.cell_height, self.cell_width, self.cell_height))
        # for coin in self.coins:
        #     pygame.draw.rect(self.background, (167,179,34),(coin.x*self.cell_width,coin.y*self.cell_height, self.cell_width, self.cell_height))
    def draw_coins(self):
        for coin in self.coins:
            pygame.draw.circle(self.screen,(167,179,34),(int(coin.x*self.cell_width)+self.cell_width//2+TOP_BOTTOM_BUFFER//2,int(coin.y*self.cell_height)+self.cell_height//2+TOP_BOTTOM_BUFFER//2),5)
    
    
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
        #self.draw_text('HIGH  SCORE', self.screen, [4,0], START_TEXT_SIZE, (255, 255, 255), START_FONT)
        pygame.display.update()



############################## FUNCIONES DEL JUEGO ##############################

    def juego_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.move(vec(-1,0))
                if event.key == pygame.K_RIGHT:
                    self.player.move(vec(1,0))
                if event.key == pygame.K_UP:
                    self.player.move(vec(0,-1))
                if event.key == pygame.K_DOWN:
                    self.player.move(vec(0,1))
                if event.key == pygame.K_r:
                    self.state = 'inicio'
                    self.__init__()
                    self.run()
                    

    
    def juego_update(self):
        self.player.update()
        for enemy in self.enemies:
            enemy.update()
            
        for enemy in self.enemies:
            if enemy.grid_position == self.player.grid_position:
                self.remove_life()
        if self.coins == []:
            self.state = "win"
    
    def juego_draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.background, (TOP_BOTTOM_BUFFER//2,TOP_BOTTOM_BUFFER//2))
        self.draw_coins()
        #Dibujamos la grilla
        # self.draw_grid()
        #Dibujamos el mapa
        self.draw_map()
        # self.draw_coins()
        #Textos
        self.draw_text('CURRENT SCORE: {}'.format(self.player.current_score), self.screen, [60,0], 18, WHITE, START_FONT, center=False)
        # self.draw_text('HIGH SCORE: 0', self.screen, [WIDTH//2+60,0], 18, WHITE, START_FONT, center=False)
        
        #Dibujamos al jugador
        self.player.draw()
        for enemy in self.enemies:
            enemy.draw()
        pygame.display.update()
        
    def remove_life(self):
        self.player.lives -= 1        
        if self.player.lives == 0:
            self.state = "game over"
        else:
            self.player.grid_position = vec(self.player.starting_position)
            self.player.pixel_position = self.player.get_pixel_position()
            self.player.direction *= 0
            for enemy in self.enemies:
                enemy.grid_position = vec(enemy.starting_position)
                enemy.pixel_position = enemy.get_pixel_position()
                enemy.direction *= 0
                
                
############################## FUNCIONES DEL FIN DE JUEGO ##############################

    def game_over_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.__init__()
                self.state = "juego"
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False
    def game_over_update(self):
        pass
    def game_over_draw(self):
        self.screen.fill(BLACK)
        self.draw_text("GAME OVER", self.screen, [WIDTH//2, 100], 36, RED, "arial", center=True)
        self.draw_text('PRESIONE ESPACIO PARA JUGAR OTRA VEZ', self.screen, [WIDTH//2, HEIGHT//2], START_TEXT_SIZE, (170,132,58), START_FONT, center = True)
        self.draw_text('PRESIONE ESCAPE PARA SALIR', self.screen, [WIDTH//2, HEIGHT//3], START_TEXT_SIZE, RED, START_FONT, center = True)
        self.draw_text('SU PUNTAJE: {}'.format(self.player.current_score), self.screen, [WIDTH//2, HEIGHT//2+50], START_TEXT_SIZE, (49, 176, 170), START_FONT, center = True)
        pygame.display.update()
        
############################## FUNCIONES DE VICTORIA DE JUEGO ##############################

    def win_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.__init__()
                self.state = "juego"
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False
    def win_update(self):
        pass
    def win_draw(self):
        self.screen.fill(BLACK)
        self.draw_text("YOU WIN", self.screen, [WIDTH//2, 100], 36, (170,132,58), "arial", center=True)
        self.draw_text('PRESIONE ESPACIO PARA JUGAR OTRA VEZ', self.screen, [WIDTH//2, HEIGHT//2], START_TEXT_SIZE, (170,132,58), START_FONT, center = True)
        self.draw_text('PRESIONE ESCAPE PARA SALIR', self.screen, [WIDTH//2, HEIGHT//3], START_TEXT_SIZE, RED, START_FONT, center = True)
        self.draw_text('SU PUNTAJE: {}'.format(self.player.current_score), self.screen, [WIDTH//2, HEIGHT//2+50], START_TEXT_SIZE, (49, 176, 170), START_FONT, center = True)
        pygame.display.update()