"""
clean_anomaly_log.py

This script loads a raw drone flight CSV and selects relevant columns for detecting anomalies in
flight paths, removes rows with missing GPS data, convert incompatible data types, renames relevant
columns for interpretability, and saves a cleaned version to the processed logs folder.
"""
from tokenize import String

# Import statements
import pandas as pd
import os


def clean_anomaly_log(input_path, output_path):
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
        "GPS:Lat",
        "GPS:Long",

        # Altitude  - May be used for 3D trajectory
        "IMU_ATTI(0):relativeHeight:C",
        "IMU_ATTI(0):atti_cnt:D",
        "GPS:heightMSL",

        # Orientation - Used for direction tracking
        "IMU_ATTI(0):yaw:C",
        "IMU_ATTI(0):pitch:C",
        "IMU_ATTI(0):roll:C",
        "IMU_ATTI(0):tiltInclination:C",

        # Velocity - Used to understand motion of drone
        "IMU_ATTI(0):velN",
        "IMU_ATTI(0):velE",
        "IMU_ATTI(0):velD",
        "IMU_ATTI(0):velComposite:C",
        "GPS:velN",
        "GPS:velE",
        "GPS:velD",
        "MVO:velocityUncertainty1",
        "MVO:velocityUncertainty3",
        "MVO:velocityUncertainty4",
        "MVO:velocityUncertainty6",
        "IMUCalcs(0):diffVelN:C",
        "IMUCalcs(0):diffVelE:C",
        "IMUCalcs(0):diffVelD:C",

        # Distance - Cumulative tracking
        "IMU_ATTI(0):distanceTravelled:C",

        # Acceleration - Helpful for determining anomalies
        "IMU_ATTI(0):accelX",
        "IMU_ATTI(0):accelY",
        "IMU_ATTI(0):accelZ",
        "IMU_ATTI(0):accelComposite:C",

        # Position
        "IMUCalcs(0):PosN:C",   # Movement in North position
        "IMUCalcs(0):PosE:C",   # Movement in East position
        "IMUCalcs(0):PosD:C",   # Movement in Downward position
        "IMUCalcs(0):PositionError:C",     # Error in estimated position

        # Direction of Flight - Directional movement of the drone
        "IMU_ATTI(0):directionOfTravel[mag]:C",
        "IMU_ATTI(0):directionOfTravel[true]:C",

        # Obstacle Avoidance
        "OA:emergBrake",

        # Gyro
        "IMU_ATTI(0):gyroX",
        "IMU_ATTI(0):gyroZ",
        "IMU_ATTI(0):gyroComposite:C",
        "IMUCalcs(0):totalGyroZ:C",
        "IMUCalcs(0):totalGyroX:C",
        "IMUCalcs(0):totalGyroY:C",

        # Hovering
        "MVO:hoverPointUncertainty1",
        "MVO:hoverPointUncertainty2",
        "MVO:hoverPointUncertainty3",
        "MVO:hoverPointUncertainty4",
        "MVO:hoverPointUncertainty5",
        "MVO:hoverPointUncertainty6",

        # GPS Information - Helpful for detecting drops
        "GPS:numGPS",       # Fewer satellites - increased risk of GPS dropout
        "GPS:hDOP",
        "GPS:pDOP",
        "GPS:sAcc",     # Speed accuracy from GPS

        # Landing vs. In-Flight State
        "Controller:ctrl_mode",
        "Controller:motor_state:D",

        # Battery - Used for anomaly detection
        "BatteryStatus:volVerylow",
        "BatteryStatus:volLevel1:D",
        "BatteryStatus:vollevel2:D",
        "SMART_BATT:goHome%",
        "SMART_BATT:land%",
        "SMART_BATT:goHomeTime",
        "SMART_BATT:landTime",

        # Sensors
        "IMU_ATTI(0):temperature",
        "IMU_ATTI(0):sensor_stat:D",
        "IMU_ATTI(0):filter_stat:D",
        "IMU_ATTI(0):magMod:C"  # Checks for compass interference
    ]

    # Read the CSV into a pandas DataFrame
    input = pd.read_csv(input_path, usecols=lambda col: col in relevant_cols)

    # Convert strings representing booleans to boolean values
    input[["IMUCalcs(0):PositionError:C","OA:emergBrake"]]= input[["IMUCalcs(0):PositionError:C", "OA:emergBrake"]].astype('boolean')

    # Convert GPS:dateTimeStamp to dateTime format
    input["GPS:dateTimeStamp"] = pd.to_datetime(input["GPS:dateTimeStamp"])

    # Convert the object attributes to Strings
    input["Controller:ctrl_mode"] = input["Controller:ctrl_mode"].astype("category")

    # rename log attributes for better interpretability
    name_map = {
        # Time - Used for ordering & syncing
        "Clock:offsetTime": "clock_offset",
        "GPS:dateTimeStamp": "gps_timestamp",

        # Location
        "IMU_ATTI(0):Latitude": "imu_latitude",
        "IMU_ATTI(0):Longitude": "imu_longitude",
        "GPS:Lat": "gps_latitude",
        "GPS:Long": "gps_longitude",

        # Altitude  - May be used for 3D trajectory
        "IMU_ATTI(0):relativeHeight:C": "imu_rel_height",
        "IMUCalcs(0):height:C": "imu_calc_height",
        "IMU_ATTI(0):atti_cnt:D": "altitude_counter",
        "GPS:heightMSL": "gps_heightMSL",

        # Orientation - Used for direction tracking
        "IMU_ATTI(0):yaw:C": "yaw",
        "IMU_ATTI(0):pitch:C": "pitch",
        "IMU_ATTI(0):roll:C": "roll",
        "IMU_ATTI(0):tiltInclination:C": "tilt_inclination",

        # Velocity - Used to understand motion of drone
        "IMU_ATTI(0):velN": "vel_north",
        "IMU_ATTI(0):velE": "vel_east",
        "IMU_ATTI(0):velD": "vel_down",
        "IMU_ATTI(0):velComposite:C": "vel_composite",
        "GPS:velN": "gps_vel_north",
        "GPS:velE": "gps_vel_east",
        "GPS:velD": "gps_vel_down",
        "MVO:velocityUncertainty1": "velocity_uncertainty1",
        "MVO:velocityUncertainty3": "velocity_uncertainty3",
        "MVO:velocityUncertainty4": "velocity_uncertainty4",
        "MVO:velocityUncertainty6": "velocity_uncertainty6",
        "IMUCalcs(0):diffVelN:C": "delta_vel_north",
        "IMUCalcs(0):diffVelE:C": "delta_vel_east",
        "IMUCalcs(0):diffVelD:C": "delta_vel_down",

        # Distance - Cumulative tracking
        "IMU_ATTI(0):distanceTravelled:C": "dist_travelled",

        # Acceleration - Helpful for determining anomalies
        "IMU_ATTI(0):accelX": "accel_x",
        "IMU_ATTI(0):accelY": "accel_y",
        "IMU_ATTI(0):accelZ": "accel_z",
        "IMU_ATTI(0):accelComposite:C": "accel_composite",

        # Position
        "IMUCalcs(0):PosN:C": "imu_pos_north",  # Movement in North position
        "IMUCalcs(0):PosE:C": "imu_pos_east",  # Movement in East position
        "IMUCalcs(0):PosD:C": "imu_pos_down",  # Movement in Downward position
        "IMUCalcs(0):PositionError:C": "pos_error",  # Error in estimated position

        # Direction of Flight - Directional movement of the drone
        "IMU_ATTI(0):directionOfTravel[mag]:C": "direction_travel_magnetic",
        "IMU_ATTI(0):directionOfTravel[true]:C": "direction_travel_true",

        # Obstacle Avoidance
        "OA:emergBrake": "oa_emergency_brake",

        # Gyro
        "IMU_ATTI(0):gyroX": "gyro_x",
        "IMU_ATTI(0):gyroZ": "gyro_z",
        "IMU_ATTI(0):gyroComposite:C": "gyro_composite",
        "IMUCalcs(0):totalGyroZ:C": "total_gyro_z",
        "IMUCalcs(0):totalGyroX:C": "total_gyro_x",
        "IMUCalcs(0):totalGyroY:C": "total_gyro_y",

        # Hovering
        "MVO:hoverPointUncertainty1": "hover_point_uncertainty1",
        "MVO:hoverPointUncertainty2": "hover_point_uncertainty2",
        "MVO:hoverPointUncertainty3": "hover_point_uncertainty3",
        "MVO:hoverPointUncertainty4": "hover_point_uncertainty4",
        "MVO:hoverPointUncertainty5": "hover_point_uncertainty5",
        "MVO:hoverPointUncertainty6": "hover_point_uncertainty6",

        # GPS Information - Helpful for detecting drops
        "GPS:numGPS": "num_satellites",  # Fewer satellites - increased risk of GPS dropout
        "GPS:hDOP": "gps_hdop",     # Horizontal dilution of precision
        "GPS:pDOP": "gps_pdop",     # Positional dilution of precision
        "GPS:sAcc": "gps_speed_accuracy",  # Speed accuracy from GPS

        # Landing vs. In-Flight State
        "Controller:ctrl_mode": "control_mode",
        "Controller:motor_state:D": "motor_state",

        # Battery - Used for anomaly detection
        "BatteryStatus:volVerylow": "battery_very_low",
        "BatteryStatus:volLevel1:D": "battery_level1",
        "BatteryStatus:vollevel2:D": "battery_level2",
        "SMART_BATT:goHome%": "batter_go_home",
        "SMART_BATT:land%": "batter_land",
        "SMART_BATT:goHomeTime": "batter_go_home_time",
        "SMART_BATT:landTime": "batter_land_time",

        # Sensors
        "IMU_ATTI(0):temperature": "temperature",
        "IMU_ATTI(0):sensor_stat:D": "imu_sensor_status",
        "IMU_ATTI(0):filter_stat:D": "imu_filter_status",
        "IMU_ATTI(0):magMod:C": "compass_interference"  # Checks for compass interference
    }

    # rename the attributes using dict
    input.rename(columns=name_map, inplace=True)

    # Save the cleaned dataset into the processed folder in \data
    input.to_csv(output_path, index=False)

# Create the processed data
clean_anomaly_log("/Users/ladylo/PycharmProjects/FlightForensics/data/raw/logs/flight/DF061/18-06-19-02-04-47_FLY003.csv",
                 "/Users/ladylo/PycharmProjects/FlightForensics/data/processed/logs/flight/DF061/anomaly_detection/cleaned_18-06-19-02-04-47_anomaly_log.csv")