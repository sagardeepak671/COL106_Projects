# COL106 — Data Structures and Algorithms

Five projects, each one an excuse to build a data structure from scratch and then use it to solve a
real problem. **No `dict`, no `set`, no `heapq`, no `sorted()`** where the structure is the point —
the AVL tree, the hash table, the heap and the stack are all implemented by hand in pure Python.

| # | Project | Data structure built | Problem solved |
|---|---|---|---|
| 1 | Pac-Man in Maze World | Stack | Iterative DFS pathfinding with backtracking |
| 2 | Galactic Cargo Management | AVL tree (×3) | Bin packing under four allocation policies |
| 3 | Treasure Quest | Binary heap with custom comparators | Scheduling with deadlines and load balancing |
| 4 | Library Digitalization | Hash set / hash map, static and dynamic | Text indexing and keyword search |
| 5 | Flight Planner | Queue + heap | Three shortest-path variants over a time-constrained graph |

> **COL106 – Data Structures and Algorithms**, IIT Delhi. Each project ships with the original
> problem statement PDF, the provided starter skeleton, and the completed solution.

---

## Table of Contents

- [Environment Setup](#environment-setup)
- [Running](#running)
- [1 — Pac-Man in Maze World](#1--pac-man-in-maze-world)
- [2 — Galactic Cargo Management System](#2--galactic-cargo-management-system)
- [3 — Treasure Quest: The Straw Hat Crew](#3--treasure-quest-the-straw-hat-crew)
- [4 — Library Digitalization](#4--library-digitalization)
- [5 — Flight Planner](#5--flight-planner)
- [Repository Layout](#repository-layout)
- [Contributing](#contributing)

---

## Environment Setup

**Python 3.8+ and nothing else.** No pip install, no virtual environment strictly required — every
project uses only the standard library, and deliberately avoids the parts of it that would do the
work for you.

```bash
python3 --version        # 3.8 or newer
```

If you prefer isolation:

```bash
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
```

<details>
<summary><b>Installing Python</b></summary>

```bash
# Debian / Ubuntu
sudo apt update && sudo apt install -y python3

# macOS
brew install python3

# Windows — python.org installer, or: winget install Python.Python.3.11
```
</details>

---

## Running

Each `*_final/` directory is self-contained. Change into it and run `main.py`:

```bash
cd "1-Pac-Man in Maze World/Ass1_final"
python3 main.py
```

Test cases are defined **inside** `main.py` rather than read from stdin — edit that file to try your
own inputs. Some projects ship additional drivers (`maintester.py`, `bigtest.py`); run them the same
way.

The matching `*_starter/` directory holds the original skeleton, which is useful for diffing to see
exactly what was implemented.

---

## 1 — Pac-Man in Maze World

Navigate a grid maze from start to goal, where `0` is open and `1` is a wall.

**Built:** a `Stack` class (`push`, `pop`, `top`, `empty`) with no reliance on Python list methods
beyond storage.

**Used for:** iterative depth-first search. The stack holds the current path; when a cell has no
unvisited neighbours, it is popped and the search backtracks. Because the path *is* the stack, the
solution falls out of the traversal without a separate reconstruction step.

Raises `PathNotFoundException` when the start or goal is a wall, or when no route exists.

```bash
cd "1-Pac-Man in Maze World/Ass1_final"
python3 main.py
```

| File | Contents |
|---|---|
| `stack.py` | The stack |
| `maze.py` | Grid representation |
| `navigator.py` | `PacMan.find_path` — the DFS |
| `exception.py` | `PathNotFoundException` |

---

## 2 — Galactic Cargo Management System

Cargo objects must be placed into bins under one of four colour-coded allocation policies, with
every operation in `O(log n)`.

**Built:** an `AVLTree` with insertion, deletion, rebalancing, and — the interesting part —
**order-statistic queries**: `lower_bound_node`, `get_maximum_node`, `get_minimum_id_node`,
`get_maximum_id_node`.

**Used for:** the system maintains **three** AVL trees simultaneously —

| Tree | Keyed by | Answers |
|---|---|---|
| `bintree` | remaining capacity | which bins can fit this object |
| `bin_address_tree` | bin ID | what is in a given bin |
| `object_address_tree` | object ID | which bin holds a given object |

The four policies map directly onto tree traversals:

| Colour | Policy | Traversal |
|---|---|---|
| **Green** | Largest remaining capacity | rightmost node |
| **Red** | Largest capacity, smallest ID among ties | rightmost, then min ID |
| **Yellow** | Smallest sufficient capacity, largest ID among ties | `lower_bound`, then max ID |
| **Blue** | Smallest sufficient capacity, smallest ID among ties | `lower_bound`, then min ID |

That is the whole point of the assignment: choosing the right tree keying turns four different
allocation strategies into four different two-line traversals. Raises `NoBinFoundException` when
nothing fits.

```bash
cd "2-Galactic Cargo Management System/Assignment 2 final"
python3 main.py
```

---

## 3 — Treasure Quest: The Straw Hat Crew

Treasures arrive over time, each with a size and a deadline. Assign them to `m` crewmates so that
processing respects arrival times and finishes as early as possible.

**Built:** a `Heap` class parameterised by an arbitrary **comparator function**, so the same code
backs two differently ordered priority queues.

**Used for:**

- `comp2` orders crewmates by `load + latest_entry` — the least-loaded crewmate is always at the
  root, so assignment is `O(log m)`.
- `comp1` orders treasures by `-(arrival_time) - size`, breaking ties by ID — this yields the
  processing order that minimises completion time.

Passing the comparator into the heap rather than hard-coding `<` is what makes one implementation
serve both roles. Ships with eight treasury test cases plus heap unit tests and expected outputs.

```bash
cd "3-Treasure Quest The Straw Hat Crew/Assignment 3 final"
python3 main.py
python3 bigtest.py            # stress test
diff <(python3 main.py) expected_output.txt
```

---

## 4 — Library Digitalization

Index a collection of books and support distinct-word queries and keyword search — three times,
with three different structures, so the trade-offs are visible.

| Library | Structure | Characteristics |
|---|---|---|
| `MuskLibrary` | Sorted arrays via hand-written **merge sort** | `O(n log n)` build, no hashing, deterministic |
| `JGBLibrary` (static) | `HashSet` / `HashMap` with a fixed table | Fast until the table fills |
| `JGBLibrary` (dynamic) | `DynamicHashSet` / `DynamicHashMap` | **Rehashes when load factor ≥ 0.5** |

**Built:**

- `HashSet` and `HashMap` supporting three collision strategies — **chaining**, **linear probing**,
  and **double hashing** — selectable at construction
- A polynomial string hash `h(name, z, table_size)` and a second hash `h2(name, z2, c2)` for double
  hashing
- `prime_generator.get_next_size()` so the table always grows to a prime
- `rehash()`, which reinserts every element into the larger table — the reason amortised insertion
  stays `O(1)`

The three implementations share one interface (`distinct_words`, `count_distinct_words`,
`search_keyword`, `print_books`), so you can measure them against each other directly.

```bash
cd "4-Library Digitalization/Ass4_final"
python3 main.py
```

---

## 5 — Flight Planner

Given a set of flights with departure time, arrival time, and fare, answer three different "best
route" questions between two cities within a time window — with a 20-minute minimum connection time.

| Query | Objective | Algorithm |
|---|---|---|
| `least_flights_earliest_route` | Fewest hops; earliest arrival among those | **BFS** over the flight graph |
| `cheapest_route` | Minimum total fare | **Dijkstra** with a hand-built min-heap |
| `least_flights_cheapest_route` | Fewest hops first, then cheapest | Layered BFS + Dijkstra |

**Built:** `Que.py` (queue for BFS) and `heap.py` (comparator-driven min-heap for Dijkstra).

The modelling decision that makes this work: nodes are **flights**, not cities. A city node cannot
express "you arrived at 14:00, so the 13:50 departure is unreachable"; a flight node can. Paths are
recovered by backtracking through parent pointers stored per flight.

```bash
cd "5-Flight Planner/Ass5_final"
python3 main.py
python3 maintester.py         # also: maintester2.py, maintester3.py
diff output.txt model_output.txt
```

`flights.txt` is the small dataset; `fli1000.txt` is a 1,000-flight stress test.

---

## Repository Layout

```
.
├── 1-Pac-Man in Maze World/
│   ├── Ass1_final/{main,maze,navigator,stack,exception}.py
│   ├── Ass1_starter/
│   └── COL106_Assignment_1.pdf
│
├── 2-Galactic Cargo Management System/
│   ├── Assignment 2 final/{main,gcms,avl,bin,node,object,exceptions}.py
│   ├── Ass2_starter/
│   └── COL106_Assignment_2.pdf
│
├── 3-Treasure Quest The Straw Hat Crew/
│   ├── Assignment 3 final/{main,straw_hat,heap,crewmate,treasure}.py
│   │                      + tc_treasury1-8.txt, tc_heap1.txt, expected_output.txt
│   ├── Ass3_starter/
│   └── COL106_A3_v5.pdf
│
├── 4-Library Digitalization/
│   ├── Ass4_final/{main,library,hash_table,dynamic_hash_table,prime_generator}.py
│   ├── Ass4_starter/
│   └── assignment_4.pdf
│
├── 5-Flight Planner/
│   ├── Ass5_final/{main,planner,flight,heap,Que}.py + maintester*.py, flights.txt, fli1000.txt
│   ├── Ass5_starter/
│   └── COL106_A5.pdf
│
├── How_to_run.txt
└── README.md
```

---

## Contributing

This is coursework, but the structures are clean enough to reuse. Useful improvements:

- Replace the in-file test cases with `pytest` suites and CLI argument parsing
- Add complexity assertions — benchmark AVL and hash operations against their claimed bounds
- Add type hints throughout (project 1 has them; the rest do not)
- Visualise the AVL rebalancing and the hash-table rehash for teaching
- Benchmark project 4's three library implementations on a large corpus and chart the results

```bash
git checkout -b feat/your-change
cd "5-Flight Planner/Ass5_final" && python3 main.py && diff output.txt model_output.txt
git commit -m "feat: describe your change"
```

Please keep solutions dependency-free — using a library structure where the assignment asks you to
build one defeats the purpose.

---

## License

Released for educational use. Problem statements belong to their original authors.
