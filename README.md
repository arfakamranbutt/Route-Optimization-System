# Route Optimization System

A graph-based analysis and route optimization system developed for my Design and Analysis of Algorithms (DAA) course in Python.

This project demonstrates the implementation and visualization of classical graph algorithms used in route planning and network optimization.

## Features

- Graph creation and visualization
- Dijkstra's Shortest Path Algorithm
- A* Search Algorithm
- Prim's Minimum Spanning Tree (MST)
- Performance analysis and comparison
- Automatic graph visualizations

## Algorithms Implemented

### Dijkstra's Algorithm
Computes the shortest path between a source node and destination node in a weighted graph.

### A* Search Algorithm
Uses heuristic-based search to efficiently find optimal paths.

### Prim's Algorithm
Generates a Minimum Spanning Tree that connects all vertices with minimum total edge weight.

## Project Structure

```text
algorithms.py    # Graph algorithms
graph.py         # Graph construction and management
visualizer.py    # Graph visualization functions
analyzer.py      # Algorithm analysis utilities
main.py          # Program entry point
images/          # Generated visual outputs
```

## Technologies Used

- Python
- NetworkX
- Matplotlib

## Installation

Clone the repository:

```bash
git clone https://github.com/arfakamranbutt/route-optimization-system.git
cd route-optimization-system
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the project:

```bash
python main.py
```

## Sample Outputs

### Original Graph

![Graph](images/graph.png)

### Dijkstra Shortest Path

![Dijkstra](images/dijkstra_path.png)

### A* Search Path

![A Star](images/astar_path.png)

### Minimum Spanning Tree

![MST](images/mst.png)

## Learning Outcomes

This project demonstrates practical applications of:

- Graph Theory
- Shortest Path Algorithms
- Greedy Algorithms
- Algorithm Analysis
- Data Structures

## Future Improvements

- Interactive GUI using Streamlit
- Real-world map integration
- Traffic-aware routing
- Runtime benchmarking on larger datasets
- Additional graph algorithms

## Author

Arfa Kamran
CS Student
