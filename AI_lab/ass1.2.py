from datetime import datetime

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
        if method == 'Euclidean':
            return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
        else:
            return 0

    def aStarGraphSearch(self, start, goal, heuristic_method):
        queue = []
        heapq.heappush(queue, (0, start))  # 初始成本为0，起始节点入队

        # 用于记录每个节点的访问状态和到达该节点的成本
        self.visited = set()
        costs = {start: 0}  # 记录每个节点的最小成本
        parent_map = {start: None}  # 记录路径所需的父节点信息

        while queue:
            current_cost, current = heapq.heappop(queue)  # 取得最小成本的节点

            # 检查当前节点是否为目标节点
            if current == goal:
                path = []  # 初始化路径
                while current is not None:  # 通过parent_map构建路径
                    path.append(current)
                    current = parent_map[current]
                path.reverse()  # 反转路径以便从起点到终点
                return path  # 返回从起点到终点的路径

            # 标记当前节点为已访问
            self.visited.add(current)

            # 获取当前节点的邻居位置
            directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]

            for direction in directions:
                new_row = current[0] + direction[0]
                new_col = current[1] + direction[1]
                new_position = (new_row, new_col)

                # 检查新位置是否合法
                if (0 <= new_row < self.rows and
                        0 <= new_col < self.cols and
                        new_position not in self.visited and
                        self.grid[new_row][new_col] != -1):  # 确保不是障碍物

                    # 计算到达新位置的总代价
                    new_cost = current_cost + self.grid[new_row][new_col]+self.heuristic(new_position,goal,heuristic_method)

                    # 如果新位置未被访问过，或找到更低成本，则更新
                    if new_position not in costs or new_cost < costs[new_position]:
                        costs[new_position] = new_cost  # 更新成本
                        parent_map[new_position] = current  # 设置父节点
                        heapq.heappush(queue, (new_cost, new_position))  # 入队
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
start_time = datetime.now()
# find path
graph_path = pathfinder.aStarGraphSearch(start,goal, heuristic)

print(graph_path)

# visualization
pathfinder.visualize_path(graph_path)
end_time = datetime.now()
print(f"运行时间: {end_time - start_time} 秒")
