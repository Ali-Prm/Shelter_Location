## Problem Statement

The problem is formulated as the `P-Median model`, which makes the location and allocation decisions to **minimize the total system cost**, which is both the total travel time of evacuees finding and not finding shelters.
1. Shelter locations are choosed from subset of netowrk's nodes.

- The model is formulated using the open-source `Pyomo` package, and it is solved using `cbc` solver.

-----------------------------------------------------------



## Assumptions
1. We implement the model in the Tehran network consisting of 693 traffic zones, and each zone's centroid is considered a node.
3. We generate a scenario using the following approach: <br>
- We randomly choose a specific number of zones to be hit by a hurricane, and every zone in a predefined vicinity is also affected by the hurricane. <br>
- We assume that a specific percentage of the population in each affected zone needs shelters and are considered evacuees.
4. Each shelter has a predefined capacity for the total number of people accommodated in them.
5. It may not be possible to accommodate all the people in a given scenario.
6. P shelter can be located. 


-----------------------------------------------------------------------


## Notations and Sets 
1. $j \in J:  Index \space of \space candidate \space node \space for \space shelters$
2. $i \in I:  Index \space of \space nodes \space hit$
3. $N_i \subseteq J$: Subset of i's candid neighbor which are sorted based on ascending order of travle time.
4. $N_j \subseteq J$: Subset of j's candid neighbor which are sorted based on ascending order of travel time.


## Parameters
1. $P$ Numbers of shelters can be located 
2. $c_j$ capacity of shelters (thousand people)
3. $h_i$ number of evacuees from node $i$ seeking shelters 
4. $n_j$ binary parameters that shows if shelter at site $j$ is safe to be opened
5. $t_{i,j}$ Travel time between node $i$ and node $j$
6. $\gamma$ assumed travel time for the people not accommodated in shelters.


## Decision Variables
1. $X_j$ a binary decsion variable to be one if a shelter is located at site $j$ and zero otherwise.
2. $Y_{i,j}$ a non-negative decision variable to indicate the number of evacuees from origin $i$ that use a shelter at site $j$
4. $Z_i$ a non-negative decision variable to indicate the number of evacuees from origin $i$ who seek shelters but cannot be accommodated.


## Formulation

$\min \quad \gamma \sum_ {i} Z_i +  \sum_ {i} \sum_ {j} t_{i,j} Y_{i,j}$ 

$\textrm{s.t.} \quad \sum_{j} X_j = P$


$\quad \quad  X_j \leq n_j \quad \quad \forall j \in J$

$\quad \quad \sum_{i} Y_{i,j} \leq c_j X_j \quad \quad \forall j \in J$

$\quad \quad \sum_{j} Y_{i,j} + Z_i =  h_i \quad \quad \forall j \in N_i$

$\quad \quad Y_{i,j_1} >= Y_{i,j_2} \quad \quad \forall i \in I, \quad \forall j \in N_i, \quad (j_1, j_2) \in N_j$
