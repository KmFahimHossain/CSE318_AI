Compared to your previous assignment (A* and search), this is a different branch of AI. You are moving from classical graph search to local search and metaheuristics for optimization.

You should study these topics, in roughly this order.

1. Combinatorial Optimization (Highest Priority)

Understand what optimization problems are.

Topics:

* Optimization vs search
* Feasible solution
* Objective function
* Global optimum
* Local optimum
* NP-hard optimization problems

You should understand why MAX-CUT is hard and why exact algorithms are impractical for large graphs.

Time: 30–45 minutes.

---

2. Local Search Algorithms (Highest Priority)

This is the core new concept.

Study:

* State (a partition of vertices)
* Neighbor
* Neighborhood
* Move operator
* Improvement
* Hill Climbing
* Best-improvement (steepest ascent)
* First-improvement
* Local optimum

Your assignment literally implements hill climbing.

The equation

δ(v)

tells you how much the objective changes if you move one vertex.

If δ(v) > 0

move that vertex.

Repeat until no vertex improves the solution.

This entire section is essentially hill climbing.

Time: 2–3 hours.

---

3. Greedy Algorithms

You already know greedy ideas from A*, but here it is different.

Need to understand

* greedy construction
* incremental solution building
* greedy evaluation function

The greedy function here is

max(σX(v), σY(v))

which measures how attractive a vertex currently is.

Time: 1 hour.

---

4. Randomized Algorithms

Very important.

Study

* Random initialization
* Random sampling
* Multiple independent runs
* Average performance
* Random number generation

Algorithm 2 is just Monte Carlo.

Each run creates a different cut.

Time: 30 minutes.

---

5. Semi-Greedy Construction

This is probably the newest idea.

Understand

Restricted Candidate List (RCL)

Instead of

always picking the best,

you

pick randomly among several good candidates.

Study:

* greedy score
* ranking candidates
* threshold selection
* alpha parameter

The equation

μ = wmin + α(wmax−wmin)

is extremely important.

Need to understand

α = 0

→ everything enters RCL

Very random.

α = 1

→ only best candidate

Almost greedy.

Middle values balance both.

Time: 2 hours.

---

6. GRASP (Most Important)

This is the main algorithm.

Study the entire workflow.

```
repeat

    Construct semi-greedy solution

    Improve using local search

Keep best solution

until enough iterations
```

That's literally all GRASP is.

Construction

↓

Local Search

↓

Repeat

↓

Best solution

Time: 2 hours.

---

7. Graph Representation

Easy.

Need

* adjacency list
* edge list
* weighted graph

You'll repeatedly compute

σX(v)

σY(v)

so efficient graph representation matters.

Time: 30 minutes.

---

8. Complexity Analysis

Not heavily emphasized but useful.

Know roughly

Randomized

O(number of edges)

Greedy

O(VE)

Local Search

depends on iterations

GRASP

iterations × (construction + local search)

---

9. Performance Evaluation

Because you're comparing algorithms.

Need

* average
* maximum
* comparison tables
* plotting

Probably using

matplotlib

and

pandas.

---

10. Parameter Tuning

The only parameter is

α

Understand how

α

changes exploration vs exploitation.

This is a classic AI idea.

Small α

→ exploration

Large α

→ exploitation

---

Topics you do NOT need

No need to study:

* A*
* BFS
* DFS
* UCS
* IDDFS
* Bidirectional search
* Minimax
* Alpha-beta pruning
* CSP
* Bayesian Networks
* MDP
* Reinforcement Learning
* Genetic Algorithms
* Simulated Annealing
* Ant Colony Optimization
* Neural Networks

---

Concept map

```
MAX-CUT
   │
   ├── Objective Function
   │
   ├── Greedy Construction
   │        │
   │        └── Semi-Greedy (RCL + α)
   │
   ├── Randomized Construction
   │
   ├── Local Search
   │       │
   │       └── Hill Climbing
   │
   └── GRASP
          │
          ├── Semi-Greedy
          ├── Local Search
          └── Repeat
```

Study priority (highest to lowest):

1. Local Search / Hill Climbing
2. GRASP
3. Semi-Greedy & Restricted Candidate List (RCL)
4. Greedy Construction
5. Randomized Algorithms
6. MAX-CUT problem formulation
7. Graph representation
8. Performance evaluation and plotting

If you understand the first five topics well, you'll have essentially all the AI concepts needed to implement this assignment. The remaining work is mainly programming and careful implementation of the formulas given in the assignment.
