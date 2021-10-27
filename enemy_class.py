import pygame
vec = pygame.math.Vector2
from settings import *
import random


class Enemy:
    def __init__(self, pacman, position, number):
        self.pacman = pacman
        self.grid_position = position
        self.starting_position = [position.x, position.y]
        self.pixel_position = self.get_pixel_position()
        self.r = random.randint(1,255)
        self.g = random.randint(1,255)
        self.b = random.randint(1,255)
        self.number = number
        self.direction = vec(0,0)
        self.personality = self.set_personality()
        self.target = None
        self.speed = self.set_speed()
        
    def update(self):
        self.target = self.set_target()
        if self.target != self.grid_position:
            self.pixel_position += self.direction * self.speed
            if self.time_to_move():
                self.move()
        
        # Configuramos la posicion en referencia a la posicion del pixel
        self.grid_position[0] = (self.pixel_position[0]-TOP_BOTTOM_BUFFER+self.pacman.cell_width//2)//self.pacman.cell_width+1
        self.grid_position[1] = (self.pixel_position[1]-TOP_BOTTOM_BUFFER+self.pacman.cell_height//2)//self.pacman.cell_height+1
    
    def draw(self):
        pygame.draw.circle(self.pacman.screen, (self.r,self.g,self.b),self.pixel_position, 7)
    
    def set_speed(self):
        if self.personality in ["speedy", "scared"]:
            speed = 2
        else:
            speed = 1
        return speed
    
    def set_target(self):
        if self.personality == "speedy" or self.personality == "slow":
            return self.pacman.player.grid_position
        else:
            if self.pacman.player.grid_position[0] > COLS//2 and self.pacman.player.grid_position[1] > ROWS//2:
                return vec(1,1)
            if self.pacman.player.grid_position[0] > COLS//2 and self.pacman.player.grid_position[1] < ROWS//2:
                return vec(1,ROWS-2)
            if self.pacman.player.grid_position[0] < COLS//2 and self.pacman.player.grid_position[1] > ROWS//2:
                return vec(COLS-2,1)
            else:
                return vec(COLS-2,ROWS-2)
    
    def get_pixel_position(self):
        return vec((self.grid_position.x*self.pacman.cell_width)+TOP_BOTTOM_BUFFER//2+self.pacman.cell_width//2, (self.grid_position.y*self.pacman.cell_height)+TOP_BOTTOM_BUFFER//2+self.pacman.cell_height//2)
    
    def time_to_move(self):
        if int(self.pixel_position.x+TOP_BOTTOM_BUFFER//2) % self.pacman.cell_width == 0:
            if self.direction == vec(1,0) or self.direction == vec(-1,0) or self.direction == vec(0,0):
                return True
        if int(self.pixel_position.y+TOP_BOTTOM_BUFFER//2) % self.pacman.cell_height == 0:
            if self.direction == vec(0,1) or self.direction == vec(0,-1) or self.direction == vec(0,0):
                return True
        #return False
    
    def move(self):
        if self.personality == "random":
            self.direction = self.get_random_direction()
        elif self.personality == "slow":
            self.direction = self.get_path_direction(self.target)
        elif self.personality == "speedy":
            self.direction = self.get_path_direction(self.target)
        elif self.personality == "scared":
            self.direction = self.get_path_direction(self.target)
            
    def get_path_direction(self,target):
        next_cell = self.find_next_cell_in_path(target)
        xdir = next_cell[0] - self.grid_position[0]
        ydir = next_cell[1] - self.grid_position[1]
        return vec(xdir,ydir)
    
    def find_next_cell_in_path(self, target):
        path = self.BFS([int(self.grid_position.x), int(self.grid_position.y)],[int(target[0]),int(target[1])])

        return path[1]
    
    def BFS(self, start, target):
        grid = [[0 for x in range(28)] for x in range(30)]
        for cell in self.pacman.walls:
            if cell.x < 28 and cell.y < 30:
                grid[int(cell.y)][int(cell.x)] = 1
        queue = [start]
        path = []
        visited = []
        while queue:
            current = queue[0]
            queue.remove(queue[0])
            visited.append(current)
            if current == target:
                break
            else:
                neighbours = [[0, -1], [1, 0], [0, 1], [-1, 0]]
                for neighbour in neighbours:
                    if neighbour[0]+current[0] >= 0 and neighbour[0] + current[0] < len(grid[0]):
                        if neighbour[1]+current[1] >= 0 and neighbour[1] + current[1] < len(grid):
                            next_cell = [neighbour[0] + current[0], neighbour[1] + current[1]]
                            if next_cell not in visited:
                                if grid[next_cell[1]][next_cell[0]] != 1:
                                    queue.append(next_cell)
                                    path.append({"Current": current, "Next": next_cell})
        shortest = [target]
        while target != start:
            for step in path:
                if step["Next"] == target:
                    target = step["Current"]
                    shortest.insert(0, step["Current"])
        return shortest              
    
    def get_random_direction(self):
        while True:
            number = random.randint(-2,2)
            if number == -2:
                x_dir, y_dir = 1,0
            elif number == -1:
                x_dir, y_dir = 0,1
            elif number== 0:
                x_dir, y_dir = -1,0
            else:
                x_dir, y_dir = 0,-1
            next_position = vec(self.grid_position.x + x_dir, self.grid_position.y + y_dir)
            if next_position not in self.pacman.walls:
                break
            # if vec(direction.x+x_dir, direction.y+y_dir) in self.pacman.walls:
            #     break
        return vec(x_dir, y_dir)
            
    def set_personality(self):
        if self.number == 0:
            return "speedy"
        elif self.number == 1:
            return "slow"
        elif self.number == 2:
            return "random"
        else:
            return "scared"
        