# HPC Job Carbon Footprint Estimator

## Overview

This web application, built with Streamlit, helps HPC users to:

1.  Model HPC jobs by defining parameters like size, duration, and hardware characteristics
2.  Analyse the impact of data centre efficiency (PUE) and average node utilisation
3.  Calculate the influence of electricity grid carbon intensity on overall carbon footprint
4.  Compare emissions across different geographical locations
5.  Contextualise carbon emissions using practical equivalencies

**Disclaimer:** This is a simplified model for educational purposes. Real-world carbon accounting depends on many factors not included here (e.g., real-time grid changes, specific hardware models, embodied carbon). Results should be used as estimates to understand relative impacts.

## Features

*   Job parameter configuration via input fields
*   Hardware and data centre inputs for node power profiles and PUE
*   Location-based intensity selection
*   Energy consumption (kWh) and carbon emissions (kg CO₂e) calculations
*   Impact equivalencies for contextualisation
*   Geographical comparison of carbon footprint
*   Technical explanations of PUE and Carbon Intensity
*   Model assumptions documentation

## Requirements

*   Python 3.x
*   The following Python libraries:
    *   `streamlit`
    *   `pandas`
    *   `plotly`

## Installation

1.  **Ensure Python 3 is installed** on your system.
2.  **Clone or download** the repository/directory containing the application script (e.g., `hpc_carbon_app.py`).
3.  **Open a terminal or command prompt**, navigate to the directory where you saved the script.
4.  **Install the required libraries** using pip:
    ```bash
    pip install streamlit pandas plotly
    ```

## How to Run the Application

1.  **Open a terminal or command prompt.**
2.  **Navigate** to the directory containing the `hpc_carbon_app.py` file.
3.  **Run the Streamlit application** using the following command:
    ```bash
    streamlit run hpc_carbon_app.py
    ```
4.  Streamlit will start a local web server, and the application should automatically open in your default web browser. If not, the terminal will provide a local URL (usually `http://localhost:8501`) that you can open manually.

## How to Use the Application

The interface comprises a sidebar for inputs and a main area for results.

### 1. Configure Simulation Parameters (Sidebar: `⚙️ Simulation Parameters`)

*   **Job Characteristics:**
    *   `Number of Compute Nodes Used`: Total nodes for the job
    *   `Job Duration (hours)`: Runtime in hours
    *   `Average Node Utilisation (%)`: Estimated average load across nodes

*   **Cluster Hardware & Datacentre:**
    *   `Power per Node - Idle (Watts)`: Node power consumption when idle
    *   `Power per Node - Peak Load (Watts)`: Node power consumption at maximum load
    *   `Data Centre PUE`: Power Usage Effectiveness value

*   **Hosting Location & Grid:**
    *   `Select Hosting Location`: Choose location with associated grid carbon intensity
    *   `Custom Carbon Intensity`: Manual entry option for specific values

### 2. Results Analysis (Main Area: `📊 Estimated Impact Results`)

*   **Job Impact Summary:**
    *   Average power per node
    *   Total energy consumption including PUE
    *   Carbon emissions in kg CO₂e

*   **Equivalencies:**
    *   Comparative metrics for emissions (driving distance, tree absorption)

### 3. Location Comparison (Main Area: `🗺️ Location Comparison`)

*   Bar chart showing emissions variation by location
*   Visual representation of grid carbon intensity impact

### 4. Model Assumptions

*   Documentation of model limitations and simplifications