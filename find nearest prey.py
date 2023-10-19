# -*- coding: utf-8 -*-
"""
Created on Sun Oct 15 16:29:52 2023

@author: jules
"""

def find_nearest_prey(wolf_instance, prey_list, grid):
    
    nearest_prey = None 
    x, y = wolf_instance.position
    
    for i in range(1,  grid_size):
        for j in range(-i,i + 1):

            for k in range(-i, i + 1):
                
                if j!= 0 or k != 0:
                    
                    if 0 <= (x + j) < grid_size - 1 and 0 <= (y + k) < grid_size - 1 :
                        if grid[x + j][y + k] == 1:
                        
                            nearest_prey = find_prey(x+j, y + k, prey_list)
            
    