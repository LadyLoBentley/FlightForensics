'''
topo_sort.py

Kahn's Topological sorting algorithm used to sort the Directed Acyclic Graph (DAG) representing the historic drone
flight path for drone hovering analysis.
'''

import networkx as nx

def topo_sort(G):
    '''
    Function uses Kahn's topological sorting algorithm for sorting a directed acyclic graph (DAG).

    :param G: networkx graph representing a DAG.
    :return topo_order: The sorted networkx graph representing the DAG.
    '''

    # Initialize array containing in-degree mappings & assume all nodes degree is 0
    in_degree = {node: 0 for node in G.nodes}

    # Increment degree in each node if edge is found
    for u, v in G.edges:
        in_degree[v] += 1

    # Initialize queue with nodes having in-degree of 0
    queue = [node for node in G.nodes if in_degree[node] == 0]

    # Initialize array maintaining topological order
    topo_order = []

    # Start topological sorting
    while queue:            # While queue is not empty,
        u = queue.pop(0)        # Dequeue node in queue
        topo_order.append(u)    # Add node to sorted list

        for neighbor in G.successors(u):    # For each neighbor,
            in_degree[neighbor] -= 1        # Decrement degree

            if in_degree[neighbor] == 0:    # If in-dree equals 0,
                queue.append(neighbor)              # push neighbor onto queue

    return topo_order


G = nx.DiGraph()
G.add_edges_from([
    ('A', 'B'),
    ('A', 'C'),
    ('B', 'D'),
    ('C', 'D'),
])

topo_order = topo_sort(G)
print(topo_order)