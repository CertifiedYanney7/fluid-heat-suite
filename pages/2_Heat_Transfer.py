import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from engineering import HeatTransfer

st.set_page_config(page_title="Heat Transfer Calculator", page_icon="🔥", layout="wide")

st.title("🔥 Module B: Heat Transfer Calculator")
st.markdown("Analyze 1D steady-state heat conduction and transient Newton's cooling processes.")

tab1, tab2 = st.tabs(["1D Steady-State Conduction", "Newton's Law of Cooling"])

# ---------------------------------------------------------
# TAB 1: Conduction
# ---------------------------------------------------------
with tab1:
    st.subheader("1D Steady-State Conduction (Fourier's Law)")
    st.caption("Heat rate equation: $Q = \\frac{k \\cdot A \\cdot (T_1 - T_2)}{L}$")

    col1, col2 = st.columns(2)
    with col1:
        k = st.number_input(
            "Thermal Conductivity, k (W/m·K)",
            value=0.8,
            min_value=0.01,
            help="Property indicating material's ability to conduct heat (e.g., Concrete ≈ 0.8, Steel ≈ 50)."
        )
        area = st.number_input(
            "Surface Area, A (m²)",
            value=10.0,
            min_value=0.1,
            help="Cross-sectional area perpendicular to heat transfer direction."
        )
        thickness = st.number_input(
            "Wall Thickness, L (m)",
            value=0.2,
            min_value=0.001,
            help="Distance across the wall through which heat travels."
        )

    with col2:
        t_in = st.number_input("Inside Temperature, T1 (°C)", value=25.0)
        t_out = st.number_input("Outside Temperature, T2 (°C)", value=15.0)

    try:
        q_watts = HeatTransfer.conduction_flat_wall(k, area, thickness, t_in, t_out)
        st.success(f"**Heat Loss Rate (Q):** `{q_watts:.2f} W` ({q_watts / 1000.0:.3f} kW)")
    except Exception as err:
        st.error(f"Error: {err}")

# ---------------------------------------------------------
# TAB 2: Newton's Law of Cooling
# ---------------------------------------------------------
with tab2:
    st.subheader("Transient Cooling Process (Newton's Law of Cooling)")
    st.caption("Cooling equation: $T(t) = T_\\infty + (T_0 - T_\\infty)e^{-k_c t}$")

    col_a, col_b = st.columns(2)
    with col_a:
        t0 = st.slider("Initial Temperature, T0 (°C)", min_value=30.0, max_value=150.0, value=90.0)
        t_inf = st.slider("Ambient Temperature, T∞ (°C)", min_value=-10.0, max_value=40.0, value=20.0)

    with col_b:
        kc = st.slider("Cooling Constant, kc (1/min)", min_value=0.01, max_value=0.50, value=0.05, step=0.01)
        t_target = st.slider("Target Temperature (°C)", min_value=float(t_inf + 1.0), max_value=float(t0 - 1.0), value=40.0)

    try:
        time_needed = HeatTransfer.time_to_target_temp(t0, t_target, t_inf, kc)
        st.metric("Time to Reach Target Temperature", f"{time_needed:.2f} minutes")

        # Generate Plot Data
        max_t = max(time_needed * 1.5, 30.0)
        time_array = np.linspace(0, max_t, 100)
        temp_array = [HeatTransfer.newton_cooling_temperature(t, t0, t_inf, kc) for t in time_array]

        # Render Cooling Curve Plot
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(time_array, temp_array, color="royalblue", lw=2, label="Body Temp T(t)")
        ax.axhline(t_inf, color="gray", linestyle=":", label=f"Ambient ({t_inf}°C)")
        ax.scatter([time_needed], [t_target], color="red", zorder=5, label=f"Target ({t_target}°C @ {time_needed:.1f}m)")
        ax.set_xlabel("Time (minutes)")
        ax.set_ylabel("Temperature (°C)")
        ax.set_title("Cooling Curve vs Time")
        ax.grid(True, alpha=0.3)
        ax.legend()
        st.pyplot(fig)

    except Exception as ex:
        st.error(f"Error: {ex}")