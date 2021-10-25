#Definimos la clase del jugador
import pygame
from settings import *
vec = pygame.math.Vector2

class Player:
    def __init__(self, pacman, position):
        self.pacman = pacman
        self.grid_position = position
        self.pixel_position = self.get_pixel_position()
        self.direction = vec(1,0)
        self.stored_direction = None
        self.able_to_move = True
        self.current_score = 0
        self.speed = 2
        #print(self.grid_position, self.pixel_position)
        
    
    
    def update(self):
        if self.able_to_move:
            self.pixel_position += self.direction*self.speed
        if self.time_to_move():
            if self.stored_direction != None:
                self.direction = self.stored_direction
            self.able_to_move = self.can_move()
        
        
        #Configuración de la grilla para referencial la posición del pixel
        self.grid_position[0] = (self.pixel_position[0]-TOP_BOTTOM_BUFFER+self.pacman.cell_width//2)//self.pacman.cell_width+1
        self.grid_position[1] = (self.pixel_position[1]-TOP_BOTTOM_BUFFER+self.pacman.cell_height//2)//self.pacman.cell_height+1
        
        if self.on_coin():
            self.eat_coin()

    
    def draw(self):
        pygame.draw.circle(self.pacman.screen, PLAYER_COLOR, (int(self.pixel_position.x),int(self.pixel_position.y)), self.pacman.cell_width//2-2)
        #Dibuja el rectangulo en la grilla
        # pygame.draw.rect(self.pacman.screen, RED, (self.grid_position[0]*self.pacman.cell_width+TOP_BOTTOM_BUFFER//2,self.grid_position[1]*self.pacman.cell_height+TOP_BOTTOM_BUFFER//2, self.pacman.cell_width,self.pacman.cell_height), 1)
        
    def move(self, direction):
        self.stored_direction = direction
        
    def get_pixel_position(self):
        return vec((self.grid_position.x*self.pacman.cell_width)+TOP_BOTTOM_BUFFER//2+self.pacman.cell_width//2, (self.grid_position.y*self.pacman.cell_height)+TOP_BOTTOM_BUFFER//2+self.pacman.cell_height//2)
    
    def time_to_move(self):
        if int(self.pixel_position.x+TOP_BOTTOM_BUFFER//2) % self.pacman.cell_width == 0:
            if self.direction == vec(1,0) or self.direction == vec(-1,0):
                return True
        if int(self.pixel_position.y+TOP_BOTTOM_BUFFER//2) % self.pacman.cell_height == 0:
            if self.direction == vec(0,1) or self.direction == vec(0,-1):
                return True
            
    def can_move(self):
        for wall in self.pacman.walls:
            if vec(self.grid_position+self.direction) == wall:
                return False
        return True
    
    def on_coin(self):
        if self.grid_position in self.pacman.coins:
            if int(self.pixel_position.x+TOP_BOTTOM_BUFFER//2) % self.pacman.cell_width == 0:
                if self.direction == vec(1,0) or self.direction == vec(-1,0):
                    return True
            if int(self.pixel_position.y+TOP_BOTTOM_BUFFER//2) % self.pacman.cell_height == 0:
                if self.direction == vec(0,1) or self.direction == vec(0,-1):
                    return True
        return False
            
    def eat_coin(self):
        self.pacman.coins.remove(self.grid_position)
        self.current_score += 1