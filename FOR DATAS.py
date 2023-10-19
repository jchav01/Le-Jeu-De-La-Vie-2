# -*- coding: utf-8 -*-
"""
Created on Sat Oct 14 23:52:27 2023

@author: jules
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Oct 14 13:10:55 2023

@author: jules
"""

import numpy as np
import random
import matplotlib.pyplot as plt

initial_prey_number = 20
initial_wolves_number = 6
spawn_period = 20
limit_eating = 15
reproduction_threshold = 7
age_death = 60
grid_size = 50
time = 0 
CMAX = 500


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
        
    def move(self, grid):
        x, y = self.position
        possible_moves = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        random_move = random.choice(possible_moves)
        
        x_next, y_next = random_move
        # Check if the random move is available
        if 0 <= random_move[0] < grid_size and 0 <= random_move[1] < grid_size :
            self.position = random_move
        
 
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
    
    

########### WOlVES ROUTINE ####################################################

def reproduction(Wolves_list, grid):
    
    new_wolves = []
    
    for i, wolf1 in enumerate(Wolves_list):
        for wolf2 in Wolves_list[i+1:]:
            if distance(wolf1, wolf2) <= 3 and rep_threshold(wolf1, wolf2) > 0.5 : 
            
                # Generate a new position near the couple of wolves
                x1, y1 = wolf1.position
                x2, y2 = wolf2.position
                possible_positions = [(x1 + 1, y1), (x1 - 1, y1), (x1, y1 + 1), (x1, y1 - 1),
                                      (x2 + 1, y2), (x2 - 1, y2), (x2, y2 + 1), (x2, y2 - 1)]
                
                for new_pos in possible_positions:
                    
                    if not position_taken(new_pos, grid):
                        
                        new_wolf = wolf(new_pos)
                        new_wolves.append(new_wolf)
                        break
                        
                #Reset the reproduction rate to 0
                wolf1.reproduction()
                wolf2.reproduction()
                
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

def Chase(Wolves_list, prey_list):
    for pred in Wolves_list:
        nearest_prey = find_nearest_prey(pred, prey_list)
        if nearest_prey:
            x1, y1 = pred.position
            x2, y2 = nearest_prey.position
            # Calculate the direction to move (2 cases towards the prey)
            dx = 2 if x2 > x1 else -2 if x2 < x1 else 0
            dy = 2 if y2 > y1 else -2 if y2 < y1 else 0
            new_position = (x1 + dx, y1 + dy)
            # Check if the new position is within the grid
            if 0 <= new_position[0] < grid_size and 0 <= new_position[1] < grid_size and not position_taken(new_position,grid):
                pred.move(new_position)


def Eat(Wolves_list, prey_list):
    

    for i, pred in enumerate(Wolves_list):
        for j, prey_instance in enumerate(prey_list):
            if distance(pred, prey_instance) < 3:
                # Mark the prey and wolf for removal
                del prey_list[j]
                pred.eat()
                continue
        
            
    
def check_deaths(Wolves_list):
    
    for i, pred in enumerate(Wolves_list):
        
        if pred.days_without_eating == limit_eating or pred.age > age_death:
            
            del Wolves_list[i]
            


######## PREYS Routine #######################################################

def preys_movement(Prey_list, grid):
    
    for prey in Prey_list:
        
        prey.move(grid)

def add_random_prey(Prey_list, time):
    
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
            new_grid[x][y] = 2  # Update the new grid with new positions of prey
    return new_grid
     
# Create initial grid
grid = update_grid(Wolves_list, Prey_list)




##### UPDATE ##################################################################
    
    
def update(time, grid):
    
    global Wolves_list, Prey_list
    
    # CALL MAIN FUNCTIONS
    for pred in Wolves_list:
        pred.pass_day()
        
    preys_movement(Prey_list, grid)
    add_random_prey(Prey_list, time)
    check_deaths(Wolves_list)
    Eat(Wolves_list, Prey_list)
    reproduction(Wolves_list, grid)
    Chase(Wolves_list, Prey_list)
    
    
    grid = update_grid(Wolves_list, Prey_list)
    
    
    time += 1
    
    return len(Wolves_list), len(Prey_list)

############ SIMULATION #######################################################

def single_simulation(grid_size, initial_prey_number, initial_wolves_number, spawn_period, limit_eating, reproduction_threshold, age_death):
    
    count = 0
    # Data collection
    prey_counts = []
    wolf_counts = []
    
    while count < CMAX:
        
        a, b = update(time, grid)
        wolf_counts.append(a)
        prey_counts.append(b)
        
        count += 1
        
        if count % 100 == 0:
            print("caca")
    
    return wolf_counts, prey_counts

########### MAIN ##############################################################
def main():

   # Run a single simulation
   wolf_counts, prey_counts = single_simulation(grid_size, initial_prey_number, initial_wolves_number, spawn_period, limit_eating, reproduction_threshold, age_death)

   # Visualize population data
   time_steps = range(CMAX)
   plt.plot(time_steps, prey_counts, label='Prey')
   plt.plot(time_steps, wolf_counts, label='Wolves')
   plt.xlabel('Time')
   plt.ylabel('Population Count')
   plt.legend()
   plt.show()

if __name__ == "__main__":
    main()
    
