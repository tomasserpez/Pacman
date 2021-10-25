import pygame
vec = pygame.math.Vector2
from settings import *
import random


class Enemy:
    def __init__(self, pacman, position, number):
        self.pacman = pacman
        self.grid_position = position
        self.pixel_position = self.get_pixel_position()
        self.r = random.randint(1,255)
        self.g = random.randint(1,255)
        self.b = random.randint(1,255)
        self.number = number
        
    def update(self):
        pass
    
    def draw(self):
        pygame.draw.circle(self.pacman.screen, (self.r,self.g,self.b),self.pixel_position, 7)
    
    def get_pixel_position(self):
        return vec((self.grid_position.x*self.pacman.cell_width)+TOP_BOTTOM_BUFFER//2+self.pacman.cell_width//2, (self.grid_position.y*self.pacman.cell_height)+TOP_BOTTOM_BUFFER//2+self.pacman.cell_height//2)
    