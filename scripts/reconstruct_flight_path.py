'''
reconstruct_flight_path.py

After running the clean_flight_log.py script, the processed drone flight dataset can be used to reconstruct flight paths
recorded from drone telemetry logs. This script extracts two sets of spatial coordinates: IMU-calculated and GPS-based
latitude and longitude. Capturing both coordinate sets allows for a visual comparison to detect potential deviations or
abnormal flight behavior.

Additionally, GPS timestamps are utilized to sort the dataset chronologically and construct a spatial-temporal graph.
The resulting graph is modeled as a Directed Acyclic Graph (DAG) using the networkX library, with each node representing
a moment in time and each edge capturing the transition between positions based on time and movement.

Input: A processed dataset from `clean_anomaly_log.py` containing historic flight data.
Output: A networkX Graph object representing the spatial-temporal flight path.

This script is intended to create a Directed Acyclic Graph (DAG) representation of the drone's flight path utilizing
NetworkX.
'''
from networkx.algorithms.shortest_paths.dense import reconstruct_path

# Import statements

# Script(s)

# Data Structures
import pandas as pd
import networkx as nx

# Temporal and Spatial Tools
from geopy.distance import geodesic

#---------------------------------------------------------------------------------------------------------------------

# Function implementing graph construction
def construct_flight_path(input,
                          output=None,
                          drop_duplicates=True):
    '''
    Function to construct a spatial-temporal flight path.

    :param input: pandas DataFrame object containing drone telemetry data.
    :param output: (Optional) string representing the file path to save the processed dataset.
    :param drop_duplicates: (Optional) Boolean to drop duplicate entries in the processed dataset.
    :return: A Directed Acyclic Graph object representing the spatial-temporal flight path and the pandas DataFrame containing flight logs.
    '''


    drone_log = input
    #clean_flight_log(input)

    if drop_duplicates:
        drone_log = drone_log.drop_duplicates(subset=["gps_latitude", "gps_longitude", "imu_latitude", "imu_longitude"])

    if drop_duplicates:
        drone_log = drone_log.drop_duplicates(subset=["gps_latitude", "gps_longitude", "imu_latitude", "imu_longitude"])

    # Drop instances with relevant missing values
    drone_log = drone_log.dropna(subset=["imu_latitude",        # IMU-calculated latitude
                                         "imu_longitude",       # IMU-calculated longitude
                                         "gps_latitude",        # GPS-based latitude
                                         "gps_longitude",       # GPS-based longitude
                                         "gps_timestamp"])      # GPS-based timestamp

    # Convert gps_timestamp to dateTime format
    drone_log["gps_timestamp"] = pd.to_datetime(
        drone_log["gps_timestamp"], errors='coerce'
    ).dt.tz_localize(None)

    # Sort DataFrame in chronological order
    drone_log = drone_log.sort_values(by=["gps_timestamp"]).reset_index(drop=True)

    # Initialize the directed graph object
    G = nx.DiGraph()

    # Create a node for each instance holding spatial-temporal data
    for i, row in drone_log.iterrows():
        # Create the coordinate calculated by IMU sensors
        imu_coord = (row["imu_latitude"], row["imu_longitude"])

        # Create the coordinate captured by GPS satellites
        gps_coord = (row["gps_latitude"], row["gps_longitude"])

        # Create node containing attributes:
        G.add_node(
            i,                                  # Node Identifier,
            pos=imu_coord,                      # IMU-calculated coordinate,
            gps_pos=gps_coord,                  # GPS-based coordinate,
            timestamp=row["gps_timestamp"],     # GPS-based timestamp,
            control_mode=row["control_mode"],   # Drone's current control mode,
            velocity=row["vel_composite"],      # Drone's measurement of velocity,
            distance=row["dist_travelled"],      # And total distance drone has travelled
            anomaly_score=row["anomaly_score"], # Anomaly score of flight activity
            activity=row["anomaly_label"]       # normal or suspicious activity
        )

    # Connect the nodes
    for i in range(len(drone_log) -1):      # For each node,

        # Calculate delta time (the difference of time travelled from node-to-node)
        t1 = drone_log.loc[i, "gps_timestamp"]
        t2 = drone_log.loc[i+1, "gps_timestamp"]
        delta_time = (t2 - t1).total_seconds()      # Delta time in seconds

        # Calculate the distance between nodes
        coord1 = (drone_log.loc[i, "imu_latitude"], drone_log.loc[i, "imu_longitude"])
        coord2 = (drone_log.loc[i+1, "gps_latitude"], drone_log.loc[i+1, "gps_longitude"])
        distance = geodesic(coord1, coord2).meters  # distance in meters

        # Calculate the speed of the drone
        if delta_time == 0:
            speed = None  # Avoid calculating invalid speed
        else:
            speed = distance / delta_time

        # Add edges
        G.add_edge(
            i,          # Edge from current node
            i+1,        # to the subsequent node

            # Add the computed weights:
            delta_time=delta_time,   # time difference between nodes
            distance=distance,       # Distance between nodes,
            speed=speed              # Drone's speed during travel
        )

    # Return both the graph and pandas DataFrame representing the drone log
    return G, drone_log

log = pd.read_csv("/Users/ladylo/PycharmProjects/FlightForensics/data/processed/logs/flight/DF061/anomaly_detection/model_ready/flight_anomaly_dataset.csv")
log = log[log["flight_sequence"] == "flight04"].reset_index(drop=True)
G, _ = construct_flight_path(log)