"""
algorithms.py
Route Optimizer class - all 4 algorithms live here:
Dijkstra, A*, Floyd-Warshall, Prim's MST.
"""

import heapq


class RouteOptimizer:
    def __init__(self, graph):
        self.graph = graph

    # ------------------------------------------------------------------
    # DIJKSTRA - greedy single-source shortest path, min-heap priority queue
    # Time: O((V + E) log V)   Space: O(V)
    # ------------------------------------------------------------------
    def dijkstra(self, source, target):
        distances = {city: float('inf') for city in self.graph.get_all_nodes()}
        distances[source] = 0
        previous = {city: None for city in self.graph.get_all_nodes()}

        priority_queue = [(0, source)]  # (distance_so_far, city)
        visited = set()
        nodes_explored = 0  # tracked so we can fairly compare against A*

        while priority_queue:
            current_dist, current_city = heapq.heappop(priority_queue)

            if current_city in visited:
                continue  # already finalized with a shorter path
            visited.add(current_city)
            nodes_explored += 1

            if current_city == target:
                break

            for neighbor, weight in self.graph.get_neighbors(current_city).items():
                if neighbor in visited:
                    continue
                new_dist = current_dist + weight
                if new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    previous[neighbor] = current_city
                    heapq.heappush(priority_queue, (new_dist, neighbor))

        path = self._reconstruct_path(previous, source, target)
        return path, distances[target], nodes_explored

    # ------------------------------------------------------------------
    # A* - Dijkstra + heuristic (straight-line distance to target)
    # Time: O((V + E) log V) worst case, fewer nodes explored in practice
    # ------------------------------------------------------------------
    def astar(self, source, target):
        g_score = {city: float('inf') for city in self.graph.get_all_nodes()}
        g_score[source] = 0
        previous = {city: None for city in self.graph.get_all_nodes()}

        h_start = self.graph.euclidean_distance(source, target)
        priority_queue = [(h_start, source)]  # (f_score, city)
        visited = set()
        nodes_explored = 0

        while priority_queue:
            _, current_city = heapq.heappop(priority_queue)

            if current_city in visited:
                continue
            visited.add(current_city)
            nodes_explored += 1

            if current_city == target:
                break

            for neighbor, weight in self.graph.get_neighbors(current_city).items():
                if neighbor in visited:
                    continue
                tentative_g = g_score[current_city] + weight
                if tentative_g < g_score[neighbor]:
                    g_score[neighbor] = tentative_g
                    previous[neighbor] = current_city
                    h = self.graph.euclidean_distance(neighbor, target)
                    heapq.heappush(priority_queue, (tentative_g + h, neighbor))

        path = self._reconstruct_path(previous, source, target)
        return path, g_score[target], nodes_explored

    # ------------------------------------------------------------------
    # FLOYD-WARSHALL - DP all-pairs shortest path
    # dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j]) for every k
    # Time: O(V^3)   Space: O(V^2)
    # ------------------------------------------------------------------
    def floyd_warshall(self):
        nodes = self.graph.get_all_nodes()
        n = len(nodes)
        index = {city: i for i, city in enumerate(nodes)}

        dist = [[float('inf')] * n for _ in range(n)]
        for i in range(n):
            dist[i][i] = 0
        for city1, city2, weight in self.graph.get_all_edges():
            i, j = index[city1], index[city2]
            dist[i][j] = weight
            dist[j][i] = weight

        for k in range(n):
            for i in range(n):
                for j in range(n):
                    if dist[i][k] + dist[k][j] < dist[i][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]

        return dist, index 

    # ------------------------------------------------------------------
    # PRIM'S MST - greedy minimum spanning tree, same heap trick as Dijkstra
    # Time: O(E log V)   Space: O(V)
    # ------------------------------------------------------------------
    def mst_prim(self, start=None):
        nodes = self.graph.get_all_nodes()
        if not nodes:
            return [], 0

        start = start or nodes[0]
        visited = {start}
        edges_heap = []  
        for neighbor, weight in self.graph.get_neighbors(start).items():
            heapq.heappush(edges_heap, (weight, start, neighbor))

        mst_edges = []
        total_cost = 0

        while edges_heap and len(visited) < len(nodes):
            weight, frm, to = heapq.heappop(edges_heap)
            if to in visited:
                continue  

            visited.add(to)
            mst_edges.append((frm, to, weight))
            total_cost += weight

            for neighbor, w in self.graph.get_neighbors(to).items():
                if neighbor not in visited:
                    heapq.heappush(edges_heap, (w, to, neighbor))

        return mst_edges, total_cost

    # ------------------------------------------------------------------
    def _reconstruct_path(self, previous, source, target):
        """Walk backwards from target to source using the previous-city map."""
        path = []
        current = target
        while current is not None:
            path.append(current)
            current = previous[current]
        path.reverse()

        if path[0] != source:
            return []  # target unreachable
        return path