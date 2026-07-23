## CSE 318: Offline 1 

## **Solve N-Puzzle** 

**Objective:** Write a program to solve the n-puzzle problem using the A* search algorithm, where 

**==> picture [141 x 14] intentionally omitted <==**

## **Problem Description:** 

From the early days of artificial intelligence, the _n-puzzle_ has served as a classic benchmark problem. It requires a degree of intelligent reasoning to find an optimal solution. The n-puzzle was invented and popularized in the 1870s by Noyes Palmer Chapman, a postmaster from Canastota, New York. 

The game is played on a _k × k_ grid containing _n_ = _k_[2] _−_ 1 square tiles labeled from 1 to _n_ and a single blank square. The objective is to arrange the tiles in numerical order with the blank tile in the last position, using as few moves as possible. Players may slide any adjacent tile horizontally or vertically into the blank space, thereby changing the configuration of the board. The challenge lies in determining the shortest sequence of such legal moves that transforms an initial configuration into the goal configuration. 

**==> picture [435 x 72] intentionally omitted <==**

## **Solving the N-Puzzle Using A* Search** 

To solve the n-puzzle problem efficiently, we use the **A* search algorithm** , which finds the shortest sequence of moves from the initial configuration to the goal state. 

In this approach, each _search node_ represents 

- The current board configuration 

- A move count (priority value) 

- A reference to the previous search node 

The algorithm begins by inserting the **initial node** (initial board, 0 moves, and null previous node) into a **priority queue** , often called the _open list_ . 

The main loop of the algorithm works as follows: 

1. Remove the node with the **lowest priority value** from the priority queue (this is the most promising node). 

1 

2. Add it to the _closed list_ . 

3. Generate all valid neighboring board configurations (reachable by one legal move). 

4. For each neighbor not in the closed list, insert it into the priority queue. 

This process repeats until the goal board is dequeued from the priority queue. At that point, the algorithm has found an optimal solution. 

The key component of A* is its **priority function** : 

**==> picture [99 x 13] intentionally omitted <==**

Where: 

- _g_ ( _n_ ): The cost to reach node _n_ from the start (i.e., number of moves made so far) 

- _h_ ( _n_ ): A heuristic estimate of the cost to reach the goal from node _n_ 

## **Heuristic Functions** 

To guide the A* search algorithm effectively, we use heuristic functions that estimate the cost from a given state to the goal state. The better (more accurate and admissible) the heuristic, the fewer nodes the algorithm needs to explore. 

1. **Hamming Distance** : Counts the number of tiles that are not in their goal position. The blank tile is not included in this count. 

2. **Manhattan Distance** : Calculates the sum of the vertical and horizontal distances each tile must move to reach its goal position. This is one of the most commonly used admissible heuristics for the n-puzzle. 

3. **Euclidean Distance** : Computes the straight-line distance from each tile’s current position to its goal position, based on the Euclidean formula: 

**==> picture [195 x 22] intentionally omitted <==**

4. **Linear Conflict** : A more informed heuristic that enhances Manhattan distance by considering pairs of tiles that are in the correct row or column but in the wrong order. 

Two tiles _tj_ and _tk_ are said to be in _linear conflict_ if: 

- They are in the same line (row or column), 

- Their goal positions are also in that line, 

- Tile _tj_ is to the right (or below) of _tk_ in the current state, 

- But the goal position of _tj_ is to the left (or above) the goal position of _tk_ . 

In such cases, at least one of the tiles must move out of the way to allow the other to pass, resulting in at least two additional moves. The linear conflict heuristic is calculated as: 

- _h_ ( _n_ ) = Manhattan Distance + 2 _×_ (Number of Linear Conflicts) 

2 

5. **Custom Heuristic:** Design and implement your own admissible heuristic function distinct from the four provided above. You may combine existing strategies or formulate a novel approach. 

Let us assume that our initial board is 

**==> picture [53 x 52] intentionally omitted <==**

**----- Start of picture text -----**<br>
7 2 4<br>6 5<br>8 3 1<br>**----- End of picture text -----**<br>


Our goal board is 

**==> picture [53 x 53] intentionally omitted <==**

**----- Start of picture text -----**<br>
1 2 3<br>4 5 6<br>7 8<br>**----- End of picture text -----**<br>


From the following table we can calculate Hamming distance = **7** 

|Digits|1<br>2<br>3<br>4<br>5<br>6<br>7<br>8|
|---|---|
|Is placed correctly (1 = no, 0 = yes)|1<br>0<br>1<br>1<br>1<br>1<br>1<br>1|



From the following table we can calculate Manhattan distance = **16** 

|Digits|1<br>2<br>3<br>4<br>5<br>6<br>7<br>8|
|---|---|
|Row distance<br>Column distance|2<br>0<br>2<br>1<br>0<br>0<br>2<br>0<br>2<br>0<br>1<br>2<br>1<br>2<br>0<br>1|
|Total distance|4<br>0<br>3<br>3<br>1<br>2<br>2<br>1|



From the following table we can calculate Euclidean distance = **13.30** 

|Digits|1<br>2<br>3<br>4<br>5<br>6<br>7<br>8<br><br><br>|
|---|---|
|Distance<br>Value (approx)|~~_√_~~<br>8<br>0<br>~~_√_~~<br>5<br>~~_√_~~<br>5<br>1<br>2<br>2<br>1<br>2_._828<br>0<br>2_._236<br>2_._236<br>1<br>2<br>2<br>1|



Linear conflict count = **1 (in 2nd row)** So, Linear Conflict heuristic = **Manhattan distance + 2 × 1 = 18** 

## **Detecting Unsolvable Puzzles** 

Not all initial board configurations of the n-puzzle can be solved. That is, not every arrangement of tiles can be transformed into the goal state using legal moves. For example, the following board is unsolvable: 

3 

|8|1|2|
|---|---|---|
||4|3|
|7|6|5|



This happens because the set of all possible board states can be divided into two **equivalence classes** those that can reach the goal state, and those that cannot. Whether a board belongs to the solvable or unsolvable class can be determined by computing the number of **inversions** in the board. 

**Inversion:** An inversion is a pair of tiles ( _i, j_ ) such that _i < j_ but tile _i_ appears _after_ tile _j_ in the board’s row-major ordering (i.e., reading rows left to right, top to bottom). The blank tile is ignored. 

|1|2|3|||1|3|
|---|---|---|---|---|---|---|
||4|6||4|2|5|
|8|5|7||7|8|6|



**row-major order:** 1 2 3 4 6 8 5 7 **3 inversions:** 6-5, 8-5, 8-7 

**row-major order:** 1 3 4 2 5 7 8 6 **4 inversions:** 3-2, 4-2, 7-6, 8-6 

The rules for solvability depend on the size of the grid: 

- **If** _k_ **is odd** (e.g., 3×3 grid): The puzzle is solvable if the total number of inversions is **even** . 

- **If** _k_ **is even** (e.g., 4×4 grid): Let the row of the blank tile be counted from the _bottom_ (starting from 1). The puzzle is solvable if: 

   - The blank is on an even row from the bottom **and** the number of inversions is odd, or 

   - The blank is on an odd row from the bottom **and** the number of inversions is even. 

For all other cases, the puzzle is unsolvable. 

## **Additional Resources** 

- **Is the given puzzle solvable? (1 to 9)** 

- **Is the given puzzle solvable? (1 to 15)** 

- **Visualizing N-Puzzle** 

4 

## **Tasks** 

1. Implement the A* search algorithm using the heuristic algorithms. Your implementation should allow the user to easily switch between heuristics without modifying the core A* algorithm. Aim for modular, extensible code where heuristic logic is separated from the search logic. Your program should take the following inputs: 

   - Grid size _k_ 

   - Initial board configuration (use 0 to represent the blank tile) 

2. Determine whether the input board configuration is solvable. If it is solvable: 

   - Output the optimal cost to reach the goal state and the sequence of board configurations representing each step. 

3. To explore the trade-off between computational efficiency and solution optimality, modify your algorithm to implement **Weighted** _A[∗]_ . Update your priority function to: 

_f_ ( _n_ ) = _g_ ( _n_ ) + _W · h_ ( _n_ ) 

where _W ≥_ 1 _._ 0 is a configurable weight parameter. 

- Generate at least ten distinct, _solvable_ 4 _×_ 4 puzzle configurations. 

- Run your search on each of these generated configurations using _W ∈{_ 1 _._ 0 _,_ 1 _._ 2 _,_ 2 _._ 0 _,_ 5 _._ 0 _}_ . 

- Submit a PDF with a metrics table (comparing nodes explored and solution cost across the different _W_ values for each test case). 

5 

## **Input and output formats** 

The input and output format for a board is the board size N, followed by the N-by-N initial board, with 0 representing the blank square. 

|**Input**|**Output**|
|---|---|
|3<br>0 1 3<br>4 2 5<br>7 8 6|Minimum number of moves = 4<br>0 1 3<br>4 2 5<br>7 8 6<br>1 0 3<br>4 2 5<br>7 8 6<br>1 2 3<br>4 0 5<br>7 8 6<br>1 2 3<br>4 5 0<br>7 8 6<br>1 2 3<br>4 5 6<br>7 8 0|
|3<br>1 2 3<br>0 4 6<br>7 5 8|Minimum number of moves = 3<br>1 2 3<br>0 4 6<br>7 5 8<br>1 2 3<br>4 0 6<br>7 5 8<br>1 2 3<br>4 5 6<br>7 0 8<br>1 2 3<br>4 5 6<br>7 8 0|



6 

|3<br>1 2 3<br>4 5 6<br>8 7 0|Unsolvable puzzle|
|---|---|
|4<br>1 10 7 11<br>6 9 14 2<br>13 12 4 3<br>15 5 8 0|Minimum number of moves = 44|
|‘||



## **Submission Deadline** 

## **06 July, Monday, 11:55 PM** 

7 

