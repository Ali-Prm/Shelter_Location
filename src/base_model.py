import numpy as np 
import pandas as pd 
import pyomo.environ as pyo






def base_model(scenario, demand, od, candidate,
                  max_shelter_num, shelter_cap,
                  gamma):
    """
    Base Model Generator
    Input:
    scenario: Index of the demand scenario
    demand: Dictionary contatining demand data, the demand defined for scenario and node of the network 
    od: Travel time between nodes of the network 
    candidate: List of candidate node for shelter location 
    max_shelter_num: Number of shelters to be located 
    shelter_cap: Capacity of each shelter
    gamma: Assumed travel time for the poeole who not find shelters

    Output:
    A object of the base model 

    """

    # Safe nodes among candidate list that can be choosen for shelter location  
    safe_nodes = {}
    for node in candidate:
        if node in demand[scenario].keys():
            safe_nodes[node] = 0
        else:
            safe_nodes[node] = 1
            

    # List of the demand node based on the index of the scenario    
    demand_node = {i:[] for i in demand.keys()}
    for i in demand.keys():
        for j in demand[i].keys():
            demand_node[i].append(j)

    # Modified version of the OD, which only contain travel time between demand nodes and canidate nodes       
    od_modified = {(x,y):od[x,y] for y in candidate for x in demand_node[scenario]}
    
    # Total demand of the choosen scenario 
    all_demand = 0
    for key in demand[scenario].keys():
        all_demand += demand[scenario][key]
    
    model = pyo.ConcreteModel('base')
    
    
    ######## 1. Sets 
    # demand nodes 
    model.I = pyo.Set(initialize = demand_node[scenario])

    # current station location
    model.J = pyo.Set(initialize = candidate)
    

    
    ######## 2. Decision variables 
    # shelter locations : binary variable 
    model.x = pyo.Var(model.J, within=pyo.Binary)

    # flow variable between demand nodes and shelter locations
    model.y = pyo.Var(model.I, model.J, within=pyo.NonNegativeReals)

    # unresponded demand from each node 
    model.z = pyo.Var(model.I, within=pyo.NonNegativeReals)
    
    
    
    ###### 3. Parameters 
    # maximum number of shelters to be located 
    model.max_located = pyo.Param(initialize=max_shelter_num)

    # capacity of shelters 
    model.capacity = pyo.Param(initialize=shelter_cap)

    # demand 
    model.demand = pyo.Param(model.I, initialize=demand[scenario])

    # safe nodes 
    model.safe_node = pyo.Param(model.J, initialize=safe_nodes)

    # travel time 
    model.tt = pyo.Param(model.I, model.J, initialize=od_modified)

    #  gamma parameter : Assumed travel time for the poeole who not find shelters
    model.gamma = pyo.Param(initialize=gamma)
    
    # total number of demands 
    model.all_demand = pyo.Param(initialize = all_demand)
    
    
    
    ##### 4. Constraints 

    # maximum number of shelters to be located 
    model.cons_max_loc_shelters = pyo.Constraint(expr = sum(model.x[j] for j in model.J) == model.max_located)

    # sheletrs must be located only in safe nodes 
    def safe_shelter(mdl, j):
        return mdl.x[j] <= mdl.safe_node[j]
    model.cons_safe_shelters = pyo.Constraint(model.J, rule=safe_shelter)

    # the total number of people accommodated in the shelter at site j cannot exceed its capacity
    def accom_shelter(mdl, j):
        return sum(mdl.y[i,j] for i in mdl.I) <= mdl.capacity * mdl.x[j]
    model.cons_accom_shelters = pyo.Constraint(model.J, rule=accom_shelter)

    # the number of evacuees from each demand node that could not find shelters 
    def not_accom(mdl, i):
        return sum(mdl.y[i,j] for j in mdl.J) + mdl.z[i] == mdl.demand[i]
    model.cons_not_accom = pyo.Constraint(model.I, rule=not_accom)
    
            
    
    ###### 5. Object function 
    def obj_rule(mdl):
        return (sum(mdl.z[i] for i in mdl.I)*mdl.gamma + sum(mdl.y[i,j]*mdl.tt[i,j] for i in mdl.I for j in mdl.J))/mdl.all_demand
    model.objective = pyo.Objective(rule=obj_rule, sense=pyo.minimize)
    
    return model
    