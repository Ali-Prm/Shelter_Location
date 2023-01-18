import random
import numpy as np
import pandas as pd 


# Scenario Generation
# scenarios are generated randomly. The generation process in explained in the following.
## 1. Initialy we assume that a specific number of nodes are hit by hurricane. Therefore, we randomly select a subset of network nodes.
## 2. Given that hurricane moves, we assume that nodes in the predefined neighboring of the hit ones are also affects by the hurricane.
## 3. We assume that a defined percentage of the populatin in each node need service. 



def demand_generator(data,
                     od,
                     scenario_num,
                     initial_num_hit,
                     vicinity_threshold,
                     percentage_affected):

    """
    Inputs:
    data: data containing the population of network's node
    od : travel time of the network 
    scenario_num: number of scenarios to be generated 
    initial_num_hit: initial number of nodes hit by hurricane
    vicinity_threshhod: the threshold, based on travel time, that indicate the affected nodes in the vicinity of the hit
    percentage_affected: the percentage of the people in the hit and affected nodes who need shelters 

    Output:
    A dictionary containg demand in each scenario
    """

    scenarios = {i:[] for i in range(1,scenario_num+1)}

    # generating the list of the demand nodes
    for i in scenarios.keys():
        locs = random.sample(range(1,693), initial_num_hit)
        for loc in locs:
            scenarios[i].append(loc)
            neigbors = od[od[loc]<vicinity_threshold].index.tolist()
            for j in neigbors:
                scenarios[i].append(j)


    # computing number of evacuees            
    demand = {i:None for i in range(1,scenario_num+1)}
    for i in demand.keys():
        d = data[data['zone'].isin(scenarios[i])]
        demand[i] = dict(zip(d['zone'], d['pop']*percentage_affected))
                
 
            
    return demand 
    