#Definimos la clase del jugador
import pygame
from settings import *
vec = pygame.math.Vector2

class Player:
    def __init__(self, pacman, position):
        self.pacman = pacman
        self.grid_position = position
        self.pixel_position = vec((self.grid_position.x*self.pacman.cell_width)+TOP_BOTTOM_BUFFER//2+self.pacman.cell_width//2, (self.grid_position.y*self.pacman.cell_height)+TOP_BOTTOM_BUFFER//2+self.pacman.cell_height//2)
        print(self.grid_position, self.pixel_position)
        
    
    
    def update(self):
        pass
    
    def draw(self):
        pygame.draw.circle(self.pacman.screen, PLAYER_COLOR, (int(self.pixel_position.x),int(self.pixel_position.y)), self.pacman.cell_width//2-2)