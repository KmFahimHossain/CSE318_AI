

CSE 318 Assignment-02
Solving the Max-cut problem by GRASP
## July 6, 2026
The maximum cut (MAX-CUT) problem
Given an undirected graph G = (V,U ), where V  is the set of vertices and U  is the set of edges, and
weights w
uv
associated  with  each  edge  (u,v) ∈ U .   The Maximum Cut (MAX-CUT)  problem
consists in finding a nonempty proper subset of vertices S ⊂ V  (S ̸= ∅), such that the weight of the
cut (S,
## ̄
S), given by
w(S,
## ̄
## S) =
## X
u∈S, v∈
## ̄
## S
w
uv
## ,
is maximized.
The above figure shows four cuts having different weights on a graph with five nodes and seven
edges.  The maximum cut has S ={1, 2, 4} and
## ̄
S ={3, 5}, with weight w(S,
## ̄
## S) = 50.
Solving a combinatorial optimization problem by GRASP
GRASP (Greedy Randomized Adaptive Search Procedure) is a randomized multistart iterative method
for computing good quality solutions of combinatorial optimization problems.  Each GRASP iteration
is usually made up of:
-  a construction phase, where a feasible solution is constructed, and
-  a local search phase, which starts at the constructed solution and applies iterative improvement
until a locally optimal solution is found.
Typically, the construction phase of GRASP is a semi-greedy or randomized greedy algorithm.
## 1

Algorithm 1 GRASP (Greedy Randomized Adaptive Search Procedure)
1: procedure GRASP(MaxIterations)
2:   for i = 1 to MaxIterations do
3:Build a greedy randomized solution x using semi-greedy heuristic
4:x← LocalSearch(x)
5:if i = 1 then
## 6:x
## ∗
← x
7:else if w(x) > w(x
## ∗
) then
## 8:x
## ∗
← x
9:end if
10:   end for
11:   return x
## ∗
12: end procedure
Randomized Heuristic for the Maximum Cut Problem
The algorithm starts with both partitions X and Y  being empty.  For each vertex v ∈ V , it is placed in
either partition X or Y  uniformly at random, with probability
## 1
## 2
each.  The final cut is determined by
the edges crossing between the two partitions.  To get a reliable estimate of the cut size, the algorithm
is run n times and the results are averaged.
Algorithm 2 Randomized-1 Heuristic for MAX-CUT
1: procedure RandomizedMaxCut(G = (V,E),w,n)
2:totalCutWeight ← 0
3:   for i = 1 to n do
4:Initialize partitions: X ←∅, Y ←∅
5:for all vertex v ∈ V do
6:if  Random choice with probability >=
## 1
## 2
then
7:X ← X ∪{v}
## 8:else
9:Y ← Y ∪{v}
10:end if
11:end for
12:cutWeight ←
## P
(u,v)∈E,u∈X,v∈Y  or u∈Y,v∈X
w
uv
13:totalCutWeight ← totalCutWeight + cutWeight
14:   end for
15:averageCutWeight ←
totalCutWeight
n
16:   return averageCutWeight
17: end procedure
Greedy Heuristic for the Maximum Cut Problem
The algorithm starts by placing one vertex to each partition X and Y  (initially both are empty) such
that each contains an endpoint of the edge with the largest weight.  The remaining |V|− 2 vertices are
then considered one by one.  For each unassigned vertex, it is placed into the partition (X or Y ) where
it contributes the most to the current partial cut.  This placement is done greedily at each iteration.
Semi-greedy Heuristic for the Maximum Cut Problem
A  semi-greedy  heuristic  builds  on  a  greedy  function  by  introducing  randomness  in  the  candidate
selection process.  For each candidate element v, a greedy function is evaluated.  Based on these values,
candidates  are  ranked  and  a Restricted Candidate List (RCL)  is  constructed.   One  element  is  then
randomly selected from the RCL to extend the current partial solution.
## 2

Algorithm 3 Greedy Heuristic for MAX-CUT
1: procedure GreedyMaxCut(G = (V,E),w)
2:Initialize partitions: X ←∅, Y ←∅
3:Find edge (u,v)∈ E with maximum weight w
uv
## 4:   X ← X ∪{u}, Y ← Y ∪{v}
5:   U ← V \{u,v}▷ Unassigned vertices
6:   for all vertex z ∈ U do
7:Compute weight if z ∈ X: w
## X
## =
## P
y∈Y
w
zy
8:Compute weight if z ∈ Y : w
## Y
## =
## P
x∈X
w
zx
9:if w
## X
> w
## Y
then
10:X ← X ∪{z}
## 11:else
12:Y ← Y ∪{z}
13:end if
14:   end for
15:   return partitions X,Y
16: end procedure
There are two primary strategies for building the RCL:
- Cardinality-based method:  Selects the top-k candidates (e.g., k = 5 or k = 10).
- Value-based method:  Selects all candidates v with greedy function value ≥ μ, where
μ = w
min
+ α· (w
max
− w
min
## ),
and α∈ [0, 1] is a tunable parameter.
For the above greedy heuristic, the candidate elements are vertices which are not yet assigned to
set X  and set Y .  Let V
## ′
= V −{X ∪ Y} be the set of all candidate elements.  The cut-off value is
denoted by
μ = w
min
+ α· (w
max
− w
min
## )(1)
where α is a parameter such that 0 ≤ α ≤ 1, and the restricted candidate list consists of all vertices
whose value of the greedy function is greater than or equal to μ.  A vertex is randomly selected from
the restricted candidate list.
For each vertex v, we define
σ
## X
## (v) =
## X
u∈X
w
vu
and  σ
## Y
## (v) =
## X
u∈Y
w
vu
## .
The greedy function value of v is
max{σ
## X
## (v),σ
## Y
## (v)}
However, w
min
and w
max
can be updated using the following naive rules:
w
min
= min
## 
min
v∈V
## ′
σ
## X
(v), min
v∈V
## ′
σ
## Y
## (v)
## 
w
max
= max
## 
max
v∈V
## ′
σ
## X
(v), max
v∈V
## ′
σ
## Y
## (v)
## 
Use equation (1) for determining the placement of the current candidate vertex in X or Y.
Local Search for the Maximum Cut Problem
A simple local search method for the maximum cut problem is described below:
Assume that we have obtained a feasible solution at the end of the construction phase and S,
## ̄
## S
are  two  partitions  of  the  current  solution  (S,
## ̄
S).   The  local  search  phase  is  based  on  the  following
## 3

neighborhood structure.  To each vertex v ∈ V , we associate either the neighbor (S−{v},
## ̄
S∪{v}) if
v ∈ S, or the neighbor (S∪{v},
## ̄
S−{v}) if v ∈
## ̄
## S.
The value
δ(v) =
## (
σ
## S
(v)− σ
## ̄
## S
(v),    if v ∈ S
σ
## ̄
## S
(v)− σ
## S
(v),    if v ∈
## ̄
## S
## (2)
represents the change in the objective function (MAX-CUT value) associated with moving vertex
v from one subset of the cut to the other.  All possible moves are investigated and the best improving
neighbor replaces the current solution.
The local search stops when no improving neighbor is found after evaluation of all possible moves
(we are stuck in a local optima).
## Input Format
The input is provided as a text file with the following structure:
-  The first line contains two integers: n and m, where:
– n is the number of vertices
– m is the number of edges (the size of the graph).
-  Each of the next m lines describes an edge of the graph using three integers:
## V
## 1
## V
## 2
## W
t
## – V
## 1
and V
## 2
are the endpoints of the edge,
## – W
t
is the weight associated with the edge (V
## 1
## ,V
## 2
## ).
The graphs are undirected.
## Benchmark Data Set
The benchmark data set contains 54 input graphs.  For 24 of them, the known best solution or upper
bound is provided in the table below:
ProblemKnown BestProblemKnown BestProblemKnown BestProblemKnown Best
SolutionSolutionSolutionSolution
## G112078G143187G321560G437027
## G212084G153169G331537G447022
## G312077G163172G341541G457020
## G11627G2214123G358000G486000
## G12621G2314129G367996G496000
## G13645G2414131G378009G505988
Table 1:  Known best solutions or upper bounds for selected benchmark instances.
## Task Description
## 1. Algorithm Implementation
You need to implement the algorithms: Greedy, Randomized, Semi-Greedy, Local Search and
GRASP. For each of these algorithms, you are required to record the performance on all 54 bench-
mark graphs.  For the Semi-Greedy algorithm, you need to use the value-based selection method as
described earlier.
## 4

- CSV File Submission
A CSV file named 2205***.csv should be submitted summarizing the results obtained from running
the  different  algorithms  on  the  54  benchmark  graphs  provided.   The  format  of  the  CSV  can  be  as
follows:
For semi-greedy, you may include information regarding value of α.
You should be prepared to regenerate the result for any one algorithm on any one graph during
evaluation.
## 3. Report Submission
Along with the CSV file, you should submit a brief report in PDF format (renamed as 2205***.pdf).
The report should include:
-  A  high-level  description  of  each  algorithm  implemented  (Randomized,  Greedy,  Semi-Greedy,
Local Search, GRASP).
-  Comparison of algorithms (e.g., which algorithm consistently performs better across the bench-
marks).
-  Plots or visualizations that demonstrate how the algorithms perform across different graphs.
An example plot is shown below for reference:
## 5

You do not need to match the exact values as shown in the sample plots—they are included for
illustration only.
## Mark Distribution
TaskMarks
Implementation of Randomized Algorithm10
Implementation of Greedy Algorithm10
Implementation of Semi-Greedy Algorithm20
Implementation of GRASP40
## Report10
Observation from Plots5
## Proper Submission5
## Total100
Table 2:  Mark Distribution for the Assignment
## Submission Format
Create a folder named 2205***.  Place all source files (e.g., code files) inside the folder, and rename
them as your student ID. Include the report as 2205***.pdf, and the result CSV file as 2205***.csv.
Compress the folder into a ZIP file and submit the zip file (2205***.zip) in Moodle.
## Submission Deadline
20 July, Monday, 11:55 pm
## 6