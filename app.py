import streamlit as st

st.set_page_config(
    page_title="Fluid & Heat Suite",
    page_icon="⚙️",
    layout="wide",
)

st.title("⚙️ Fluid Flow & Heat Transfer Engineering Suite")
st.markdown("---")

st.markdown(
    """
### Welcome to the Engineering Calculation Suite
This multi-page application provides interactive tools for fluid mechanics, thermodynamics, and petrophysical data analysis.

#### Available Modules:
1. **Pipe Flow Analyser:** Calculate velocity, Reynolds number, friction factor, and pressure drops across custom pipe geometry with dynamic flow curve plotting.
2. **Heat Transfer Calculator:** Model 1D steady-state conduction through flat walls and dynamic Newton's Law of Cooling curves.
3. **Rock & Fluid Data Dashboard:** Load, filter, analyze, and visualize petrophysical sample datasets.

---
*Use the sidebar menu on the left to navigate between modules.*
"""
)