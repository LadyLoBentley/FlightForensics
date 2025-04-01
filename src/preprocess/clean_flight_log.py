"""
clean_flight_log.py

This script loads a raw drone flight CSV and selects relevant columns for flight path reconstruction,
removes rows with missing GPS data, convert incompatible data types, renames relevant columns for
interpretability, and saves a cleaned version to the processed logs folder.

Input: A dataset of telemetry data from drone logs.
Output: A cleaned dataset of only relevant features for reconstructing flight paths from drones.

This script is intended for use of simulating historical flight paths.
"""

# Import statements
import pandas as pd
import os


def clean_flight_log(input_path, output_path):
    '''
    Function to clean the flight log file to reconstruct flight paths.

    :param input_path: String representing the path of the raw input CSV file.
    :param output_path: String representing the path of the processed CSV file.
    '''

    # List of columns relevant to reconstructing flight paths
    relevant_cols = [
        # Time - Used for ordering & syncing
        "Clock:offsetTime",
        "GPS:dateTimeStamp",

        # Location
        "IMU_ATTI(0):Latitude",
        "IMU_ATTI(0):Longitude",
        "IMUCalcs(0):Lat:C",
        "IMUCalcs(0):Long:C",
        "GPS:Lat",
        "GPS:Long",

        # Altitude  - May be used for 3D trajectory
        "IMU_ATTI(0):relativeHeight:C",
        "IMUCalcs(0):height:C",
        "GPS:heightMSL",

        # Orientation - Used for direction tracking
        "IMU_ATTI(0):yaw:C",
        "IMU_ATTI(0):pitch:C",
        "IMU_ATTI(0):roll:C",
        "IMU_ATTI(0):yaw360:C",
        "IMU_ATTI(0):yawUnWrapped:C",

        # Velocity - Used to understand motion of drone
        "IMU_ATTI(0):velN",
        "IMU_ATTI(0):velE",
        "IMU_ATTI(0):velD",
        "IMU_ATTI(0):velH:C",   # Horizontal speed
        "IMU_ATTI(0):velComposite:C",
        "GPS:velN",
        "GPS:velE",
        "GPS:velD",

        # Distance - Cumulative tracking
        "IMU_ATTI(0):distanceTravelled:C",

        # Position
        "IMUCalcs(0):PosN:C",   # Movement in North position
        "IMUCalcs(0):PosE:C",   # Movement in East position
        "IMUCalcs(0):PosD:C",   # Movement in Downward position

        # Landing vs. In-Flight State
        "Controller:ctrl_mode",
        "Controller:motor_state:D"
    ]

    # Read the CSV into a pandas DataFrame
    input = pd.read_csv(input_path, usecols=lambda col: col in relevant_cols)

    # Drop the rows with missing values
    #print(input.isna().sum())

    # Convert the GPS:dateTimeStamp to datetime format
    input["GPS:dateTimeStamp"] = pd.to_datetime(input["GPS:dateTimeStamp"])
    #print(input.info())

    # Dictionary to map original names with improved attribute names
    name_map = {
        # Time - Used for ordering & syncing
        "Clock:offsetTime": "clock_offset",
        "GPS:dateTimeStamp": "gps_timestamp",

        # Location
        "IMU_ATTI(0):Latitude": "imu_latitude",
        "IMU_ATTI(0):Longitude": "imu_longitude",
        "IMUCalcs(0):Lat:C": "imu_calc_lat",
        "IMUCalcs(0):Long:C": "imu_calc_long",
        "GPS:Lat": "gps_latitude",
        "GPS:Long": "gps_longitude",

        # Altitude  - May be used for 3D trajectory
        "IMU_ATTI(0):relativeHeight:C": "imu_rel_height",
        "IMUCalcs(0):height:C": "imu_calc_height",
        "GPS:heightMSL": "gps_heightMSL",

        # Orientation - Used for direction tracking
        "IMU_ATTI(0):yaw:C": "yaw",
        "IMU_ATTI(0):pitch:C": "pitch",
        "IMU_ATTI(0):roll:C": "roll",
        "IMU_ATTI(0):yaw360:C": "yaw360",
        "IMU_ATTI(0):yawUnWrapped:C": "yaw_UnWrapped",

        # Velocity - Used to understand motion of drone
        "IMU_ATTI(0):velN": "vel_north",
        "IMU_ATTI(0):velE": "vel_east",
        "IMU_ATTI(0):velD": "vel_down",
        "IMU_ATTI(0):velH:C": "vel_horizontal",  # Horizontal speed
        "IMU_ATTI(0):velComposite:C": "vel_composite",
        "GPS:velN": "gps_vel_north",
        "GPS:velE": "gps_vel_east",
        "GPS:velD": "gps_vel_down",

        # Distance - Cumulative tracking
        "IMU_ATTI(0):distanceTravelled:C": "dist_travelled",

        # Position
        "IMUCalcs(0):PosN:C": "imu_pos_north",  # Movement in North position
        "IMUCalcs(0):PosE:C": "imu_pos_east",  # Movement in East position
        "IMUCalcs(0):PosD:C": "imu_pos_down",  # Movement in Downward position

        # Landing vs. In-Flight State
        "Controller:ctrl_mode": "control_mode",
        "Controller:motor_state:D": "motor_state"
    }

    # Rename the columns to increase interpretability of the dataset
    input.rename(columns=name_map, inplace=True)

    #print(raw_input.columns)
    #print(raw_input.head())

    # Save the cleaned dataset into the processed folder in \data
    input.to_csv(output_path, index=False)

# Create the processed data from flight at 02-04-47
clean_flight_log("/Users/ladylo/PycharmProjects/FlightForensics/data/raw/logs/flight/DF061/18-06-19-02-04-47_FLY003.csv",
                 "/Users/ladylo/PycharmProjects/FlightForensics/data/processed/logs/flight/DF061/path_construction/cleaned_18-06-19-02-04-47_path_log.csv")

# Create the processed data from flight at 02-11-31
clean_flight_log("/Users/ladylo/PycharmProjects/FlightForensics/data/raw/logs/flight/DF061/18-06-19-02-11-31_FLY004.csv",
                 "/Users/ladylo/PycharmProjects/FlightForensics/data/processed/logs/flight/DF061/path_construction/cleaned_18-06-19-02-11-31_path_log.csv")