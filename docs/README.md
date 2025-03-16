# README: ✈️FlightForensics 
*A forensic Analysis of Drone Flight Data using NLP, Graph-Based Visualization, and Anomaly Detection.*

## Project overview
Flight forensics is a drone forensics tool that extracts, processes, and visualizes flight data to reconstruct drone 
flight paths. It leverages **natural language processing (NLP) for log extraction, graph-based visualization and 
animation for flight path reconstruction, and rule-based or ML-driven anomaly detection to classify suspicious drone
activity.

---

## Goals & Objectives
1. **Develop an NLP Model** to extract structured flight data from raw logs.
2. **Reconstruct Flight Paths** using extracted data and a graph-based approach.
3. **Visualize Drone Flight Paths** with real-time simulation using NetworkX & Matplotlib.
4. **Implement Anomaly Detection** (Rule-Based & ML-Based) to classify suspicious flights.
5. **Ensure Scalability** by expanding to multiple datasets.

---

## Project structure

- **data** → flight logs and other relevant extracted data
- **docs** → Documentation such as README, milestones, and project plans
- **notebooks** → Jupyter notebooks for data exploration
- **scripts** → Standalone scripts used for preprocessing and validation
- **src** → Core source code
  - **analysis** → Flight data analysis scripts
  - **extract** → Scripts to extract flight logs from backups 
  - **preprocess** → Data cleaning and preprocessing
  - **utils** → Helper functions and utilities
  - **visualization** → Flight path reconstruction and plotting
- **tests** → Unit testing to verify data integrity 
- **.gitignore** → Git ignored files
- **requirements.txt** → Project dependencies

---

## Installation
To set up the environment and install dependencies, run:

    pip install -r requirements.txt

--- 

## Dataset Overview
### Data Sources
Data is sourced from the VTO.inc Drone Forensics Program, supported by DHS Cyber Security Division.
***Dataset Link:** CFREDS Drone Dataset → https://cfreds-archive.nist.gov/drone-images.html

--- 

## Project Phases & Milestones
- **Phase 1:** Prototype Development *(March 12 – April 6)*
  - Milestone 1: Define Scope & Requirements (Completed)
  - Milestone 2: Data Processing & NLP Model (In Progress)
  - Milestone 3: Flight Path Reconstruction (In Queue)
  - Milestone 4: Initial Visualization (In Queue)
  - Milestone 5: Implement Rule-Based Anomaly Detection (In Queue)
  
  
- **Phase 2:** Data Expansion & Refinement *(April 7 – April 12)*
  - Milestone 6: Expand NLP & Flight Path Reconstruction (In Queue) 
  - Milestone 7: Improve Rule-Based Detection & Performance (In Queue)
  
  
- **Phase 3:** Machine Learning Anomaly Detection *(April 13 – April 17)*
  - Milestone 8: Train ML-Based Anomaly Detection Model (In Queue) 
  - Milestone 9: Integrate ML-Based Anomalies into Visualization 
  
  
- **Phase 4:** Final Testing & Documentation *(April 18 – April 21)*
  - Milestone 10: System Testing & Optimization (In Queue) 
  - Milestone 11: Documentation & Final Report (In Queue) 
  

---

## Citations
1. **CFREDS Drone Dataset**
   - Cyber Forensic Reference Dataset: https://cfreds-archive.nist.gov/drone-images.html
2. **Named Entity Recognition for Drone Forensics using BERT & DistilBERT** 
   - IEEE Xplore: https://ieeexplore.ieee.org/document/98629163
3. **DronLomaly: Runtime Detection of Anomalous Drone Behaviors**
   - SMU Research: https://ink.library.smu.edu.sg/cgi/viewcontent.cgi?article=8548&context=sis_research