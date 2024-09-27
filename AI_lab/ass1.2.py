import matplotlib.pyplot as plt
import numpy as np
import heapq
import math


class PathFinder:
    def __init__(self, grid):
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0])

    def heuristic(self, node, goal, method='manhattan'):

        # default
        x1, y1 = node
        x2, y2 = goal

        if method == 'manhattan':
            return abs(x2 - x1) + abs(y2 - y1)
        ### your code here ###
        else:
            return 0

    def aStarGraphSearch(self, start, goal, heuristic_method):
        ### your code here ###
        pass

    def visualize_path(self, path):
        grid = np.array(self.grid)

        plt.figure(figsize=(10, 10))
        plt.imshow(grid, cmap="Greys", origin="upper")

        if path is not None:
            path_x = []
            path_y = []

            for point in path:
                path_x.append(point[0])
                path_y.append(point[1])

            plt.plot(path_x, path_y, marker='o', color='red', linewidth=2, markersize=6, label='Path')

            plt.text(path[0][0], path[0][1], 'Start', color='green', fontsize=12, ha='center', va='center')
            plt.text(path[-1][0], path[-1][1], 'Goal', color='blue', fontsize=12, ha='center', va='center')

            plt.legend()
            plt.xticks(np.arange(grid.shape[1]))
            plt.yticks(np.arange(grid.shape[0]))
            plt.grid(True)
            plt.title("Path Visualization")

            plt.show()
grid = [
    [1, 2, 1, -1, 3, 2, 1],
    [2, -1, 5, -1, 2, 3, 1],
    [1, 1, 1, 1, 5, -1, 1],
    [1, -1, -1, -1, 1, 2, 1],
    [1, 1, 3, 1, 1, 5, 1],
    [1, -1, 1, 1, 2, 1, 1],
    [1, 1, 1, -1, 1, 1, 1]
]

# build class
pathfinder = PathFinder(grid)

# start and goal
start=(0, 0)
goal=(6, 6)

# default heuristics
heuristic = "euclidean"

# find path
graph_path = pathfinder.aStarGraphSearch(start,goal, heuristic)
print(graph_path)

# visualization
pathfinder.visualize_path(graph_path)
