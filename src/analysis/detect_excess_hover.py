'''
Detect_excess_hover.py

Identifies excessive hovering behavior in drone flight data by analyzing
topologically sorted telemetry data in a DAG structure.
'''

from geopy.distance import geodesic
from src.analysis.topo_sort import topo_sort
import networkx as nx

def same_location(pos_u,
                  pos_v,
                  dist_thres=0.5):

    '''
    Function detects whether drone remains at the same location

    :param pos_u: tuple representing node coordinates
    :param pos_v: tuple representing node coordinates
    :param dist_thres: threshold for distance between two nodes
    :return: boolean determining whether the drone is at the same location
    '''

    return geodesic(pos_u, pos_v).meters < dist_thres

def detect_hovering(G,
                    velocity_thresh=0.5,
                    time_thresh=0.5,
                    dist_thresh=0.5):

    '''
    Function determines whether drone is hovering, detecting potential unauthorized surveillance.

    :param G: networkX Directed Acyclic Graph (DAG) representing drone flight path.
    :param velocity_thresh: float representing velocity threshold used to determine hovering.
    :param time_thresh: float representing time threshold used to determine hovering.
    :param dist_thresh: float representing distance threshold used to determine hovering.
    :return:
    '''

    # Sort the nodes using topological sorting
    sorted_nodes = topo_sort(G)

    # Get the coordinates from the node attributes
    pos = nx.get_node_attributes(G, 'pos')

    hover_segments = []     # Initialize array containing hovering flight activity
    current_segment = []    # Initialize list to contain current path segment
    total_time = 0          # Initialize time tracker

    # Analyze the flight path to detect hovering
    for i in range(len(sorted_nodes) - 1):      # For each sorted node in DAG,
        u = sorted_nodes[i]         # Starting node
        v = sorted_nodes[i + 1]     # Destination node

        edge = G.get_edge_data(u, v)    # Get edge attributes

        if(
                edge is None or     # If there is no edge,
                u not in pos or     # or starting node or
                v not in pos        # destination node is not in position,
        ):
            continue                # skip

        speed = edge.get('speed', 0)
        time = edge.get('delta_time', 0)

        if(
            speed is not None and                       # If speed attribute exists,
            speed < velocity_thresh and                 # and is less than provided threshold
            same_location(pos[u], pos[v], dist_thresh)  # without changing location,
        ):
            current_segment.append((u, v))      # Evaluate potential hovering activity
            total_time += time                  # and record its time

        else:           # Otherwise, 2/3 qualifications are reached
            if total_time > time_thresh:    # and time exceed threshold,
                hover_segments.append((current_segment.copy(), total_time))     # So the drone is hovering

            current_segment = []            # Clear out current activity
            total_time = 0                  # and remove time

    # Check the last instance for hovering if applicable
    if total_time > time_thresh: hover_segments.append((current_segment.copy(), total_time))

    return hover_segments       # Return positions of hovering

