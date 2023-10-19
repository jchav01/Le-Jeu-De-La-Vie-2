# -*- coding: utf-8 -*-
"""
Created on Sat Oct 14 14:44:41 2023

@author: jules
"""

import numpy as np
import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.colors as mcolors
import time

# Paramètres
grid_size = 50
initial_prey_number = 25
initial_wolves_number = 10

############# CLASSES #########################################################

class prey:
    def __init__(self, position):
        self.position = position
        
    def move(self):
        x, y = self.position
        possible_moves = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        random_move = random.choice(possible_moves)
        # Check if the random move is within the grid boundaries
        if 0 <= random_move[0] < grid_size and 0 <= random_move[1] < grid_size:
            self.position = random_move
            
            

############# INITIALISATION ##################################################

Prey_list = []
for _ in range(initial_prey_number):
    position = (random.randint(0, grid_size - 1), random.randint(0, grid_size - 1))
    prey_instance = prey(position)
    Prey_list.append(prey_instance)


# Create the grid
grid = [[0 for _ in range(grid_size)] for _ in range(grid_size)]

# Initialize the grid with wolves and rabbits
for prey in Prey_list:
    x, y = prey.position
    grid[x][y] = 1  # 1 represents a rabbit
    
######## FUNCTIONS ############################################################

def preys_movement(Prey_list):
    
    for prey in Prey_list:
        
        prey.move()


##### UPDATE ##################################################################

def update(step):
    global Prey_list
    preys_movement(Prey_list)
    
    # Create a new empty grid with white cells
    new_grid = [[0 for _ in range(grid_size)] for _ in range(grid_size)]
    
    for prey in Prey_list:
        x, y = prey.position
        if 0 <= x < grid_size and 0 <= y < grid_size:
            new_grid[x][y] = 1  # Update the new grid with new positions of prey

    im = ax.imshow(new_grid, cmap=cmap, animated=True)
    text.set_text('Time Step: {}'.format(step))
    return im, text

############ AFFICHAGE ########################################################
cmap = mcolors.ListedColormap(['white', 'green', 'red'])

# Create the figure and axes
fig, ax = plt.subplots()
ims = []

# Create a text annotation to display the time step
text = ax.text(0.02, 0.95, '', transform=ax.transAxes, color='white')

# Create the animation
for step in range(100):
    im, text = update(step)
    ims.append([im, text])
    plt.pause(1.5)  # Pause for 0.5 seconds between steps

ani = animation.ArtistAnimation(fig, ims, interval=200, blit=True)

plt.show()