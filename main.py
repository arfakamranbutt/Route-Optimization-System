"""
main.py
Entry point. Builds a fixed 12 city network and runs a CLI menu
"""

import random

from graph import Graph
from algorithms import RouteOptimizer
from visualizer import Visualizer
from analyzer import PerformanceAnalyzer

def build_sample_graph():
    g = Graph()

    cities = {
        "A": (0, 2),
        "B": (2, 3),
        "C": (4, 2),
        "D": (6, 3),
        "E": (8, 2),
        "F": (10, 2.5),
        "G": (2, 6),    
        "H": (4.5, 7),
        "I": (7, 6),
        "J": (2, -2),   
        "K": (4.5, -3),
        "L": (7, -2),
    }
    for name, (x, y) in cities.items():
        g.add_node(name, x, y)

    roads = [
        ("A", "B", 2), ("B", "C", 2), ("C", "D", 2), ("D", "E", 2), ("E", "F", 2),  # main road
        ("A", "G", 2), ("G", "H", 3), ("H", "I", 2), ("I", "E", 2),                  # decoy branch 1
        ("B", "J", 2), ("J", "K", 2), ("K", "L", 2), ("L", "F", 2),                  # decoy branch 2
    ]
    for c1, c2, w in roads:
        g.add_edge(c1, c2, w)

    return g




def apply_random_traffic(graph):
    traffic_graph = Graph()
    for city in graph.get_all_nodes():
        x, y = graph.coordinates[city]
        traffic_graph.add_node(city, x, y)

    for c1, c2, weight in graph.get_all_edges():
        factor = random.uniform(1.0, 3.0)
        traffic_graph.add_edge(c1, c2, round(weight * factor, 1))

    return traffic_graph


def pick_city(graph, prompt):
    cities = graph.get_all_nodes()
    print(f"\nAvailable cities: {', '.join(cities)}")
    city = input(f"{prompt}: ").strip().upper()
    while city not in cities:
        print("Invalid city name, please check spelling.")
        city = input(f"{prompt}: ").strip().upper()
    return city

def print_menu():
    print("\n" + "=" * 50)
    print("   AI-POWERED ROUTE OPTIMIZATION SYSTEM")
    print("=" * 50)
    print("1. Show city network (visualize)")
    print("2. Find shortest path - Dijkstra")
    print("3. Find shortest path - A* (heuristic)")
    print("4. Compare Dijkstra vs A*")
    print("5. All-pairs shortest path - Floyd-Warshall")
    print("6. Minimum Spanning Tree - Prim's")
    print("7. Simulate traffic + recommend route")
    print("8. Run full performance analysis (sparse vs dense)")
    print("0. Exit")
    print("=" * 50)


def main():
    graph = build_sample_graph()
    optimizer = RouteOptimizer(graph)
    visualizer = Visualizer(graph)

    while True:
        print_menu()
        choice = input("Enter choice: ").strip()

        if choice == "1":
            visualizer.draw_graph(title="City Network")

        elif choice == "2":
            src = pick_city(graph, "Source city")
            dst = pick_city(graph, "Destination city")
            path, cost, explored = optimizer.dijkstra(src, dst)
            if path:
                print(f"\nDijkstra path: {' -> '.join(path)} | Total distance: {cost} | Nodes explored: {explored}")
                visualizer.highlight_path(path, "dijkstra_path.png", f"Dijkstra: {src} to {dst}")
            else:
                print("No path found.")

        elif choice == "3":
            src = pick_city(graph, "Source city")
            dst = pick_city(graph, "Destination city")
            path, cost, explored = optimizer.astar(src, dst)
            if path:
                print(f"\nA* path: {' -> '.join(path)} | Total distance: {cost} | Nodes explored: {explored}")
                visualizer.highlight_path(path, "astar_path.png", f"A*: {src} to {dst}")
            else:
                print("No path found.")

        elif choice == "4":
            src = pick_city(graph, "Source city")
            dst = pick_city(graph, "Destination city")
            d_path, d_cost, d_explored = optimizer.dijkstra(src, dst)
            a_path, a_cost, a_explored = optimizer.astar(src, dst)
            print(f"\nDijkstra: {' -> '.join(d_path)} | Distance: {d_cost} | Explored: {d_explored} nodes")
            print(f"A*:       {' -> '.join(a_path)} | Distance: {a_cost} | Explored: {a_explored} nodes")
            if d_explored > a_explored:
                print(f"\nA* explored {d_explored - a_explored} fewer nodes - its heuristic")
                print("steered the search away from branches that led away from the target.")
            else:
                print("\nBoth explored a similar number of nodes on this graph/route.")

        elif choice == "5":
            dist_table, index = optimizer.floyd_warshall()
            cities = graph.get_all_nodes()
            print(f"\n{'':<6}" + "".join(f"{c:<6}" for c in cities))
            for c1 in cities:
                row = f"{c1:<6}"
                for c2 in cities:
                    row += f"{dist_table[index[c1]][index[c2]]:<6}"
                print(row)

        elif choice == "6":
            mst_edges, total_cost = optimizer.mst_prim()
            print(f"\nMinimum Spanning Tree:")
            for c1, c2, w in mst_edges:
                print(f"  {c1} -- {c2} : {w}")
            print(f"Total cost: {total_cost}")
            visualizer.draw_mst(mst_edges)

        elif choice == "7":
            src = pick_city(graph, "Source city")
            dst = pick_city(graph, "Destination city")
            traffic_graph = apply_random_traffic(graph)
            traffic_optimizer = RouteOptimizer(traffic_graph)

            normal_path, normal_cost, _ = optimizer.dijkstra(src, dst)
            traffic_path, traffic_cost, _ = traffic_optimizer.dijkstra(src, dst)

            print(f"\nNormal route:        {' -> '.join(normal_path)} | {normal_cost}")
            print(f"Traffic-aware route: {' -> '.join(traffic_path)} | {round(traffic_cost, 1)}")
            if normal_path != traffic_path:
                print("-> Traffic changed the recommended route!")
            else:
                print("-> Same route is still best even with traffic.")

        elif choice == "8":
            n = input("Number of cities for test graphs (default 30): ").strip()
            n = int(n) if n else 30
            PerformanceAnalyzer().run_full_analysis(num_nodes=n)

        elif choice == "0":
            print("Goodbye!")
            break

        else:
            print("Invalid choice, try again.")


if __name__ == "__main__":
    main()