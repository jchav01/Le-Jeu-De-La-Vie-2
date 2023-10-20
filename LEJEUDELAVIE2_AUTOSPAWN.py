# -*- coding: utf-8 -*-
"""
Created on Sat Oct 14 13:10:55 2023

@author: jules
"""

"""
-Auto spawn on preys
-Auto spawn on predators
-Regulated through chase and limit-time life without eating for wolves

- Stability of the 2 pops, stabilizing at two distincts values OR
- Extinction of all pops, preys first and then preds

-Idea : can introduce spawn at 0 when a pop is extinded to repopulate the system... 
but objective: find a way not to reach 0 ? anyway.

-Or we can introduce a need to chase, that goes to 0 when has eaten: leaves some room for the 
other specie to populate

"""

import pygame
import numpy as np
import random
import matplotlib.pyplot as plt

# Create empty lists to store population data
wolf_population = []
prey_population = []



# Paramètres
grid_size = 130
initial_prey_number = 30
initial_wolves_number = 4
prey_spawn_ratio = 0.05
pred_spawn_ratio = 0.025
limit_eating = 25 # Time after which a wolf dies with no eating
time = 0 
speed = 2  # velocity of the wolves
SPAWN = 0
SPAWN_1 = 0

############# CLASSES #########################################################
class wolf:
    def __init__(self, position, days_without_eating = 0):
        self.position = position
        self.days_without_eating = days_without_eating

    def move(self, new_position):
        self.position = new_position

        
    def eat(self):
        self.days_without_eating = 0
        


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
    
    if not is_in_grid(position):
        
        return True
    
    else: 
    
        return grid[x][y] != 0

def sigmoid_function(j, k):

    return 1 / (1 + np.exp(- (j - k)))

    
    
def find_prey(x, y, Prey_list):
    
    for p in Prey_list:
        
        if p.position[0] == x and p.position[1] == y:
            
            return p

def is_in_grid(position):
    x,y = position
    if 0 <= x < grid_size - 1 and 0 <= y < grid_size - 1:
        
        return True
    
    else:
        return False


    
########### WOlVES ROUTINE ####################################################
"""
def reproduction(wolf_instance, mate, Wolves_list, grid):

    x1, y1 = wolf_instance.position
    if mate.days_without_reproduce > 15 :
        
        possible_positions = [(x1 + 1, y1), (x1 - 1, y1), (x1, y1 + 1), (x1, y1 - 1),
                              (x1 + 1, y1+1), (x1 + 1, y1-1), (x1-1, y1 + 1), (x1 - 1, y1 - 1)]
    
        for new_pos in possible_positions:
            if not position_taken(new_pos, grid):
                new_wolf = wolf(new_pos)
                wolf_instance.reproduction()
                mate.reproduction()
                Wolves_list.append(new_wolf)
                break
    

def find_nearest_sex_mate(pred, Pred_list):
    nearest_mate = None
    min_distance = float('inf')
    for mate in Pred_list:
        dist = distance(pred, mate)
        
        if dist < min_distance and dist >=1:
            min_distance = dist
            nearest_mate = mate
    return nearest_mate

def go_to_mate(pred, mate, grid):
    
    x1, y1 = pred.position
    x2, y2 = mate.position

    # Calculate the direction vector from the predator to the prey
    dx = x2 - x1
    dy = y2 - y1

    # Normalize the direction vector to have a magnitude of 1
    magnitude = np.maximum(1, abs(dx) + abs(dy))
    dx /= magnitude
    dy /= magnitude   

    # Calculate the new position based on the direction vector and speed
    new_position = (x1 + round(dx + 0.01), y1 + round(dy+0.01))
    
    # Check if the new position is within the grid
    if is_in_grid(new_position) and not position_taken(new_position,grid):
        pred.move(new_position)

"""

def find_nearest_prey(wolf_instance, prey_list):
    nearest_prey = None
    min_distance = float('inf')
    for prey_instance in prey_list:
        dist = distance(wolf_instance, prey_instance)
        if dist < min_distance:
            min_distance = dist
            nearest_prey = prey_instance
    return nearest_prey

    
    

def Next_movement(pred, Prey_list, Pred_list, grid):
    
    if pred.days_without_eating > -1 : 
        Chase(pred, Prey_list, grid)
    """
    else:
        
        if pred.days_without_reproduce > 15 : 
            mate = find_nearest_sex_mate(pred, Pred_list)
            
            if mate: 
                
                go_to_mate(pred, mate, grid)
                
                if distance(pred, mate) <= 2:
                    reproduction(pred, mate, Pred_list, grid)
                
    """
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
        new_position = (x1 + round(speed * dx + 0.01), y1 + round(speed * dy + 0.01))
        
        # Check if the new position is within the grid
        if is_in_grid(new_position) and not position_taken(new_position,grid):
            pred.move(new_position)


def Eat(pred, prey_list):
    
    for j, prey_instance in enumerate(prey_list):
        if distance(pred, prey_instance) < 2:
            # Mark the prey for removal
            del prey_list[j]
            pred.eat()
            continue
        
def pass_day(pred):

    pred.days_without_eating += 1
        
            
    
def check_deaths(wolf_instance):
    
    if wolf_instance.days_without_eating == limit_eating :
        Wolves_list.remove(wolf_instance)
            
def add_random_pred(SPAWN_1, Wolves_list):
    
   SPAWN_1 += pred_spawn_ratio * len(Wolves_list)
   
   for i in range(int(SPAWN_1)) :
        
        create_new_wolf(Wolves_list)
        
        SPAWN_1 = 0
    
   return SPAWN_1

######## PREYS Routine #######################################################

def preys_movement():
    
    if time%2 == 0:
        
        for prey_instance in Prey_list:
            
            x,y = prey_instance.position
            
            possible_moves = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
            random_move = random.choice(possible_moves)
            
            if 0 <= random_move[0] < grid_size - 1 and 0 <= random_move[1] < grid_size - 1 and not position_taken(random_move,grid):
                prey_instance.move(random_move)

def add_random_prey(SPAWN, Prey_list):
    
   SPAWN += prey_spawn_ratio * len(Prey_list)
   
   for i in range(int(SPAWN)) :
        
        create_new_prey(Prey_list)
        
        SPAWN = 0
    
   return SPAWN
        
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
    global Wolves_list, Prey_list, grid, time, SPAWN, SPAWN_1 # Add time as a global variable

    # CALL MAIN FUNCTIONS
    preys_movement()
    SPAWN = add_random_prey(SPAWN, Prey_list)
    SPAWN_1 = add_random_pred(SPAWN_1, Wolves_list)
    
    for pred in Wolves_list:
        pass_day(pred)
        check_deaths(pred)
        Next_movement(pred, Prey_list, Wolves_list, grid)
        Eat(pred, Prey_list)
        

    grid = update_grid(Wolves_list, Prey_list)

    time += 1  # Increment the time
    
############ AFFICHAGE ########################################################
# Initialize Pygame
pygame.init()

# Define screen parameters
grid_size = 130
cell_size = 4
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
    screen.fill((0, 0, 0))
    
    # Draw the grid
    draw_grid(grid, screen)
    
    # Append population counts to the lists
    wolf_population.append(len(Wolves_list))
    prey_population.append(len(Prey_list))
   
    # Update the display
    pygame.display.flip()

    # Control frame rate (adjust the value as needed)
    clock.tick(10)  # Example: 10 frames per second
    
plt.figure(figsize=(10, 6))
plt.plot(range(len(wolf_population)), wolf_population, label='Wolves')
plt.plot(range(len(prey_population)), prey_population, label='Prey')
plt.xlabel('Time')
plt.ylabel('Population')
plt.legend()
plt.title('Population Changes Over Time')
plt.grid(True)
plt.show()
# Quit Pygame
pygame.quit()


