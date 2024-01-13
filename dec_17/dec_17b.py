from collections import namedtuple, deque
from typing import Optional

from common_functions import load_input, Grid, print_grid

# Block = namedtuple("Block", "pos val visited prior_direction steps_since_turn")
DIRECTIONS = {"right": (0, 1), "down": (1, 0), "left": (0, -1), "up": (-1, 0)}
ARROWS = {"right": "→", "down": "↓", "left": "←", "up": "↑", "start": "."}


def get_direction(previous: tuple[int, int], current: tuple[int, int]) -> str:
    i = current[0] - previous[0]
    j = current[1] - previous[1]
    return list(DIRECTIONS.keys())[list(DIRECTIONS.values()).index((i, j))]


def dijkstra_search(
    grid: Grid, start: tuple[int, int], goal: tuple[int, int]
) -> (dict, dict):
    frontier = deque()
    frontier.append(start)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0
    while len(frontier) > 0:
        current = frontier.popleft()
        if current == goal:
            break

        for next in grid.get_neighbours(current):
            new_cost = cost_so_far[current] + grid.grid[next]
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                frontier.append(next)
                came_from[next] = current

    return came_from, cost_so_far


def build_path(
    came_from: dict, start: tuple[int, int], dest: tuple[int, int]
) -> list[tuple[int, int]]:
    current = goal
    path = []
    if goal not in came_from:
        return []
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    # path.reverse()
    return path


if __name__ == "__main__":
    data = load_input("example.txt")
    grid = Grid(data)
    grid.print_grid()
    # Cast all values to int
    for item in grid.grid:
        grid.grid[item] = int(grid.grid[item])
    print(grid.grid)
    # This looks like a breadth first search problem? Or a candidate for A*
    # We know our starting position, and we know our goal
    start = (0, 0)
    goal = (len(data) - 1, len(data[0]) - 1)
    print(f"Start pos {start}:{grid.grid[start]}, goal {goal}:{grid.grid[goal]}")
    print_grid(grid.grid)
    came_from, cost = dijkstra_search(grid, start, goal)
    print_grid(came_from)
    print_grid(cost)
    shortest = build_path(came_from, start, goal)
    print(shortest)
    path_cost = 0
    for index, val in enumerate(shortest):
        path_cost += grid.grid[val]
        try:
            grid.grid[val] = ARROWS[get_direction(shortest[index], shortest[index - 1])]
        except ValueError as e:
            print(f"Error: {e}")
    grid.print_grid()
    print(f"Path cost: {path_cost}")
