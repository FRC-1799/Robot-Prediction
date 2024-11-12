import heapq
PREDICTION_SIZE = 20

class AccuracyCheck:
    def __init__(self, robot):
        self.self = self
        self.robot = robot  # our robot's location

    def heuristic(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])  # Manhattan distance

    def astar(self, start, goal, obstacles):
        open_set = []
        heapq.heappush(open_set, (0, start))
        came_from = {}
        g_score = {start: 0}
        f_score = {start: self.heuristic(start, goal)}

        neighborIsObstical = False

        while open_set:
            current = heapq.heappop(open_set)[1]

            if current == goal:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                return path[::-1]  # Return reversed path

            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # 4 possible directions
                neighbor = (current[0] + dx, current[1] + dy)

                # Reset neighborIsObstical for each neighbor
                neighborIsObstical = False

                if (obstacles[0] <= neighbor[0] <= obstacles[0] + PREDICTION_SIZE and
                    obstacles[1] <= neighbor[1] <= obstacles[1] + PREDICTION_SIZE):
                    neighborIsObstical = True

                if neighborIsObstical or not (0 <= neighbor[0] < 800 and 0 <= neighbor[1] < 600):
                    continue  # Skip if it's an obstacle or out of bounds

                tentative_g_score = g_score[current] + 1  # Assume cost between nodes is 1

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, goal)
                    if neighbor not in [i[1] for i in open_set]:
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))

        return []  # Return empty path if no path found