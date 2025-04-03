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
import seaborn as sns
import dash

#---------------------------------------------------------------------------------------------------------------------

def plot_basic_path(input,
                    output=None,
                    imu_color="blue",
                    gps_color="green",
                    imu_edge_color="grey",
                    gps_edge_color="black",
                    node_size=30,
                    labels=False):
    '''
    Function to plot a basic path comparing the IMU-calculated coordinates and GPS-based coordinates to explore any
    deviations in the flight path.

    :param input: String representing the file path to the raw CSV file containing flight logs
    :param output: (Optional) String representing the file path to save the processed CSV file
    :param imu_color: (Optional) string representing the color of the IMU-calculated coordinate nodes
    :param gps_color: (Optional) String representing the color of the GPS-calculated coordinate nodes
    :param imu_edge_color: (Optional) String representing the color of the IMU-calculated coordinate edges
    :param gps_edge_color: (Optional) String representing the color of the GPS-calculated coordinate edges
    :param node_size: (Optional) Integer representing the size of the nodes in the graph
    :param labels: (Optional) Boolean indicating if the path should be labelled or not
    :return: None
    '''

    # Get the Graph representing the drone flight paths
    G, _ = reconstruct_flight_path.construct_flight_path(input)

    # Get IMU-calculated coordinates from node attributes
    pos = nx.get_node_attributes(G, "pos")

    # Get GPS-based coordinates from node attributes
    gps_pos = nx.get_node_attributes(G, "gps_pos")

    # Create the figure
    plt.figure(figsize=(12, 8))

    # Plot the IMU-calculated coordinates
    nx.draw( G,
             pos,
             node_size=node_size,
             node_color=imu_color,
             edge_color=imu_edge_color,
             with_labels=labels
             )

    nx.draw( G,
             gps_pos,
             node_size=node_size,
             node_color=gps_color,
             edge_color=gps_edge_color,
             with_labels=labels
             )
    plt.title('GPS vs IMU Flight Path: Basic Comparison')
    plt.show()

plot_basic_path("/Users/ladylo/PycharmProjects/FlightForensics/data/raw/logs/flight/DF061/18-06-19-02-04-47_FLY003.csv")
plot_basic_path("/Users/ladylo/PycharmProjects/FlightForensics/data/raw/logs/flight/DF061/18-06-19-02-11-31_FLY004.csv")