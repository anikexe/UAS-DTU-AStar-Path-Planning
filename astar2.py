import time
import os #for step 8 to make folder
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap


# ---------------------------------------------------------------------------
# STEP 1: Turn the text grid into something Python can work with
# ---------------------------------------------------------------------------

def pad_rows(grid_lines):
    """this will make evry row of same length though in my code i have already kept them the same but 
    just as a security measure, also padding might introduce new routes also, therefore avoided it so 
    i dont get confused"""
    longest = 0
    for line in grid_lines:
        if len(line) > longest:
            longest = len(line)

    padded_lines = []
    for line in grid_lines:
        # ljust adds . dot character on the right until each row has same no of character (basically based on the longest row)
        new_line = line.ljust(longest, '.')
        padded_lines.append(new_line)

    return padded_lines


def read_grid(grid_lines):
    """Turns a list of text rows into a list of lists of single characters
    along with 'S' start and 'G' goal posn are defined here
    """
    grid = []
    start = None
    goal = None

    row_number = 0
    for line in grid_lines:
        row = []
        col_number = 0
        for character in line:
            row.append(character)
            if character == 'S':
                start = (row_number, col_number)
            elif character == 'G':
                goal = (row_number, col_number)
            col_number = col_number + 1
        grid.append(row)
        row_number = row_number + 1

    return grid, start, goal


# ---------------------------------------------------------------------------
# STEP 2: The heuristic (this will guess the remaining distance)
# ---------------------------------------------------------------------------

def heuristic(cell_a, cell_b):
    row1 = cell_a[0]
    col1 = cell_a[1]
    row2 = cell_b[0]
    col2 = cell_b[1]
    return abs(row1 - row2) + abs(col1 - col2)
#this the manhatten distance 
#abs is absolute value to make mod
#Manhattan distance perfectly represents the minimum possible number of four-directional moves when obstacles are ignored.


# ---------------------------------------------------------------------------
# STEP 3: find the neighbours (up, down, left, right)
# ---------------------------------------------------------------------------

def get_neighbors(grid, position):
    row = position[0]
    col = position[1]
    total_rows = len(grid)
    total_cols = len(grid[0])
#this assumes evry row has same length that is why step 1 was to pad the rows

    neighbors = []

    # Check UP
    if row - 1 >= 0:
        if grid[row - 1][col] != '#':
            neighbors.append((row - 1, col))

#if obstacle it is not considered a lable obstacle is = '#' 

    # Check DOWN
    if row + 1 < total_rows:
        if grid[row + 1][col] != '#':
            neighbors.append((row + 1, col))

    # Check LEFT
    if col - 1 >= 0:
        if grid[row][col - 1] != '#':
            neighbors.append((row, col - 1))

    # Check RIGHT
    if col + 1 < total_cols:
        if grid[row][col + 1] != '#':
            neighbors.append((row, col + 1))

    return neighbors


# ---------------------------------------------------------------------------
# STEP 4: Find the entry with the smallest f-score in our "open list"
#          (this is doing the job heapq would normally do for us, but
#          written out in plain loop form so it's easy to follow)
# ---------------------------------------------------------------------------

def find_best_node(open_list):
    best_index = 0
    best_f_score = open_list[0][0]
    #first the complete entry and then the first value inside it

    i = 1
    while i < len(open_list):
        current_f_score = open_list[i][0]
        if current_f_score < best_f_score:
            best_f_score = current_f_score
            best_index = i
            #records index where smallest f score is found
        i = i + 1

    return best_index
#this will return the index with the lowest f score for A*
#due to shortage of time (got viral) used this instead of heapq(yeh alag baat hai confusing tha woh)

# ---------------------------------------------------------------------------
# STEP 5: The A* algorithm itself
# ---------------------------------------------------------------------------

def a_star(grid, start, goal):
    start_time = time.perf_counter()

    # Each entry in open_list is [f_score, position]
    open_list = [[heuristic(start, goal), start]]

    g_score = {}
    g_score[start] = 0

    came_from = {}   # remembers to reach this cell, we came from that cell
    explored = []     # plain list of every cell we actually looked at

    while len(open_list) > 0:

        best_index = find_best_node(open_list)
        best_entry = open_list.pop(best_index)
        current = best_entry[1]

        # to skip if we've already properly explored this cell before
        if current in explored:
            continue

        explored.append(current)

        if current == goal:
            # Walk backwards from goal to start using came_from
            path = [current]
            while path[-1] != start:
                previous_cell = came_from[path[-1]]
                path.append(previous_cell)
            path.reverse()

            time_taken = time.perf_counter() - start_time
            total_cost = g_score[goal]
            return path, total_cost, explored, time_taken

        neighbors = get_neighbors(grid, current)
        for neighbor in neighbors:
            new_cost = g_score[current] + 1

            # only update if it is a NEW cell, or a CHEAPER way to reach it
            if (neighbor not in g_score) or (new_cost < g_score[neighbor]):
                g_score[neighbor] = new_cost
                came_from[neighbor] = current
                f_score = new_cost + heuristic(neighbor, goal)
                open_list.append([f_score, neighbor])

    # If we get here, open_list ran out and we never reached the goal
    time_taken = time.perf_counter() - start_time
    return [], -1, explored, time_taken


# ---------------------------------------------------------------------------
# STEP 6: Draw the grid, explored cells, and final path using matplotlib
# ---------------------------------------------------------------------------

def visualize(grid, start, goal, path, explored, title, filename):
    total_rows = len(grid)
    total_cols = len(grid[0])

    # Build a grid of plain numbers for matplotlib to color:
    # 0 = free cell, 1 = obstacle, 2 = explored cell, 3 = final path cell
    display = []
    row_index = 0
    while row_index < total_rows:
        row_values = []
        col_index = 0
        while col_index < total_cols:
            if grid[row_index][col_index] == '#':
                row_values.append(1)
            else:
                row_values.append(0)
            col_index = col_index + 1
        display.append(row_values)
        row_index = row_index + 1

    for cell in explored:
        r = cell[0]
        c = cell[1]
        if display[r][c] == 0:
            display[r][c] = 2

    for cell in path:
        r = cell[0]
        c = cell[1]
        display[r][c] = 3


    colors = [
        "white",         # 0 = free
        "black",         # 1 = obstacle
        "lightskyblue",  # 2 = explored
        "gold"           # 3 = final path
        ]
    cmap = ListedColormap(colors)

    plt.imshow(
    display,
    cmap=cmap,
    vmin=-0.5,
    vmax=3.5,
    interpolation="nearest"
    )

    plt.title(title)
    ax = plt.gca()
    # Show every row and column number
    ax.set_xticks(range(total_cols))
    ax.set_yticks(range(total_rows))

    # Put minor ticks on cell boundaries
    ax.set_xticks(
    [column - 0.5 for column in range(total_cols + 1)],
    minor=True
    )
    ax.set_yticks(
    [row - 0.5 for row in range(total_rows + 1)],
    minor=True
    )
    # Draw outlines around cells
    ax.grid(
    which="minor",
    color="gray",
    linewidth=0.8
    )
    # Hide the small tick marks
    ax.tick_params(
    which="minor",
    bottom=False,
    left=False
    )
    plt.text(start[1], start[0], "S", ha="center", va="center",
             color="black", fontweight="bold")
    plt.text(goal[1], goal[0], "G", ha="center", va="center",
             color="black", fontweight="bold")
    plt.savefig(filename)
    plt.close()


# ---------------------------------------------------------------------------
# STEP 7: Print the results for one test case, in the format the task asks for
# ---------------------------------------------------------------------------

def print_results(name, path, cost, explored, time_taken, image_file):
    print("----------- " + name + " -----------")
    if len(path) > 0:
        print("Path Found: YES")
        print("Path:")#this will print all the cells we visit 
        for cell in path:
            print(cell)
        print("Total Path Cost:", cost)
    else:
        print("Path Found: NO")
        print("No valid path exists between Start and Goal.")

    print("Nodes Explored:", len(explored))
    print("Execution Time:", time_taken, "seconds")
    print("Visualization saved:", image_file)
    print()


# ---------------------------------------------------------------------------
# STEP 8: Define the test grids and run everything
# ---------------------------------------------------------------------------

# makes a folder 'output' to store the images 
if not os.path.exists("outputs"):
    os.mkdir("outputs")

test_case_1 = [
    "S........",
    "..#.##...",
    "....#.#..",
    ".#..#....",
    ".#.......",
    "....#....",
    "........G",
]

test_case_2 = [
    "S.........",
    "..........",
    "....##....",
    "....##....",
    "..........",
    ".........G",
]

test_case_3 = [
    "S....#####",
    "####.#####",
    "####..####",
    "#####..###",
    "######.###",
    "######..##",
    "#######.G#",
]

test_case_4 = [
    "S.#..#..#.",
    "..#.#.#.#.",
    "..#...#.#.",
    "....#.##..",
    "###.#.###.",
    "....#.....",
    ".####...#G",
]

test_case_5 = [
    "S.........",
    "..........",
    "##########",
    "..........",
    "..........",
    ".........#",
    "........#G",
]

test_case_6 = [
    "SG........",
    "......##..",
    "..#.......",
    ".....#....",
    ".###......",
]

test_case_7 = [
    "S#########",
    ".#########",
    ".#########",
    ".#########",
    ".#########",
    ".#########",
    ".........G",
]

test_case_8 = [
    "S.........",
    "..........",
    "..........",
    "..........",
    "..........",
    ".........G",
]

test_case_9 = [
    "S...#....G",
    "....#.....",
    "....#.....",
    "....#.....",
    "....#.....",
    "....#.....",
    "..........",
]


# A list of (name, grid) pairs -- one per test case
all_test_cases = []
all_test_cases.append(("Test Case 1: Simple Path", test_case_1))
all_test_cases.append(("Test Case 2: Multiple Possible Paths", test_case_2))
all_test_cases.append(("Test Case 3: One Passage Only", test_case_3))
all_test_cases.append(("Test Case 4: Scattered Obstacles", test_case_4))
all_test_cases.append(("Test Case 5: No Valid Path", test_case_5))
all_test_cases.append(("Test Case 6: Adjacent Start and Goal", test_case_6))
all_test_cases.append(("Test Case 7: Path Along Boundary", test_case_7)) #to thoroughly check path conditons 
all_test_cases.append(("Test Case 8: Open Grid", test_case_8))
all_test_cases.append(("Test Case 9: Forced Detour", test_case_9))



case_number = 1
for name, raw_lines in all_test_cases:
    fixed_lines = pad_rows(raw_lines)#corrected grid
    grid, start, goal = read_grid(fixed_lines)

    path, cost, explored, time_taken = a_star(grid, start, goal)

    image_file = f"outputs/testcase_{case_number}.png"
    visualize(grid, start, goal, path, explored, name, image_file)
    print_results(name, path, cost, explored, time_taken, image_file)
    
    case_number = case_number + 1
