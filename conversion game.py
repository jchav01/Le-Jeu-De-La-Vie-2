# -*- coding: utf-8 -*-
"""
Created on Sat Oct 14 13:10:55 2023

@author: jules
"""
import pygame
import numpy as np
import random





# Paramètres
grid_size = 80
initial_prey_number = 100
initial_wolves_number = 1
poo_spawntime = 4
poo_to_prey_number = 3
preys_around_number = 5
poo_lifetime = 35
poo_speed_when_chasing = 2
time = 0 
speed = 2  # velocity of the wolves

game_over = False
win = False



############# CLASSES #########################################################
class wolf:
    def __init__(self, position, days_after_eating =  -1):
        self.position = position
        self.days_after_eating = days_after_eating
    

    def move(self, new_position):
        self.position = new_position
    
    def eat(self):
        self.days_after_eating = 0
      
    def poop(self):
        self.days_after_eating = -1 

class prey:
    def __init__(self, position):
        self.position = position
        
    def move(self, new_position):
        self.position = new_position
   
    
class poo:
    def __init__(self, position, age = 0):
        self.position = position
        self.age = age
        
    def aging(self):
        self.age += 1
        
 
############ FUNCTIONS ########################################################

def create_new_wolf(Wolves_list):
    position = (random.randint(0, grid_size - 1), random.randint(0, grid_size - 1))
    wolf_instance = wolf(position)
    Wolves_list.append(wolf_instance)


def create_new_prey(Prey_list):
    position = (random.randint(0, grid_size - 1), random.randint(0, grid_size - 1))
    prey_instance = prey(position)
    Prey_list.append(prey_instance)

def create_new_poo(position, Poo_list):
    new_pos = look_for_new_position(position)
    if new_pos != None:
        new_poo = poo(new_pos)
    Poo_list.append(new_poo)


        
    
# Defines the distance between 2 entities a and b
def distance(a,b):
    xa, ya = a.position
    xb, yb = b.position
    return np.abs((xb - xa)) + np.abs((yb - ya))

def position_taken(position, grid):
    x, y = position
    if x > grid_size - 1 or x < 0 or y > grid_size - 1 or y < 0:
        return True
    
    else: 
        return grid[x][y] != 0


def find_poop_in_list(Poo_list, x, y):
    
    for poo in Poo_list:
        
        if poo.position[0] == x and poo.position[1] == y:
            
            return poo
        
    return None

def is_in_grid(position):
    x,y = position
    if 0 <= x < grid_size - 1 and 0 <= y < grid_size - 1:
        
        return True
    
    else:
        return False
    
    
########### WOlVES ROUTINE ####################################################


def find_nearest_prey(wolf_instance, prey_list):
    nearest_prey = None
    min_distance = float('inf')
    for prey_instance in prey_list:
        dist = distance(wolf_instance, prey_instance)
        if dist < min_distance:
            min_distance = dist
            nearest_prey = prey_instance
    return nearest_prey

        
   
def Chase(pred, prey_list, grid):
   
    nearest_prey = find_nearest_prey(pred, prey_list)
    if nearest_prey:
        
        for i in range(speed):
            
            # we define the vector 
            x1, y1 = pred.position
            x2, y2 = nearest_prey.position
            
            # Calculate the direction vector from the predator to the prey
            dx = x2 - x1
            dy = y2 - y1
            
            # Normalize the direction vector to have a magnitude of 1
            magnitude = np.maximum(1, abs(dx) + abs(dy))
            dx /= magnitude
            dy /= magnitude  
            
            new_pos = (x1 + round(dx + 0.001), y1 + round(dy + 0.001))
            
            if is_in_grid(new_pos) and not position_taken(new_pos, grid):
                pred.move(new_pos)
                
def preys_are_around(pred, Prey_list, grid):

    count = 0
    x, y = pred.position
    for i in range(-2, 3):
        for j in range(-2,3):
            pos_to_check = (x+i,y+j)
            if is_in_grid(pos_to_check):
                if grid[x+i][y+j] == 1:
                    count += 1
            
    return count

def Eat(pred, prey_list, grid):
    
    for j, prey_instance in enumerate(prey_list):
        if distance(pred, prey_instance) <= 2:
            if preys_are_around(pred, Prey_list, grid) < 1000:
                # Mark the prey for removal
                del prey_list[j]
                if pred.days_after_eating == -1:
                    pred.eat()
                    continue
        
def defect(pred, Poo_list):
    
    if pred.days_after_eating >= 0:
    
        pred.days_after_eating += 1
        
    if pred.days_after_eating == poo_spawntime:
        create_new_poo(pred.position, Poo_list)
        pred.poop()


def is_encircled(pred, grid):

    if around_wolf(pred, grid) >= preys_around_number:
        Wolves_list.remove(pred)
 

def around_wolf(pred, grid):
    count = 0
    x, y = pred.position
    arr = 2
    for i in range(-arr, arr +1):
        for j in range(-arr, arr +1):
            pos = (x+i, y+j)
            if is_in_grid(pos):
                if grid[x+i][y+j]==1:
                    count += 1
    return count
 
          


######## PREYS Routine #######################################################
def chase_poo(Poo_list, prey, grid, grid_size):
    
    poo = is_around(Poo_list, prey, grid)
    
    if poo:
        
        x1, y1 = prey.position
        x2, y2 = poo.position
    
        # Calculate the direction vector from the predator to the prey
        dx = x2 - x1
        dy = y2 - y1
    
        # Normalize the direction vector to have a magnitude of 1
        magnitude = np.maximum(1, abs(dx) + abs(dy))
        dx /= magnitude
        dy /= magnitude   
    
        # Calculate the new position based on the direction vector and speed
        new_position = (x1 + round(poo_speed_when_chasing*dx), y1 + round(poo_speed_when_chasing*dy))
        
        # Check if the new position is within the grid
        if is_in_grid(new_position) and not position_taken(new_position,grid):
            prey.move(new_position)
    
    else :
        
        preys_movement(prey)
                
def is_around(Poo_list, prey, grid):
    
    x, y = prey.position
    radius = 40
    for i in range(- radius, radius):
        for j in range(- radius, radius) :
            
            if i!= 0 or j!= 0:
                position = (x+i, y + j)
                if is_in_grid(position):
                    if grid[x+i][y+j] == 3:
                
                        poop = find_poop_in_list(Poo_list, x + i, y + j)
                 
                        return poop                    

def Eat_poo(Poo_list, prey, Prey_list):
    for j, poo_instance in enumerate(Poo_list):
        if distance(prey, poo_instance) <= 2:
            
            transform_to_prey(poo_instance, Poo_list, Prey_list)
            
def look_for_new_position(position):
    x, y = position
    possible_positions = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1),
                          (x+1, y+1), (x+1, y-1), (x-1, y+1), (x-1, y-1), 
                          (x+2, y), (x-2, y), (x, y+2), (x, y-2),
                          (x+2, y+1), (x+2, y-1), (x-2, y+1), (x-2, y-1),
                          (x+1, y+2), (x+1, y-2), (x-1, y+2), (x-1, y-2)]

    for new_pos in possible_positions:
        if is_in_grid(new_pos) and not position_taken(new_pos, grid):
            return new_pos
    
    return None

def transform_to_prey(poo, Poo_list, Prey_list):
    
    pos = poo.position
    Poo_list.remove(poo)
    prey_instance = prey(pos)
    Prey_list.append(prey_instance)

    for i in range(poo_to_prey_number):
        additionnal = look_for_new_position(pos)
        if additionnal != None :
            prey_2 = prey(additionnal)
            Prey_list.append(prey_2)

def preys_movement(prey):
    
    if time%2 == 0:
    
        x,y = prey.position
        
        possible_moves = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        random_move = random.choice(possible_moves)
        
        if 0 <= random_move[0] < grid_size - 1 and 0 <= random_move[1] < grid_size - 1 and not position_taken(random_move,grid):
            prey.move(random_move)
############ POO ROUTINE ######################################################

def poo_dies(poo, Poo_list):
    
    Poo_list.remove(poo)
    
        
############# INITIALISATION ##################################################

# Initialisation des Loups et des proies
Wolves_list = []
for _ in range(initial_wolves_number):
    
    create_new_wolf(Wolves_list)

Prey_list = []
for _ in range(initial_prey_number):
    
    create_new_prey(Prey_list)

Poo_list = []

    
def update_grid(Wolves_list, Prey_list):
    
    # Create a new empty grid with white cells
    new_grid = [[0 for _ in range(grid_size)] for _ in range(grid_size)]
    
    for prey in Prey_list:
        x, y = prey.position
        if 0 <= x < grid_size - 1 and 0 <= y < grid_size - 1:
            new_grid[x][y] = 1  # Update the new grid with new positions of prey
    
    for pred in Wolves_list:
        x, y = pred.position
        if 0 <= x < grid_size - 1 and 0 <= y < grid_size - 1:
            new_grid[x][y] = 2  # Update the new grid with new positions of pred
    
    for poo in Poo_list:
        x, y = poo.position
        if 0 <= x < grid_size - 1 and 0 <= y < grid_size - 1:
            new_grid[x][y] = 3  # Update the new grid with new positions of poo
            
    return new_grid
     
# Create initial grid
grid = update_grid(Wolves_list, Prey_list)




##### UPDATE ##################################################################
    
    
def update():
    global Wolves_list, Prey_list, Poo_list, grid, time  # Add time as a global variable

    # CALL MAIN FUNCTIONS
    for prey in Prey_list:
        chase_poo(Poo_list, prey, grid, grid_size)
        Eat_poo(Poo_list, prey, Prey_list)
        
    
    for pred in Wolves_list:
        Eat(pred, Prey_list, grid)
        Chase(pred, Prey_list, grid)
        defect(pred, Poo_list)
        is_encircled(pred, grid)
    
    for poo in Poo_list:
        poo.aging()
        if poo.age == poo_lifetime:
            poo_dies(poo, Poo_list)

    grid = update_grid(Wolves_list, Prey_list)

    time += 1  # Increment the time
    
############ AFFICHAGE ########################################################
# Initialize Pygame
pygame.init()

# Define screen parameters
grid_size = 80
cell_size = 10
screen_width = grid_size * cell_size
screen_height = grid_size * cell_size

# Create the Pygame window
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Wolf and Prey Simulation")

# Pygame color constants
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

# Function to draw the grid
def draw_grid(grid, screen):
    for x in range(grid_size):
        for y in range(grid_size):
            cell_color = None
            if grid[x][y] == 1:
                cell_color = GREEN  # Prey
            elif grid[x][y] == 2:
                cell_color = RED  # Wolf
            elif grid[x][y] == 3:
                cell_color = YELLOW  # Poop
            else:
                cell_color = BLACK  # Empty

            pygame.draw.rect(screen, cell_color, (x * cell_size, y * cell_size, cell_size, cell_size))

# Main game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update the grid (call your update function here)
    update()

    # Clear the screen
    screen.fill((255, 255, 255))

    # Draw the grid
    draw_grid(grid, screen)

    # Check win or lose conditions
    if not Wolves_list:
        game_over = True
    elif not Prey_list:
        game_over = True
        win = True

    # Update the display
    pygame.display.flip()

    # Control frame rate (adjust the value as needed)
    clock.tick(4)  # Example: 4 frames per second

    # If the game is over, display a message
    if game_over:
        font = pygame.font.Font(None, 36)
        text = font.render('You Win!' if win else 'You Lose!', True, (255, 0, 0))
        text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.wait(2000)  # Display the message for 2 seconds
        running = False  # Exit the game loop

# Quit Pygame
pygame.quit()
