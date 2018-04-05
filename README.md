# Satellite Scheduling Problem
## Author: Tan Ren Jie
## Dated: 18 Dec 2016
Effcient satellite mission planning has always been a key aspect of the Ground Operations. <br>
The task of satellite mission planning has always been placed onto a human operator to plan accurately and effciently to meet all of the requirements provided. <br>
This manual tasking is tedious and reuires high level of meticulosity <br>
An automatic satellite scheduler can use Search Algorithms to optimize and quicken this process

# Problem Formulation
The scheduling problem of an earth observation satellite is a large and diffcult combinatorial optimization problem. <br>
Thankfully, such a scheduling problem is well-studied with numerous papers stating different problem formulations. <br>
Some notable formulations are the generalized knapsack formulation, which is well-known to be NP-hard, adopted in [2]. <br>
In [3], it discusses the possibility of using linear integer programming formulation with CPLEX or as a constraint satisfaction problem formulation. <br>
For this demostration, we shall adopt a Constraint-Optimization Problem (COP) formulation using Object Oriented Programming(OOP). <br>

COP refers to a set of problems that requires the optimization of an objective function with respect to some variables in the presence of constraints on those variables. <br>

# Object Used
- Let $R$ be a given set of imaging missions to be taken in the specifed scenario time window
- Let $U$ be a given set of satellites available in the specified scenario time window
- Let $r_i$ represent the $i^{th}$ imaging mission in $R$ and $r$ be the total number of imaging missions in $R$
- Let $u_i$ represent the $i^{th}$ satellite in $U$ and $u$ be the total number of satellites in $U$

<br>
- Let $O$ be a derived set of imaging opportunities for all the imaging missions in $R$ by all the satellites in $U$ after constraint propagation
- Let $o_{i}$ represent the $i^{th}$ imaging opportunity in $O$ and $o$ be the total number of imaging opporunities in $O$
- Let $p_{m,n}$ be the total number of imaging opporunities for the $m^{th}$ imaging mission in $R$ and the $n^{th}$ satellite in $U$ after constraint propagation

<br>
The size of the search space is given by,
$$search space size = 2^{o}$$
where a simple relation between $o$, $r$ and $u$ can be represented as such,
$$o = \sum_r o_i$$
$$=\sum^r_{m=1} \sum^u_{n=1} p_{m,n}$$

<br>
<img src="classhiearchy.jpg" alt="class hierarchy" style="width: 100px;"/>

# Algorithm
<img src="algorithm.png" alt="algo" style="width: 100px;"/>

## Objective function
$$Score_i = k_a a_i + k_b b_i + k_c c_i + k_d d_i + k_e e_i$$


# References
[1] John L. Mohammed. Spacecaps: Automated mission planning for the techsat 21 formation-
ying cluster experiment. FLAIRS-02 Proceedings, 2002. <br>
[2] Jin-Kao Hao Michel Vasquez. A \logic-constrained" knapsack formulation and a tabu al-
gorithm for the daily photograph scheduling of an earth observation satellite. Journal of
Computational Optimization and Applications, 2000. <br>
[3] J.C. Agnese N.Bataille D. Blumstein E. Bensana, G. Verfaillie. Exact and inexact methods
for the daily management of an earth observation satellite. European Space Agency, 1996. <br>
