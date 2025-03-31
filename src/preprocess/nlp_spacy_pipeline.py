'''
nlp_spacy_pipeline.py

This script uses spaCy's EntityRuler to extract structured information from unstructured drone error log messages.
It identifies subsystems, such as Obstacle Sensing, GPS, Signal, and event types, such as not functioning, too weak,
and high wind velocity, from natural language messages found in drone flight logs.

The extracted entities can be used to:
- Enrich anomaly detection models with contextual error information.
- Align log events with structured telemetry data by timestamp
- Enable consistent tagging across drones with varying message phrasing.

This pipeline is lightweight, customizable, and designed to scale as additional drone models and log formats are
introduced.
'''
from calendar import month

# Import statements
import spacy
import pandas as pd
import re
from datetime import datetime

# Load the English pipeline
nlp = spacy.load("en_core_web_sm")

# Add the EntityRuler
ruler = nlp.add_pipe("entity_ruler", before="ner")

# Define patterns in DJI Phantom Model error logs
dji_phantom_patterns = [
    # Capture hardware entities
    {"label": "SUBSYSTEM", "pattern": "Obstacle Sensing"},
    {"label": "SUBSYSTEM", "pattern": "antennas"},

    # Capture communication entities
    {"label": "COMMUNICATION", "pattern": "Signal"},

    # Capture drone status entities
    {"label": "STATUS", "pattern": "disabled"},

    # Capture environmental entities
    {"label": "ENVIRONMENT", "pattern": "Wind"},
    {"label": "ENVIRONMENT", "pattern": "Light"},

    # Capture geographic entities
    {"label": "LOCATION", "pattern": "Home Point"},

    # Capture event entities
    {"label": "EVENT", "pattern": "not functioning"},
    {"label": "EVENT", "pattern": "recorded"},
    {"label": "EVENT", "pattern": "weak"},

    # Capture drone metric entities
    {"label": "QUANTITY", "pattern": "velocity"},
    {"label": "QUANTITY", "pattern": "Altitude"},

    # Capture potential threat entities
    {"label": "WARNING", "pattern": "fly with caution"},
    {"label": "URGENT", "pattern": "ASAP"},

    # Capture safety suggestion entities
    {"label": "PROCEDURE", "pattern": "Return-to-Home"},
    {"label": "PROCEDURE", "pattern": "line of sight"},
    {"label": "PROCEDURE", "pattern": "land"},
    {"label": "PROCEDURE", "pattern": "facing toward the aircraft"},
    {"label": "PROCEDURE", "pattern": "Avoid blocking"}

]

# Add the patterns to the EntityRuler
ruler.add_patterns(dji_phantom_patterns)

# Get path to file log
path = ("/Users/ladylo/PycharmProjects/FlightForensics/data/raw/logs/error/DF061/19-06-2018-11VKF5500202NZ")

# Read the error log
with open(path, "r") as f:
    raw_log = f.read()

# Extract timestamped log blocks
pattern = r"##\s*(\d{2}:\d{2}:\d{2})(.*?)(?=##|$)"
matches = re.findall(pattern, raw_log, re.DOTALL)

# Hard code flight date and convert in dateTime format
flight_date = "2018-06-19"
flight_date = datetime.strptime(flight_date, "%Y-%m-%d")

# Strip whitespaces and empty lines
# log_msgs = [line.strip() for line in raw_log if line.strip()]

# Process each message to structure data
structured = []
for timestamp, message in matches:                # For each message,
    try:
        full_ts = datetime.strptime(timestamp.strip(), "%H:%M:%S").replace(
            year = flight_date.year,
            month = flight_date.month,
            day = flight_date.day
        )
    except ValueError:
        continue    # Skip any incompatible timestamps

    messages = message.strip().split("\n")    # Divide messages based on newline

    for message in messages:        # For each message,
        message = message.strip()       # remove whitespace
        if not message:             # and if it is a blank line,
            continue                    # skip it

        doc = nlp(message)  # Process the sentence

        for ent in doc.ents:                # For each entity,
            if ent.label != "org":              # Ensure that ORG entities are not included
                structured.append({                 # Then add it to a dictionary
                    "timestamp": timestamp.strip(),
                    "log_message": message,
                    "entity_txt": ent.text,
                    "entity_label": ent.label_
                })

# Create a Dataframe to store structured data
error_logs = pd.DataFrame(structured)
print(error_logs.head())

# Get path to the output location
output_path = "/Users/ladylo/PycharmProjects/FlightForensics/data/processed/logs/error/DF061/18-06-19_error_log_structured.csv"

# Save the DataFrame
error_logs.to_csv(output_path, index=False)