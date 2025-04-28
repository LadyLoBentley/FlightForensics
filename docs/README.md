# README: ✈️FlightForensics 
*A forensic Analysis of Drone Flight Data using NLP, Graph-Based Visualization, and Anomaly Detection.*

## Project Overview
Flight forensics is a drone forensics tool that extracts, processes, and visualizes flight data to reconstruct drone 
flight paths. It leverages **natural language processing (NLP)** for log extraction, graph-based visualization and 
animation for flight path reconstruction, and rule-based or ML-driven anomaly detection to classify suspicious drone
activity.

This project includes supervised anomaly detection using Isolation Forest-generated pseudo-labels and XGBoost-based 
classification for enhanced suspicious flight detection.

---

## Goals & Objectives
1. **Develop an NLP Model** to extract structured flight data from raw logs.
2. **Reconstruct Flight Paths** using extracted data and a graph-based approach.
3. **Visualize Drone Flight Paths** with real-time simulation using NetworkX & Matplotlib.
4. **Implement Anomaly Detection** (Rule-Based & ML-Based) to classify suspicious flights.
5. **Detect Unauthorized Surveillance** by implementing excessive hovering integrated with anomaly detection.
5. **Ensure Scalability** by expanding to multiple datasets.

---

## Project Structure

- **data** → flight logs and other relevant extracted data
  - **models**  → Trained XGBoost model for anomaly classification
  - **Processed** → Cleaned datasets used in machine learning and flight path reconstruction.
  - **Raw** → Original telemetry data extracted by drone logs.
- **docs** → Documentation such as README, milestones, and project plans
- **notebooks** → Jupyter notebooks for data exploration
- **scripts** → Standalone scripts used for path reconstruction and validation
- **src** → Core source code
  - **analysis** → Flight data analysis scripts such as hover detection.
  - **preprocess** → Data cleaning and preprocessing scripts
  - **utils** → Helper functions and utilities
  - **visualization** → Flight path reconstruction and plotting
- **.gitignore** → Git ignored files
- **requirements.txt** → Project dependencies

---

## Preprocessing Scripts

The following scripts are used to clean and prepare drone flight logs for analysis:

- `Clean_flight_log.py`: Cleans raw drone CSV logs for flight path reconstruction. It filters relevant GPS, velocity, and orientation data, removes missing values, renames columns for clarity, and saves the output to the `processed/logs/flight/<flight_id/path_construction/` directory.


- `clean_anomaly_log.py`: Prepares flight logs for anomaly detection by selecting relevant features such as velocity, acceleration, sensor readings, and battery stats. Outputs are saved to the `processed/logs/flight/<flight_id>/anomaly_detection/` directory.


- `nlp_spacy_pipeline.py`: Extracts structured entities from unstructured error log messages using spaCy's EntityRuler. Outputs labeled logs, such as subsystem, event, and warning, to `processed/logs/error/<flight_id>/` for feature engineering and anomaly detection.

These scripts can be found in the `src/preprocess/` directory.

---

## Flight Path Reconstruction

The flight path reconstruction module uses cleaned drone logs to create a spatial-temporal graph of the drone's movement.
Each node represents a timestamped IMU-calculated position, and each edge connects sequential nodes, weighted by:

- `delta_time`: Time elapsed between nodes
- `distance`: IMU_based geodesic distance
- `speed`: Distance divided by time
- `position_error`: Deviation between IMU and GPS

Node attributes include:
- `pos`: IMU-calculated coordinates (latitude, longitude)
- `gps_pos`: GPS-based coordinates (latitude, longitude)
- `timestamp`: GPS timestamp converted in dateTime format
- `control_mode`: Drone's current control mode
- `motor_state`: Motor status
- `velocity`: Composite velocity reported by the drone
- `distance`: Cumulative distance traveled

Script: `\scripts\reconstruct_flight_path.py`
- Builds a **Directed Acyclic Graph (DAG)** representing the drone's historic flight path using `networkx`.

Notebook: `notebooks/construct_flight_paths.ipynb`
- Interactive notebook used to prototype graph construction and visualization logic prior to scripting.

---

## Machine Learning - Anomaly Classification

The anomaly detection component uses a hybrid approach:
- **Unsupervised Pre-Labeling**: An Isolation Forest is applied to cleaned logs to generate pseudo-labels (`-1` for anomaly, `1` for normal).
- **Supervised Classification**: An XGBoost model is trained using these labels to learn generalizable anomaly patterns across flights.

Notebook: `/notebooks/flight_anomaly_model.ipynb`

---
## Flight Simulation 

Develops a simulation reenacting historic drone movements utilizing the networkX DAG as the data structure representing 
the drone path and matplotlib's animation library to create a .mp4 visualization. Drone behavior is disclosed by the 
color of the node: red indicates suspicious flight or suspicious hovering, green indicates normal flight, and blue 
indicates normal hovering. Textual context is displayed to bring more insight to suspicious drone activity, distinguishing
between hovering and normal flight activity.

Script: `/scripts/simulate_drone_flight.py`

---
## Unauthorized Surveillance

Utilizes Kahn's topological sorting algorithm to ensure temporal node ordering for successful hovering detection. 
The script maintains two list: one for current segment of flight path, and another for confirmed hovering segments. 
A threshold is given for speed and distance. If current segment remain below provided thresholds, then each node associated
will be appended to the list. Otherwise, the total time of current segment is compared to a given time threshold. The total
segment will be added to the hovering lists if hovering is confirmed, and the algorithm will reset current segment and 
repeat until drone has landed.

Topological Sorting: `/src/analysis/topo_sort.py`
Drone Hover Detection: `/src/analysis/detect_excess_hover.py`

---

## Saved Models
The XGBoost anomaly classifier is trained using pseudo-labels from Isolation Forest.

Model Path: `data/models/xgb_anomaly_model.pkl`


Use this model to classify unseen flight logs during simulation and visualization.

Example:
```python

import joblib
model = joblib.load("data/models/xgb_anomaly_model.pkl")
y_pred = model.predict(new_flight_data)
```
---

## Installation
To set up the environment and install dependencies, run:

    pip install -r requirements.txt
    python -m spacy download en_core_web_sm

--- 

## Dataset Overview
### Data Sources
Data is sourced from the VTO.inc Drone Forensics Program, supported by DHS Cyber Security Division.


**Dataset Link:** FREDS Drone Dataset → https://cfreds-archive.nist.gov/drone-images.html

--- 

## Project Phases & Milestones
- **Phase 1:** Prototype Development *(March 12 – April 6)*
  - Milestone 1: Define Scope & Requirements (Completed)
  - Milestone 2: Data Processing & NLP Model (Completed)
  - Milestone 3: Flight Path Reconstruction (Completed)
  - Milestone 4: Initial Visualization (Completed)


- **Phase 2:** Data Expansion & Refinement *(March 23 – April 10)*
  - Milestone 5: Feature Engineering & ML Model Training (Completed) 
  - Milestone 6: Integrate model predictions into visualization (Completed)
  - Milestone 7: Final ML Model Testing & Refinements (Completed)


- **Phase 3:** Expansion of the Program *(April 17 – April 20)*
  - Milestone 8: Expand NLP & Flight Path Reconstruction (Future Work) 
  

- **Phase 4:** Final Testing & Documentation *(April 12 – April 23)*
  - Milestone 9: System Testing & Optimization (Completed) 
  - Milestone 10: Documentation & Final Report (Completed)


---

## Citations
1. **CFREDS Drone Dataset**
   - Cyber Forensic Reference Dataset: https://cfreds-archive.nist.gov/drone-images.html
2. **Named Entity Recognition for Drone Forensics using BERT & DistilBERT** 
   - IEEE Xplore: https://ieeexplore.ieee.org/document/98629163
3. **DronLomaly: Runtime Detection of Anomalous Drone Behaviors**
   - SMU Research: https://ink.library.smu.edu.sg/cgi/viewcontent.cgi?article=8548&context=sis_research