import math
import heapq

locations = {
    "Pharmacy": (0, 0),
    "Main_Corridor": (2, 1),
    "Patient_Wing": (1, 4),
    "Nursing_Station": (4, 2),
    "Laboratory": (5, 5),
    "Emergency_Ward": (8, 6),
}

hospital_graph = {
    "Pharmacy": {"Main_Corridor": 2.2, "Patient_Wing": 4.1},
    "Main_Corridor": {"Nursing_Station": 2.2},
    "Patient_Wing": {"Laboratory": 5.0},
    "Nursing_Station": {"Laboratory": 3.2, "Emergency_Ward": 6.0},
    "Laboratory": {"Emergency_Ward": 3.2},
    "Emergency_Ward": {},
}


def heuristic(current, goal):
    x1, y1 = locations[current]
    x2, y2 = locations[goal]
    return math.hypot(x1 - x2, y1 - y2)


def reconstruct_path(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    return path[::-1]


def path_cost(path, graph):
    return sum(graph[a][b] for a, b in zip(path, path[1:]))


def gbfs(start, goal, graph=hospital_graph):
    frontier = [(heuristic(start, goal), start)]
    came_from = {}
    queued = {start}
    visited = set()
    order = []
    while frontier:
        _, node = heapq.heappop(frontier)
        if node in visited:
            continue
        visited.add(node)
        order.append(node)
        if node == goal:
            path = reconstruct_path(came_from, node)
            return path, path_cost(path, graph), order
        for neighbor in graph[node]:
            if neighbor not in visited and neighbor not in queued:
                came_from[neighbor] = node
                queued.add(neighbor)
                heapq.heappush(frontier, (heuristic(neighbor, goal), neighbor))
    return None, float("inf"), order


def a_star(start, goal, graph=hospital_graph):
    frontier = [(heuristic(start, goal), start)]
    came_from = {}
    g_cost = {start: 0.0}
    visited = set()
    order = []
    while frontier:
        _, node = heapq.heappop(frontier)
        if node in visited:
            continue
        visited.add(node)
        order.append(node)
        if node == goal:
            path = reconstruct_path(came_from, node)
            return path, g_cost[node], order
        for neighbor, weight in graph[node].items():
            new_g = g_cost[node] + weight
            if new_g < g_cost.get(neighbor, float("inf")):
                g_cost[neighbor] = new_g
                came_from[neighbor] = node
                heapq.heappush(frontier, (new_g + heuristic(neighbor, goal), neighbor))
    return None, float("inf"), order
