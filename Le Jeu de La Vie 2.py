# -*- coding: utf-8 -*-
"""
Created on Sat Oct 14 13:10:55 2023

@author: jules
"""
import pygame
import numpy as np
import random
import math




# Paramètres
grid_size = 80
initial_prey_number = 50
initial_wolves_number = 6
spawn_period = 60
limit_eating = 20 # Time after which a wolf dies with no eating
reproduction_threshold = 9 # parameter of the reproduction factor
age_death = 140
time = 0 
speed = 2  # velocity of the wolves

############# CLASSES #########################################################
class wolf:
    def __init__(self, position,  age = 0, days_without_eating=0, days_without_reproduction = 0):
        self.age = age
        self.position = position
        self.days_without_eating = days_without_eating
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
        
        
 
############ FUNCTIONS ########################################################

def create_new_wolf(Wolves_list):
    position = (random.randint(0, grid_size - 1), random.randint(0, grid_size - 1))
    wolf_instance = wolf(position)
    Wolves_list.append(wolf_instance)


def create_new_prey(Prey_list):
    position = (random.randint(0, grid_size - 1), random.randint(0, grid_size - 1))
    prey_instance = prey(position)
    Prey_list.append(prey_instance)
    
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
    
def find_prey(x, y, Prey_list):
    
    for p in Prey_list:
        
        if p.position[0] == x and p.position[1] == y:
            
            return p

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
        new_position = (x1 + math.ceil(speed * dx), y1 + math.ceil(speed * dy))
        
        # Check if the new position is within the grid
        if 0 <= new_position[0] < grid_size and 0 <= new_position[1] < grid_size and not position_taken(new_position,grid):
            pred.move(new_position)


def Eat(pred, prey_list):
    
    for j, prey_instance in enumerate(prey_list):
        if distance(pred, prey_instance) < 2:
            # Mark the prey and wolf for removal
            del prey_list[j]
            pred.eat()
            continue
        
            
    
def check_deaths(wolf_instance):
    
    if wolf_instance.days_without_eating == limit_eating or wolf_instance.age > age_death:
        Wolves_list.remove(wolf_instance)
            


######## PREYS Routine #######################################################

def preys_movement():
    
    if time%2 == 0:
        
        for prey_instance in Prey_list:
            
            x,y = prey_instance.position
            
            possible_moves = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
            random_move = random.choice(possible_moves)
            
            if 0 <= random_move[0] < grid_size - 1 and 0 <= random_move[1] < grid_size - 1 and not position_taken(random_move,grid):
                prey_instance.move(random_move)

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
    
def update_grid(Wolves_list, Prey_list):
    
    # Create a new empty grid with white cells
    new_grid = [[0 for _ in range(grid_size)] for _ in range(grid_size)]
    
    for prey in Prey_list:
        x, y = prey.position
        if 0 <= x < grid_size and 0 <= y < grid_size:
            new_grid[x][y] = 1  # Update the new grid with new positions of prey
    
    for pred in Wolves_list:
        x, y = pred.position
        if 0 <= x < grid_size and 0 <= y < grid_size:
            new_grid[x][y] = 2  # Update the new grid with new positions of pred
    return new_grid
     
# Create initial grid
grid = update_grid(Wolves_list, Prey_list)




##### UPDATE ##################################################################
    
    
def update():
    global Wolves_list, Prey_list, grid, time  # Add time as a global variable

    # CALL MAIN FUNCTIONS
    preys_movement()
    add_random_prey()
    
    for pred in Wolves_list:
        pred.pass_day()
        check_deaths(pred)
        Eat(pred, Prey_list)
        reproduction(pred, Wolves_list, grid)
        Chase(pred, Prey_list, grid)
    
    
    

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
    clock.tick(10)  # Example: 10 frames per second

# Quit Pygame
pygame.quit()
