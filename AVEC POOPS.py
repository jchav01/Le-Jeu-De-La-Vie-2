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
initial_prey_number = 80
initial_wolves_number = 2

limit_eating = 1000 # Time after which a wolf dies with no eating

time = 0 
speed = 2  # velocity of the wolves
reproduction = 0 #ability to reproduce
reproduction_threshold = 9 # parameter of the reproduction factor
spawn_period = 1000
age_death = 1000
############# CLASSES #########################################################
class wolf:
    def __init__(self, position,  age = 0, days_without_eating=1, days_without_reproduction = 0, days_after_eating = 0):
        self.age = age
        self.position = position
        self.days_without_eating = days_without_eating
        self.days_after_eating = days_after_eating
        self.days_without_reproduction = days_without_reproduction

    def move(self, new_position):
        self.position = new_position

    def pass_day(self):
        self.age += 1
        self.days_without_eating += 1
        self.days_without_reproduction +=1
        
    def eat(self):
        self.days_without_eating = 0
        
    def reproduction(self):
        self.days_without_reproduction = 0
        

class prey:
    def __init__(self, position):
        self.position = position
        
    def move(self, new_position):
        self.position = new_position
   
    
class poo:
    def __init__(self, position):
        self.position = position
        
        
 
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

   
            
def look_for_new_position(position):
    x, y = position
    possible_positions = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]

    for new_pos in possible_positions:
        if not position_taken(new_pos, grid):
            return new_pos
    
    return None
        
    
# Defines the distance between 2 entities a and b
def distance(a,b):
    xa, ya = a.position
    xb, yb = b.position
    return np.abs((xb - xa)) + np.abs((yb - ya))

def position_taken(position, grid):
    x, y = position
    if x > grid_size - 1 or y > grid_size - 1:
        return True
    
    else: 
        return grid[x][y] != 0

def sigmoid_function(j):
    k = reproduction_threshold  # The number of days before being able to reproduce
    return 1 / (1 + np.exp(- (j - k)))

    
def rep_threshold(a,b):
    
    return sigmoid_function(a.days_without_reproduction)*sigmoid_function(b.days_without_reproduction)

def find_poop_in_list(Poo_list, x, y):
    
    for poo in Poo_list:
        
        if poo.position[0] == x and poo.position[1] == y:
            
            return poo
        
    return None

def is_in_grid(x,y):
    
    if 0 <= x < grid_size - 1 and 0 <= y < grid_size - 1:
        
        return True
    
    else:
        return False
    
    
########### WOlVES ROUTINE ####################################################

def reproduction(wolf_instance, Wolves_list, grid):
    new_wolves = []

    for other_wolf in Wolves_list:
        if wolf_instance != other_wolf and distance(wolf_instance, other_wolf) <= 3 and rep_threshold(wolf_instance, other_wolf) > 0.5:
            x1, y1 = wolf_instance.position
            x2, y2 = other_wolf.position
            possible_positions = [(x1 + 1, y1), (x1 - 1, y1), (x1, y1 + 1), (x1, y1 - 1),
                                  (x2 + 1, y2), (x2 - 1, y2), (x2, y2 + 1), (x2, y2 - 1)]

            for new_pos in possible_positions:
                if not position_taken(new_pos, grid):
                    new_wolf = wolf(new_pos)
                    new_wolves.append(new_wolf)
                    break

            # Reset the reproduction rate to 0
            wolf_instance.reproduction()
            other_wolf.reproduction()

    Wolves_list += new_wolves

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
        x1, y1 = pred.position
        x2, y2 = nearest_prey.position
    
        # Calculate the direction vector from the predator to the prey
        dx = x2 - x1
        dy = y2 - y1
    
        # Normalize the direction vector to have a magnitude of 1
        magnitude = np.maximum(1, abs(dx) + abs(dy))
        dx /= magnitude
        dy /= magnitude   
    
        # Calculate the new position based on the direction vector and speed
        new_position = (x1 + round(speed * dx), y1 + round(speed * dy))
        
        # Check if the new position is within the grid
        if 0 <= new_position[0] < grid_size and 0 <= new_position[1] < grid_size and not position_taken(new_position,grid):
            pred.move(new_position)


def Eat(pred, prey_list):
    
    for j, prey_instance in enumerate(prey_list):
        if distance(pred, prey_instance) < 2:
            # Mark the prey for removal
            del prey_list[j]
            pred.eat()
            continue
        
def defect(pred, Poo_list):
    if pred.days_without_eating == 0:
        pred.days_after_eating += 1
        
    if pred.days_after_eating == 3:
        create_new_poo(pred.position, Poo_list)
        pred.days_without_eating = 1
        pred.days_after_eating = 0 

def is_encircled(pred, Prey_list):

    if around_wolf(pred) >= 4:
        Wolves_list.remove(pred)
        
def around_wolf(pred):
    count = 0
    x, y = pred.position
    for i in range(3):
        for j in range(3):
            if is_in_grid(x+i, y+j):
                if grid[x+i][y+j]==1:
                    count += 1
    return count
    
def check_deaths(wolf_instance):
    
    if wolf_instance.days_without_eating == limit_eating or wolf_instance.age > age_death:
        Wolves_list.remove(wolf_instance)
            


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
        new_position = (x1 + round(speed * dx), y1 + round(speed * dy))
        
        # Check if the new position is within the grid
        if is_in_grid(new_position[0], new_position[1]) and not position_taken(new_position,grid):
            prey.move(new_position)
    
    else :
        
        preys_movement(prey)
                
def is_around(Poo_list, prey, grid):
    

    x, y = prey.position
    radius = 30
    for i in range(- radius, radius):
        for j in range(- radius, radius) :
            
            if i!= 0 or j!= 0:
                if 0 <= x + i < grid_size - 1 and 0 <= y + j < grid_size - 1:
                    if grid[x+i][y+j] == 3:
                
                        poop = find_poop_in_list(Poo_list, x + i, y + j)
                 
                        return poop                    

def Eat_poo(Poo_list, prey, Prey_list):
    for j, poo_instance in enumerate(Poo_list):
        if distance(prey, poo_instance) < 2:
            
            transform_to_prey(poo_instance, Poo_list, Prey_list)

def transform_to_prey(poo, Poo_list, Prey_list):
    
    pos = poo.position
    Poo_list.remove(poo)
    prey_instance = prey(pos)
    Prey_list.append(prey_instance)

    for i in range(2):
        additionnal = look_for_new_position(pos)
        if additionnal :
            prey_2 = prey(additionnal)
            Prey_list.append(prey_2)

def preys_movement(prey):
    
    if time%3 == 0:
    
        x,y = prey.position
        
        possible_moves = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        random_move = random.choice(possible_moves)
        
        if 0 <= random_move[0] < grid_size - 1 and 0 <= random_move[1] < grid_size - 1 and not position_taken(random_move,grid):
            prey.move(random_move)

def add_random_prey():
    
    if time % spawn_period == 0:
        
        position = (random.randint(0, grid_size - 1), random.randint(0, grid_size - 1))
        prey_instance = prey(position)
        Prey_list.append(prey_instance)
        
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
        
    add_random_prey()
    
    for pred in Wolves_list:
        pred.pass_day()
        check_deaths(pred)
        Eat(pred, Prey_list)
        if reproduction == 1:
            reproduction(pred, Wolves_list, grid)
        Chase(pred, Prey_list, grid)
        defect(pred, Poo_list)
    
    

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

    # Update the display
    pygame.display.flip()

    # Control frame rate (adjust the value as needed)
    clock.tick(4)  # Example: 10 frames per second

# Quit Pygame
pygame.quit()
