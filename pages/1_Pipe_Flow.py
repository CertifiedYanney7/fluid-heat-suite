import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from engineering import Fluid, Pipe

st.set_page_config(page_title="Pipe Flow Analyser", page_icon="🚰", layout="wide")

st.title("🚰 Module A: Pipe Flow Analyser")
st.markdown("Calculate fluid velocity, Reynolds number, friction factor, and pressure drop across custom pipe geometries.")

# Sidebar Inputs
st.sidebar.header("Fluid Selection")
fluid_choice = st.sidebar.selectbox(
    "Select Fluid", ["Water", "Air", "Crude Oil", "User-Defined"]
)

if fluid_choice == "User-Defined":
    density = st.sidebar.number_input("Density (kg/m³)", value=1000.0, min_value=0.1)
    viscosity = st.sidebar.number_input("Dynamic Viscosity (Pa·s)", value=0.001, min_value=0.000001, format="%.6f")
    selected_fluid = Fluid(name="Custom", density=density, viscosity=viscosity)
else:
    selected_fluid = Fluid(name=fluid_choice)
    st.sidebar.info(f"**Density:** {selected_fluid.density} kg/m³\n\n**Viscosity:** {selected_fluid.viscosity} Pa·s")

st.sidebar.header("Pipe Geometry & Flow Rate")
diameter_mm = st.sidebar.number_input("Pipe Internal Diameter (mm)", value=50.0, min_value=1.0)
diameter = diameter_mm / 1000.0  # Convert mm to meters

length = st.sidebar.number_input("Pipe Length (m)", value=100.0, min_value=0.1)
roughness_mm = st.sidebar.number_input("Roughness ε (mm)", value=0.045, min_value=0.0, format="%.4f")
roughness = roughness_mm / 1000.0  # Convert mm to meters

flow_rate_lps = st.sidebar.number_input("Volumetric Flow Rate (L/s)", value=5.0, min_value=0.0)
flow_rate = flow_rate_lps / 1000.0  # Convert L/s to m³/s

# Calculations
try:
    pipe = Pipe(diameter=diameter, length=length, roughness=roughness)
    res = pipe.pressure_drop(selected_fluid, flow_rate)

    # Display Metric Cards
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Velocity", f"{res['velocity']:.2f} m/s")
    c2.metric("Reynolds No.", f"{res['reynolds']:,.0f}")
    c3.metric("Flow Regime", res["flow_regime"])
    c4.metric("Friction Factor", f"{res['friction_factor']:.4f}")
    c5.metric("Pressure Drop", f"{res['delta_p_bar']:.3f} bar")

    st.markdown("---")
    st.subheader("Interactive Plot: Pressure Drop vs. Flow Rate")

    # Generate data for graph
    max_q = max(flow_rate_lps * 2.0, 10.0)
    q_range_lps = np.linspace(0.1, max_q, 50)
    dp_list_bar = [pipe.pressure_drop(selected_fluid, q / 1000.0)["delta_p_bar"] for q in q_range_lps]

    plot_df = pd.DataFrame({"Flow_Rate_Lps": q_range_lps, "Pressure_Drop_bar": dp_list_bar})

    # Render Plot
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(plot_df["Flow_Rate_Lps"], plot_df["Pressure_Drop_bar"], color="crimson", lw=2, label="ΔP Curve")
    ax.axvline(flow_rate_lps, color="black", linestyle="--", label=f"Current Flow ({flow_rate_lps} L/s)")
    ax.set_xlabel("Flow Rate (L/s)")
    ax.set_ylabel("Pressure Drop (bar)")
    ax.set_title("Hydraulic System Curve")
    ax.grid(True, alpha=0.3)
    ax.legend()
    st.pyplot(fig)

    # CSV Download Button
    csv_data = plot_df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Export Results to CSV", data=csv_data, file_name="pipe_flow_results.csv", mime="text/csv")

except Exception as err:
    st.error(f"Error in calculations: {err}")