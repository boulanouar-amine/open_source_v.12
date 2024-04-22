import heapq
from collections import defaultdict, deque

class AStar:
    def __init__(self, grid, start, goal):
        self.grid = grid
        self.start = start
        self.goal = goal
        self.open_heap = []
        self.open_set = set()
        self.came_from = {}
        self.g_score = defaultdict(lambda: float('inf'))
        self.f_score = defaultdict(lambda: float('inf'))

    def heuristic(self, a, b):
        (x1, y1), (x2, y2) = a, b
        return abs(x1 - x2) + abs(y1 - y2)  # Manhattan distance

    def neighbors(self, node):
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # 4-way connectivity
        x, y = node
        result = []
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(self.grid) and 0 <= ny < len(self.grid[0]) and not self.grid[nx][ny]:
                result.append((nx, ny))
        return result

    def reconstruct_path(self, current):
        path = deque()
        while current in self.came_from:
            path.appendleft(current)
            current = self.came_from[current]
        return list(path)

    def search(self):
        self.g_score[self.start] = 0
        self.f_score[self.start] = self.heuristic(self.start, self.goal)
        heapq.heappush(self.open_heap, (self.f_score[self.start], self.start))
        self.open_set.add(self.start)

        while self.open_heap:
            current = heapq.heappop(self.open_heap)[1]
            if current == self.goal:
                return self.reconstruct_path(current)

            self.open_set.remove(current)
            for neighbor in self.neighbors(current):
                tentative_g_score = self.g_score[current] + 1
                if tentative_g_score < self.g_score[neighbor]:
                    self.came_from[neighbor] = current
                    self.g_score[neighbor] = tentative_g_score
                    self.f_score[neighbor] = self.g_score[neighbor] + self.heuristic(neighbor, self.goal)
                    if neighbor not in self.open_set:
                        heapq.heappush(self.open_heap, (self.f_score[neighbor], neighbor))
                        self.open_set.add(neighbor)

        return None

# Example usage
grid = [
    [0, 0, 0, 0, 1],
    [0, 1, 1, 0, 0],
    [0, 1, 0, 1, 0],
    [0, 0, 0, 1, 0]
]
start = (0, 0)
goal = (3, 4)

astar = AStar(grid, start, goal)
path = astar.search()
print("Path:", path)
