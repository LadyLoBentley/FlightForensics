'''
visualize_flight_paths.py

Constructs a networkx graph object using the reconstruct_flight_path script and creates a basic graphical representation
of two flight paths. One is calculated by the drone's IMU sensors and the other path is gps-based. The visual
representation is used to outline the drone flight path and detect any deviations from the two given paths. This script
may be utilized for testing purposes, flight deviation analysis, and a simplistic view of drone flight activity.

Input: A string representing the raw data of drone flight logs as input.
       path to store the processed dataset.

Output: A visual of the drone flight paths as a networkx graph

'''

# Import Statements

# Script(s)
import reconstruct_flight_path

# Data Structures
import pandas as pd
import numpy as pd
import networkx as nx

# Import visualizations
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import dash

#---------------------------------------------------------------------------------------------------------------------

def plot_basic_path(input,
                    output=None,
                    drop_duplicates=True,
                    imu_color="#E69F00",  # Orange (IMU path nodes)
                    gps_color="#56B4E9",  # Sky Blue (GPS path nodes)
                    imu_edge_color="#B35A00",  # Softer orange
                    gps_edge_color = "#005F80",  # Muted blue
                    node_size=50,
                    labels=False):
    '''
    Function to plot a basic path comparing the IMU-calculated coordinates and GPS-based coordinates to explore any
    deviations in the flight path.

    :param input: String representing the file path to the raw CSV file containing flight logs
    :param output: (Optional) String representing the file path to save the processed CSV file
    :param drop_duplicates: (Optional) Boolean to drop duplicate entries in the input CSV file
    :param imu_color: (Optional) string representing the color of the IMU-calculated coordinate nodes
    :param gps_color: (Optional) String representing the color of the GPS-calculated coordinate nodes
    :param imu_edge_color: (Optional) String representing the color of the IMU-calculated coordinate edges
    :param gps_edge_color: (Optional) String representing the color of the GPS-calculated coordinate edges
    :param node_size: (Optional) Integer representing the size of the nodes in the graph
    :param labels: (Optional) Boolean indicating if the path should be labelled or not
    :return: None
    '''

    # Get the Graph representing the drone flight paths
    G, _ = reconstruct_flight_path.construct_flight_path(input, drop_duplicates)

    # Get IMU-calculated coordinates from node attributes
    pos = nx.get_node_attributes(G, "pos")

    # Get GPS-based coordinates from node attributes
    gps_pos = nx.get_node_attributes(G, "gps_pos")

    # Create the figure
    fig, ax = plt.subplots(figsize=(10, 8))
    alpha_val = 0.8

    # Plot the IMU-calculated coordinates
    # IMU Nodes and Edges
    nx.draw_networkx_nodes(G,
                           pos,
                           node_size=node_size,
                           node_color=imu_color,
                           alpha=alpha_val,
                           ax=ax)

    nx.draw_networkx_edges(G,
                           pos,
                           edge_color=imu_edge_color,
                           alpha=0.6,
                           width=1.25,
                           ax=ax)

    # GPS Nodes and Edges
    nx.draw_networkx_nodes(G,
                           gps_pos,
                           node_size=node_size,
                           node_color=gps_color,
                           alpha=alpha_val,
                           ax=ax)

    nx.draw_networkx_edges(G,
                           gps_pos,
                           edge_color=gps_edge_color,
                           alpha=0.6,
                           width=1.25,
                           ax=ax)

    # Highlight Start and End
    if pos:
        start = list(pos.keys())[0]
        end = list(pos.keys())[-1]
        ax.text(*pos[start],
                "Start",
                fontsize=10,
                color="green",
                weight="bold",
                bbox=dict(facecolor='white', alpha=0.7))

        ax.text(*pos[end],
                "End",
                fontsize=10,
                color="red",
                weight="bold",
                bbox=dict(facecolor='white', alpha=0.7))

    # Adjust axis limits to zoom into path area
    all_x = [coord[0] for coord in pos.values()] + [coord[0] for coord in gps_pos.values()]
    all_y = [coord[1] for coord in pos.values()] + [coord[1] for coord in gps_pos.values()]

    ax.set_xlim(min(all_x) - 0.0005, max(all_x) + 0.0005)
    ax.set_ylim(min(all_y) - 0.0005, max(all_y) + 0.0005)

    # Add legend
    legend = [
        mpatches.Patch(color=imu_color, label="IMU Path"),
        mpatches.Patch(color=gps_color, label="GPS Path")
    ]
    ax.legend(handles=legend, loc='upper right')

    # Title and formatting
    ax.set_title("GPS vs IMU Flight Path: Basic Comparison", fontsize=14)
    ax.axis('off')
    plt.tight_layout()
    plt.show()

plot_basic_path("/Users/ladylo/PycharmProjects/FlightForensics/data/raw/logs/flight/DF061/18-06-19-02-04-47_FLY003.csv")
plot_basic_path("/Users/ladylo/PycharmProjects/FlightForensics/data/raw/logs/flight/DF061/18-06-19-02-11-31_FLY004.csv")