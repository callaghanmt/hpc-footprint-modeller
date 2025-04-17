import streamlit as st
import pandas as pd
import plotly.express as px
import datetime

# --- Configuration & Data ---

# Average Grid Carbon Intensity (gCO2e/kWh) - Example Data
# Source: Mix of sources like Electricity Maps, Ember, national reports (averages can vary!)
# It's crucial to use up-to-date, relevant data for a real workshop.
# Using 2023/2024 averages where possible as placeholders.
# Current date for context: Wednesday, April 16, 2025
LOCATION_CARBON_INTENSITY = {
    "Iceland (Hydro/Geo)": 10,
    "Norway (Hydro)": 15,
    "Sweden (Hydro/Nuclear/Wind)": 25,
    "France (Nuclear)": 55,
    "Ontario, Canada (Nuclear/Hydro)": 30,
    "Quebec, Canada (Hydro)": 5,
    "UK (Mixed, increasing Renewables)": 210,
    "California, USA (Mixed, high Solar)": 230,
    "Germany (Mixed, Coal phase-out)": 380,
    "US Average (Mixed)": 390,
    "Texas, USA (Mixed, high Wind/Gas)": 400,
    "China Average (Mixed, high Coal)": 540,
    "India (Mixed, high Coal)": 650,
    "Australia (Mixed, high Coal/Gas)": 600,
    "Poland (Coal Dominant)": 750,
    "Custom": None # Placeholder for manual entry
}

# Simplified Equivalency Factors (Use with caution, highly approximate)
# Source: EPA GHG Equivalency Calculator (approximations)
KM_PER_KG_CO2E = 1 / 0.175  # Approx km driven by average passenger car per kg CO2e
# Trees: Very complex, depends on type, age, location. Using a rough estimate.
# 1 mature tree sequesters ~20-25 kg CO2/year. 1 tonne = 1000 kg.
# So, ~40-50 trees sequester 1 tonne CO2/year.
TREES_PER_TONNE_CO2E_PER_YEAR = 45

# --- Helper Functions ---

def calculate_carbon_impact(num_nodes, job_duration_h, power_per_node_kw, pue, carbon_intensity_gco2e_kwh):
    """Calculates energy and carbon impact."""
    if None in [num_nodes, job_duration_h, power_per_node_kw, pue, carbon_intensity_gco2e_kwh] or carbon_intensity_gco2e_kwh < 0:
        return 0, 0 # Avoid calculation errors if inputs are invalid

    # Energy consumed by nodes
    total_node_energy_kwh = num_nodes * power_per_node_kw * job_duration_h

    # Total energy including data center overhead (PUE)
    total_dc_energy_kwh = total_node_energy_kwh * pue

    # Carbon emissions
    total_co2_g = total_dc_energy_kwh * carbon_intensity_gco2e_kwh
    total_co2_kg = total_co2_g / 1000.0

    return total_dc_energy_kwh, total_co2_kg

# --- Streamlit App Layout ---

st.set_page_config(layout="wide")

# Get current date
current_date_str = datetime.datetime.now().strftime("%Y-%m-%d")

st.title("HPC Job Carbon Footprint Estimator 🌍💡")
st.markdown(f"""
Welcome to the HPC Carbon Impact Modeller! This tool helps estimate the carbon footprint
of a high-performance computing job based on its characteristics and the location of the cluster.
Use the controls in the sidebar to configure a simulation.

*Disclaimer: This is a simplified model for educational purposes. Real-world impacts depend on many more factors,
including specific hardware, real-time grid fluctuations, cooling efficiency details, and embodied carbon.*
*Carbon intensity data is approximate and based on recent annual averages (as of {current_date_str}).*
""")

# --- Sidebar Inputs ---
with st.sidebar:
    st.header("⚙️ Simulation Parameters")

    st.subheader("Job Characteristics")
    num_nodes = st.number_input("Number of Compute Nodes Used", min_value=1, value=100, step=10)
    job_duration_h = st.number_input("Job Duration (hours)", min_value=0.1, value=24.0, step=1.0, format="%.1f")
    avg_utilization = st.slider("Average Node Utilisation (%)", min_value=0, max_value=100, value=75, step=5,
                                help="Average CPU/GPU load during the job. Affects power draw between idle and peak.")

    st.subheader("Cluster Hardware & Datacentre")
    power_idle_w = st.number_input("Power per Node - Idle (Watts)", min_value=10, value=150, step=10,
                                   help="Power consumed by one node when doing no work.")
    power_peak_w = st.number_input("Power per Node - Peak Load (Watts)", min_value=50, value=600, step=10,
                                   help="Maximum power consumed by one node under full load.")
    pue = st.slider("Data Center PUE (Power Usage Effectiveness)", min_value=1.0, max_value=3.0, value=1.5, step=0.05,
                    help="Ratio of total datacenter energy to IT equipment energy (1.0 is perfect efficiency). Typical values range from 1.1 to 2.0.")

    st.subheader("Hosting Location & Grid")
    location_options = list(LOCATION_CARBON_INTENSITY.keys())
    selected_location_option = st.selectbox("Select Hosting Location (determines Grid Carbon Intensity)",
                                            options=location_options, index=location_options.index("UK (Mixed, increasing Renewables)"))

    carbon_intensity_gco2e_kwh = LOCATION_CARBON_INTENSITY[selected_location_option]

    if selected_location_option == "Custom":
        carbon_intensity_gco2e_kwh = st.number_input("Custom Carbon Intensity (gCO₂e/kWh)", min_value=0, value=400, step=5,
                                                     help="Manually enter the grams of CO2 equivalent emitted per kilowatt-hour of electricity generated.")
    else:
        st.info(f"Average Intensity for {selected_location_option}: {carbon_intensity_gco2e_kwh} gCO₂e/kWh")

    # Validate inputs
    if power_idle_w > power_peak_w:
        st.error("Idle power cannot be greater than peak power.")
        st.stop() # Halt execution if inputs are illogical
    if carbon_intensity_gco2e_kwh is None or carbon_intensity_gco2e_kwh < 0:
         st.error("Please select a valid location or enter a non-negative custom carbon intensity.")
         st.stop()

# --- Main Area Calculations & Display ---
st.header("📊 Estimated Impact Results")

# Calculate power per node based on utilization (linear interpolation)
power_per_node_w = power_idle_w + (power_peak_w - power_idle_w) * (avg_utilization / 100.0)
power_per_node_kw = power_per_node_w / 1000.0

# Calculate total energy and carbon for the selected location
total_energy_kwh, total_co2_kg = calculate_carbon_impact(
    num_nodes, job_duration_h, power_per_node_kw, pue, carbon_intensity_gco2e_kwh
)

# Display Key Metrics
st.markdown("#### Job Impact Summary")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Avg. Power / Node", f"{power_per_node_w:,.1f} W")
with col2:
    st.metric("Total Energy Consumed", f"{total_energy_kwh:,.1f} kWh",
              help="Total electricity used by nodes and datacenter overhead (cooling, etc.)")
with col3:
    st.metric(f"Carbon Emissions ({selected_location_option})", f"{total_co2_kg:,.2f} kg CO₂e",
              help=f"Based on {carbon_intensity_gco2e_kwh} gCO₂e/kWh grid intensity.")


# Display Equivalencies
st.markdown("#### Context & Equivalencies")
if total_co2_kg > 0:
    km_driven = total_co2_kg * KM_PER_KG_CO2E
    miles_driven = km_driven * 0.621371
    total_co2_tonnes = total_co2_kg / 1000.0
    trees_years = total_co2_tonnes * TREES_PER_TONNE_CO2E_PER_YEAR

    col_eq1, col_eq2 = st.columns(2)
    with col_eq1:
        st.info(f"🚗 Equivalent to driving approximately **{km_driven:,.1f} km** ({miles_driven:,.1f} miles) in an average passenger car.")
    with col_eq2:
        st.info(f"🌳 Roughly equivalent to the CO₂ sequestered by **{trees_years:,.1f} mature trees** in one year.")
else:
    st.info("Run a simulation to see impact equivalencies.")

# --- Location Comparison ---
st.header("🗺️ Location Comparison")
st.markdown("""
How would the carbon footprint change if this *exact same job* were run on identical hardware
in a datacenter with the same PUE, but powered by different electricity grids?
""")

location_comparison_data = []
valid_locations = {loc: intensity for loc, intensity in LOCATION_CARBON_INTENSITY.items() if loc != "Custom" and intensity is not None}

for location, intensity in valid_locations.items():
    _, co2_kg = calculate_carbon_impact(
        num_nodes, job_duration_h, power_per_node_kw, pue, intensity
    )
    location_comparison_data.append({"Location": location, "Carbon Intensity (gCO₂e/kWh)": intensity, "Estimated Emissions (kg CO₂e)": co2_kg})

if location_comparison_data:
    df_comparison = pd.DataFrame(location_comparison_data)
    df_comparison = df_comparison.sort_values("Estimated Emissions (kg CO₂e)", ascending=True)

    fig = px.bar(df_comparison,
                 x="Location",
                 y="Estimated Emissions (kg CO₂e)",
                 title="Estimated Carbon Emissions by Hosting Location",
                 color="Carbon Intensity (gCO₂e/kWh)",
                 color_continuous_scale=px.colors.sequential.Reds,
                 hover_data=["Carbon Intensity (gCO₂e/kWh)"])

    fig.update_layout(xaxis_title="Hosting Location",
                      yaxis_title="Estimated Emissions (kg CO₂e)",
                      xaxis={'categoryorder':'total descending'}) # Show highest impact last if preferred

    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Could not generate location comparison data.")


# --- Assumptions ---
st.subheader("Model Assumptions & Simplifications")
st.markdown(f"""
*   **Constant Power Draw:** Assumes nodes run at the calculated average power (`{power_per_node_w:,.1f} W`) for the entire job duration. Real power fluctuates.
*   **Average Carbon Intensity:** Uses a single *average* carbon intensity value (`{carbon_intensity_gco2e_kwh} gCO₂e/kWh` for {selected_location_option}) for the grid. Real-time intensity varies significantly based on time of day and grid load.
*   **Constant PUE:** Assumes the selected PUE (`{pue}`) is constant. PUE can vary with load and external temperature.
*   **No Embodied Carbon:** Excludes emissions from manufacturing hardware, building the datacentre, etc.
*   **Simplified Equivalencies:** The driving and tree equivalencies are rough estimates for context.
*   **Hardware Homogeneity:** Assumes all nodes have the same power characteristics.
""")

st.markdown("---")
st.caption(f"App running as of {current_date_str}. Remember to use current, local data for accurate assessments.")
