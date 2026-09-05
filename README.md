# UAS-DTU-AStar-Path-Planning
An implementation of the A* path-planning algorithm for four-directional UAV navigation in a 2D obstacle grid

It was created for the **UAS-DTU Avionics Round 2 Task**.

## How It Works

The grid uses the following symbols:

* `S` = Starting position
* `G` = Goal position
* `.` = Free cell
* `#` = Obstacle

The UAV can move only up, down, left and right. Every movement has a cost of `1`.

A* selects the next cell using:

f(n) = g(n) + h(n)

* `g(n)` is the actual cost from the start.
* `h(n)` is the estimated remaining distance.
* `f(n)` is the estimated total path cost.

The program uses **Manhattan distance** as the heuristic:

h(n) = |current row - goal row| + |current column - goal column|

Manhattan distance is suitable because diagonal movement is not allowed.

## Features

* Finds an optimal path from `S` to `G`
* Avoids obstacles
* Detects when no path exists
* Prints the complete ordered path
* Prints path cost, explored nodes and execution time
* Runs nine different test cases
* Generates a separate visualization for every test
* Saves all images inside the `outputs` folder

## Visualization

* White = Free cell
* Black = Obstacle
* Light blue = Explored cell
* Gold = Final path
* `S` = Start
* `G` = Goal

## Requirements

* Python 3
* Matplotlib

## Run the Program

Open a terminal inside the project folder and run:

```bash
python astar2.py
```

The terminal results are also available in:

simulation_log.txt

## Files

astar2.py            - Main Python program
simulation_log.txt   - Results from all test cases
outputs/             - Generated visualization images


## Author 
Aniket Khila
26/A1/068, Delhi Technological University
UAS-DTU Avionics
