## Problem Statement
The model is a **two-stage stochastic MILP** location-allocation problem.<br>
The problem is formulated as `P-Median model` which makes the location and allocation decisions to **minimize the total system cost**, which are both total travel time of evacuees finding and not finiding shelters.
1. **The first stage** is to identify the shelters to be maintained over time
2.  After a hurricane scenario, **the second stage** is to select the shelters outside the affected zone to prepare to open and allocate evacuees to these shelters.

The model is formulated using the open-source `Pyomo` package, and it is solved using `cbc` solver.


## Assumptions
1. We implement the model in Tehran network consisting of 693 traffic zones, and the centroid of each zone is considered as node.
2. In the first stage, every node can be a candidate for locating shelters.
3. We generate scenrio using the following approach: <br>
- We choose a specific number of zones randomly to be hit by hurricane, and every zones in a predifined vicinity of them are also affected by the hurricane. <br>
- We assume that a specific percetange of population in each affected zone need shelters and are considered as evacuees.
4. Each shelter has predefined capacity for the total number of poeple accomadated in them.
5. It may not be possible to accomadate all the people in a given scenario.
6. There is a maximum value for the number of located shelters.
7. Due to the number of present personnel, only a specific number of shelters can be opened in a given scenario.
8. Shelters in affected zones cannot be opened in each scenario.



## Notations

1. $ l \in L:  Index \space of \space scenarios$
2. $ j \in J:  Index \space of \space candidate \space node \space for \space shelters$
3. $ i \in I:  Index \space of \space nodes \space hit$
------------------------

## Parameters
1. $P$ maximum numbers of shelters can be located 
2. $S$ maximum numbers of shelters can be opened
3. $c_j$ capacity of shelters (thousand people)
4. $ h^l_i$ number of evacuees from node $i$ seeking shelters in scenario $l$
5. $n^l_j$ binary parameters that shows if shelter at site $j$ is safe to be opened in scenario $l$
6. $t_{i,j}$ Travel time between node $i$ and node $j$
7. $p_l$ probability of each scenario
7. $\gamma$ assumed travel time in for the number of people not accommodated in shelters.
----------------------------

## Decision Variables
1. $X_j$ a binary decsion variable to be one if a shelter is located at site $j$ and zero otherwise.
2. $W^l_j$ a binary decision variable to be one if a shelter at site $j$ is openedand used to shelter people in hurricane scenario $l$
3. $Y^l_{i,j}$ a non-negative decision variable to indicate the number of evacuees from origin $i$ that use a shelter at site $j$ in scenario $l$
4. $Z^l_i$ a non-negative decision variable to indicate the number of evacuees from origin $i$ who seek shelters in scenario $l$ but cannot be accommodated.


## Formulation

$\min \quad \gamma \sum_ {l} p_l \sum_ {i} Z^l_i + \sum_ {l} p_l \sum_ {i} \sum_ {j} t_{i,j} Y^l_{i,j}$ 

$\textrm{s.t.} \quad \sum_{j} X_j \leq P $

$ \quad \quad \sum_{j} W^l_j = S \quad \quad \forall l \in L $

$ \quad \quad  W^l_j \leq n^l_j X_j \quad \quad \forall j \in J, \forall l \in L$

$ \quad \quad \sum_{i} Y^l_{i,j} \leq c_j W^l_j \quad \quad \forall j \in J, \forall l \in L $

$ \quad \quad \sum_{j} Y^l_{i,j} \leq h^l_i \quad \quad \forall i \in I, \forall l \in L $

$ \quad \quad \sum_{j} Y^l_{i,j} + Z^l_i =  h^l_i \quad \quad \forall i \in I, \forall l \in L $