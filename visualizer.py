"""
visualizer.py
Visualizer class - draws the graph, highlights paths, draws the MST.
Uses networkx only for layout/drawing, never for solving anything.
"""

import os
import networkx as nx
import matplotlib.pyplot as plt


class Visualizer:
    def __init__(self, graph, output_dir="output"):
        self.graph = graph
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def _build_networkx_graph(self):
        G = nx.Graph()
        for city in self.graph.get_all_nodes():
            G.add_node(city)
        for c1, c2, weight in self.graph.get_all_edges():
            G.add_edge(c1, c2, weight=weight)
        return G

    def _get_positions(self, G):
        """
        Use the graph's own (x, y) coordinates to position each city,
        so the layout is consistent and predictable every time (not a
        different random shape on every run).
        """
        return {city: self.graph.coordinates[city] for city in G.nodes()}

    def draw_graph(self, filename="graph.png", title="City Network"):
        G = self._build_networkx_graph()
        pos = self._get_positions(G)

        plt.figure(figsize=(10, 7))
        nx.draw(G, pos, with_labels=True, node_color="lightblue",
                node_size=800, font_size=9, font_weight="bold")
        edge_labels = nx.get_edge_attributes(G, "weight")
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

        plt.title(title)
        path = os.path.join(self.output_dir, filename)
        plt.savefig(path, dpi=150, bbox_inches="tight")
        plt.close()
        print(f"Saved: {path}")
        return path

    def highlight_path(self, path, filename="path.png", title="Shortest Path"):
        """Draws the full graph in gray, with the given path highlighted in red."""
        G = self._build_networkx_graph()
        pos = self._get_positions(G)

        plt.figure(figsize=(10, 7))
        nx.draw(G, pos, with_labels=True, node_color="lightgray",
                node_size=800, font_size=9, edge_color="lightgray")

        if path and len(path) > 1:
            path_edges = list(zip(path, path[1:]))
            nx.draw_networkx_nodes(G, pos, nodelist=path, node_color="orange", node_size=800)
            nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color="red", width=3)

        edge_labels = nx.get_edge_attributes(G, "weight")
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

        plt.title(title)
        out_path = os.path.join(self.output_dir, filename)
        plt.savefig(out_path, dpi=150, bbox_inches="tight")
        plt.close()
        print(f"Saved: {out_path}")
        return out_path

    def draw_mst(self, mst_edges, filename="mst.png", title="Minimum Spanning Tree"):
        """Draws the full graph in gray, with MST roads highlighted in green."""
        G = self._build_networkx_graph()
        pos = self._get_positions(G)

        plt.figure(figsize=(10, 7))
        nx.draw(G, pos, with_labels=True, node_color="lightgray",
                node_size=800, font_size=9, edge_color="lightgray")

        mst_edge_list = [(u, v) for u, v, w in mst_edges]
        nx.draw_networkx_edges(G, pos, edgelist=mst_edge_list, edge_color="green", width=3)

        edge_labels = nx.get_edge_attributes(G, "weight")
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

        plt.title(title)
        out_path = os.path.join(self.output_dir, filename)
        plt.savefig(out_path, dpi=150, bbox_inches="tight")
        plt.close()
        print(f"Saved: {out_path}")
        return out_path