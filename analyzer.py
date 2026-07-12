"""
analyzer.py
Performance analyzer class - benchmarks all 4 algorithms on randomly
generated sparse and dense graphs, measuring time and memory.

This satisfies the project's analysis requirements:
  - compare time complexity of algorithms
  - sparse vs dense performance
  - memory consumption
"""

import time
import random
import tracemalloc

from graph import Graph
from algorithms import RouteOptimizer


class PerformanceAnalyzer:
    def __init__(self):
        self.results = []

    def generate_random_graph(self, num_nodes, num_edges):
        """
        Random test graph with num_nodes cities and num_edges roads.
        Sparse: num_edges close to num_nodes. Dense: close to the max
        possible edges (every pair connected).
        """
        g = Graph()
        names = [f"N{i}" for i in range(num_nodes)]
        for name in names:
            g.add_node(name, x=random.uniform(0, 100), y=random.uniform(0, 100))

        # connect everything in a line first so the graph is guaranteed
        # connected (otherwise some algorithms could fail to find a path)
        for i in range(num_nodes - 1):
            g.add_edge(names[i], names[i + 1], random.randint(1, 50))

        edges_added = num_nodes - 1
        max_possible = num_nodes * (num_nodes - 1) // 2
        attempts = 0
        while edges_added < num_edges and edges_added < max_possible and attempts < num_edges * 20:
            c1, c2 = random.sample(names, 2)
            attempts += 1
            if c2 not in g.get_neighbors(c1):
                g.add_edge(c1, c2, random.randint(1, 50))
                edges_added += 1

        return g

    def _measure(self, func, *args):
        tracemalloc.start()
        start_time = time.perf_counter()

        result = func(*args)

        elapsed = time.perf_counter() - start_time
        _, peak_memory = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        return result, elapsed, peak_memory / 1024

    def benchmark_graph(self, graph, label):
        optimizer = RouteOptimizer(graph)
        nodes = graph.get_all_nodes()
        source, target = nodes[0], nodes[-1]

        _, elapsed, mem = self._measure(optimizer.dijkstra, source, target)
        self._record(label, "Dijkstra", graph, elapsed, mem)

        _, elapsed, mem = self._measure(optimizer.astar, source, target)
        self._record(label, "A*", graph, elapsed, mem)

        _, elapsed, mem = self._measure(optimizer.floyd_warshall)
        self._record(label, "Floyd-Warshall", graph, elapsed, mem)

        _, elapsed, mem = self._measure(optimizer.mst_prim)
        self._record(label, "Prim's MST", graph, elapsed, mem)

    def _record(self, label, algo_name, graph, elapsed, mem):
        self.results.append({
            "graph_type": label,
            "algorithm": algo_name,
            "nodes": graph.num_nodes(),
            "edges": graph.num_edges(),
            "time_ms": round(elapsed * 1000, 4),
            "memory_kb": round(mem, 2),
        })

    def print_report(self):
        print("\n" + "=" * 80)
        print(f"{'Graph':<8}{'Algorithm':<18}{'Nodes':<8}{'Edges':<8}{'Time (ms)':<12}{'Memory (KB)':<12}")
        print("=" * 80)
        for r in self.results:
            print(f"{r['graph_type']:<8}{r['algorithm']:<18}{r['nodes']:<8}{r['edges']:<8}"
                  f"{r['time_ms']:<12}{r['memory_kb']:<12}")
        print("=" * 80)

    def run_full_analysis(self, num_nodes=20):
        """Generates one sparse and one dense graph, benchmarks both, prints results."""
        max_edges = num_nodes * (num_nodes - 1) // 2
        sparse_edges = num_nodes
        dense_edges = int(max_edges * 0.7)

        print(f"Generating sparse graph ({num_nodes} nodes, ~{sparse_edges} edges)...")
        sparse_graph = self.generate_random_graph(num_nodes, sparse_edges)
        self.benchmark_graph(sparse_graph, "Sparse")

        print(f"Generating dense graph ({num_nodes} nodes, ~{dense_edges} edges)...")
        dense_graph = self.generate_random_graph(num_nodes, dense_edges)
        self.benchmark_graph(dense_graph, "Dense")

        self.print_report()
