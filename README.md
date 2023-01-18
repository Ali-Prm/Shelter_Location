## Problem Statement

The problem is formulated as the `P-Median model`, which tries to locate shelters to **minimize the total system cost**, which is both the total travel time of evacuees finding and not finding shelters.

Two models are introduced:
1. The `base` model, which is the regular p-median model, and its underlying assumptions is that people have full information about the capacity of shelters, so they make the best possible decsion. 
2. The `trial-and-error` model, which tries to model the evacuees' trial-and-error behavior in finding shelters. In other words, people go from demand nodes to the nearest shelters and stay at the shelter if it can accommodate them unless they go to the nearest shelter from their current position. They follow this behavior until they can find a shelter with capacity.

- The model is formulated using the open-source `Pyomo` package, and it is solved using `cbc` solver.

-----------------------------------------------------------

## Assumptions
1. We implement the model in the Tehran network consisting of 693 traffic zones, and each zone's centroid is considered a node.
3. We generate a scenario using the following approach: <br>
- We randomly choose a specific number of zones to be hit by a hurricane, and every zone in a predefined vicinity is also affected by the hurricane. <br>
- We assume that a specific percentage of the population in each affected zone needs shelters and are considered evacuees.
4. Each shelter has a predefined capacity.
5. It may not be possible to accommodate all the people in a given scenario.
6. P shelter can be located. 

-----------------------------------------------------------------------

## Base Model 

### Notations and Sets 
1. $j \in J:  Index \space of \space candidate \space node \space for \space shelters$
2. $i \in I:  Index \space of \space demand \space node$


### Parameters
1. $P$ Numbers of shelters can be located 
2. $c_j$ capacity of shelters (thousand people)
3. $h_i$ number of evacuees from node $i$ seeking shelters 
4. $n_j$ binary parameters that shows if shelter at site $j$ is safe to be opened
5. $t_{i,j}$ travel time between node $i$ and node $j$
6. $\gamma$ assumed travel time for the people not accommodated in shelters.


### Decision Variables
1. $X_j$ a binary decsion variable to be one if a shelter is located at site $j$ and zero otherwise.
2. $Y_{i,j}$ a non-negative decision variable to indicate the number of evacuees from origin $i$ that use a shelter at site $j$
4. $Z_i$ a non-negative decision variable to indicate the number of evacuees from origin $i$ who seek shelters but cannot be accommodated.


### Formulation

$\min \quad \gamma \sum_ {i} Z_i +  \sum_ {i} \sum_ {j} t_{i,j} Y_{i,j}$ 

$\textrm{s.t.} \quad \sum_{j} X_j = P$


$\quad \quad  X_j \leq n_j \quad \quad \forall j \in J$

$\quad \quad \sum_{i} Y_{i,j} \leq c_j X_j \quad \quad \forall j \in J$

$\quad \quad \sum_{j} Y_{i,j} + Z_i =  h_i \quad \quad \forall j \in J$


-------------------------------------------------------------------------------

## Trial-and-Error Model

### Notations and Sets 
1. $j \in J$:  Index of candidate node for shelters
2. $i \in I$:  Index of demand node
3. $N_i \subset J$ : Sorted list of each node neighboring candidate based on people's trial-and-error behavior


### Parameters
1. $P$ Numbers of shelters can be located 
2. $c_j$ capacity of shelters (thousand people)
3. $h_i$ number of evacuees from node $i$ seeking shelters 
4. $n_j$ binary parameters that shows if shelter at site $j$ is safe to be opened
5. $tilde{t_{i,j}}$ travel time between demand nodes and candiadate location based on the people's trial-and-error behavior
6. $\gamma$ assumed travel time for the people not accommodated in shelters.


### Decision Variables
1. $X_j$ a binary decsion variable to be one if a shelter is located at site $j$ and zero otherwise.
2. $Y_{i,j}$ a non-negative decision variable to indicate the number of evacuees from origin $i$ that use a shelter at site $j$
4. $Z_i$ a non-negative decision variable to indicate the number of evacuees from origin $i$ who seek shelters but cannot be accommodated.


### Formulation

$\min \quad \gamma \sum_ {i} Z_i +  \sum_ {i} \sum_ {j} tilde{t_{i,j}} Y_{i,j}$ 

$\textrm{s.t.} \quad \sum_{j} X_j = P$


$\quad \quad  X_j \leq n_j \quad \quad \forall j \in J$

$\quad \quad \sum_{i} Y_{i,j} \leq c_j X_j \quad \quad \forall j \in J$

$\quad \quad \sum_{j} Y_{i,j} + Z_i =  h_i \quad \quad \forall j \in N_i$


---------------------------------------------------------------------------------

## Files info:

- The `Result.ipynb` shows the result of two models in 15 different scenarios. 
- The `demand_generator.py` generate demand scenarios. 
- The `network.py` generate the soreted list of neighboring candidate ($N_i$) and the travel time ($t'_{i,j}) used in the trial-and-error model. 
- The `base_model.py` is a function that create an instance of the base model. 
- The `trial_error_model.py` is a function that create an instance of the trial-and-error model. 
- The `data` contains required data for the study. 
- The `doc` elaborates on the trial-and-error model with a toy netwerk. 