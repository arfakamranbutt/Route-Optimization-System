"""
graph.py
Graph class - stores cities and roads. Pure data structure only,
no pathfinding logic here (that's in algorithms.py).
"""

import math


class Graph:
    def __init__(self):
        # adjacency list: { city: { neighbor: weight, ... }, ... }
        self.adjacency_list = {}
        # (x, y) coordinates per city - used only by A*'s heuristic
        self.coordinates = {}

    def add_node(self, name, x=0.0, y=0.0):
        if name not in self.adjacency_list:
            self.adjacency_list[name] = {}
            self.coordinates[name] = (x, y)

    def add_edge(self, city1, city2, weight):
        #Undirected road: works both ways, like a real two-way road.
        self.adjacency_list[city1][city2] = weight
        self.adjacency_list[city2][city1] = weight

    def get_neighbors(self, city):
        return self.adjacency_list.get(city, {})

    def get_weight(self, city1, city2):
        return self.adjacency_list.get(city1, {}).get(city2, float('inf'))

    def get_all_nodes(self):
        return list(self.adjacency_list.keys())

    def get_all_edges(self):
        """Returns each road once as (city1, city2, weight), no duplicates."""
        edges = []
        seen = set()
        for city1 in self.adjacency_list:
            for city2, weight in self.adjacency_list[city1].items():
                edge_key = tuple(sorted([city1, city2]))
                if edge_key not in seen:
                    seen.add(edge_key)
                    edges.append((city1, city2, weight))
        return edges

    def num_nodes(self):
        return len(self.adjacency_list)

    def num_edges(self):
        return len(self.get_all_edges())

    def euclidean_distance(self, city1, city2):
        """Straight-line distance between two cities - the A* heuristic."""
        x1, y1 = self.coordinates[city1]
        x2, y2 = self.coordinates[city2]
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    def __str__(self):
        lines = [f"Graph: {self.num_nodes()} cities, {self.num_edges()} roads"]
        for city in self.adjacency_list:
            neighbors = ", ".join(f"{n}({w})" for n, w in self.adjacency_list[city].items())
            lines.append(f"  {city} -> {neighbors}")
        return "\n".join(lines)
