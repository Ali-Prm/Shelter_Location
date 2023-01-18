import numpy as np
import pandas as pd 


# We assume that people follow a trial-and-error approach to find shelters. In other words, evacuees travel between shelters in a greedy manner to find the first shelter with capacity. 
# For mdeling such behavior we need to implement the followings:
## 1. Sorted list of each node neighboring candidate based on people's trial-and-error behavior
## 2. Travel time should be recaculated based on people's trial-and-error behavior 


def generate_neighboring_candid(demand, candid, od, set_length):
    """
    Input
    demand : demand data generated using demand_generator.py
    candid: list of candidate node for shelter location
    set_length : length of the set containing neighboring candidate of each node
    od: travel time between nodes of the network

    Output
    Sorted list of each node neighboring candidate based on people's trial-and-error behavior
    """

    # Extracting the list of demand node of the choosen scenario 
    demand_node = {i:[j for j in demand[i].keys()] for i in demand.keys()}

    # Finding the sorted list of safe neighboring candidate for each candidate location based travel time
    mst_nearest_candid = {key:{i:[] for i in candid} for key in demand.keys()}

    for scenario in mst_nearest_candid.keys():      #go over scenario
        for i in candid:                            #go over every candidate 
            for j in od[i].sort_values().index.to_list()[1:]:
                if j in candid:
                    if j not in demand_node[scenario]:
                        mst_nearest_candid[scenario][i].append(j)
                if len(mst_nearest_candid[scenario][i]) == set_length*2:
                    break


    # Finding the sorted list of eligible neighboring candidate for each demand node based on people's trial-and-error behavior 
    ## we use the mst_neareset_candid dictionary generated above for selecting the nearest candidate location at each step 
    nearest_candid = {i: {j:[] for j in demand_node[i]} for i in demand.keys()}

    for scenario in demand.keys(): # go over scenario
        for i in demand_node[scenario]:  # go over every demand node

            # find the first choice for people at each demand node 
            for j in od[i].sort_values().index.to_list():
                if j in candid:
                    if j not in demand_node[scenario]:
                        first_station = j
                        nearest_candid[scenario][i].append(j)
                        break 
            # find the nearest candidate location from candid until the set's length becomes the predefined parameter set_length
            while len(nearest_candid[scenario][i]) <= set_length:
                #print(scenario, i, first_station)
                for z in mst_nearest_candid[scenario][first_station]:
                    # check we don't come back to the previous shelters we were in before 
                    if z not in nearest_candid[scenario][i]:
                        nearest_candid[scenario][i].append(z)
                        first_station = z


    return nearest_candid



def generate_modified_od(demand, candid, nearest_candid, od):
    """
    Input:
    demand : demand data generated using demand_generator.py
    candid : list of candidate node for shelter location
    nearest_candid : sorted list of each node neighboring candidate based on people's trial-and-error behavior
    od : travel time between nodes of the network

    """
    # Extracting the list of demand node of the choosen scenario 
    demand_node = {i:[j for j in demand[i].keys()] for i in demand.keys()}

    # Generating travel time based on people's trial-and-error behavior 
    travel_time = {i: {j:[] for j in demand_node[i]} for i in  demand.keys()}

    for scenario in demand.keys():          # go over scenario
        for node in demand_node[scenario]:  # go over demand nodes 
            candid_list = nearest_candid[scenario][node]
            # recalculate the travel time 
            for i in range(len(candid_list)):
                if i == 0:
                    travel_time[scenario][node].append(od[(node,candid_list[0])])
                else:
                    link_tt = od[(candid_list[i], candid_list[i-1])]
                    new_tt = link_tt + travel_time[scenario][node][i-1]
                    travel_time[scenario][node].append(new_tt)
                
    # coverting the the data type of recalculated travel time into dictionary   
    tt = {i: {} for i in demand.keys()}

    for scenario in demand.keys():          # go over scenarios 
        for node in demand_node[scenario]:  # go over demand nodes
                for i in range(len(nearest_candid[scenario][node])):
                    tt[scenario][(node,nearest_candid[scenario][node][i])] = travel_time[scenario][node][i]
    # Set the travel time between each node and candidate nodes that are not in the its neighboring set a very large value.
    ## we do this because we want to make sure that people only choose candidate in the generated set. 
    for i in candid:
        for scenario in demand.keys():
            for node in demand_node[scenario]:
                if i not in nearest_candid[scenario][node]:
                    tt[scenario][(node,i)] = 100000


    return tt 

