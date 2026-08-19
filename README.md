# Fluid Flow & Heat Transfer Engineering Suite

A complete, deployed, multi-page Streamlit web application providing calculation and visualization suites for fluid mechanics, thermodynamics, and petrophysical data analysis.

## Live Application
**Live App URL:** [https://share.streamlit.io/](https://share.streamlit.io/) *(Replace with your actual Streamlit Cloud URL after deployment)*

---

## Features
1. **Pipe Flow Analyser:** Darcy-Weisbach pressure drop calculations, Reynolds number determination, friction factor estimations (laminar & turbulent), and interactive performance curves.
2. **Heat Transfer Calculator:** 1D Fourier Law conduction through flat walls and transient Newton Cooling curve generation.
3. **Rock & Fluid Data Dashboard:** CSV data upload, summary statistics, porosity filtering, crossplots, and CSV export.

---

## AI Usage & Verification Log
In accordance with Module D requirements, AI tools were used to assist with initial code scaffolding:

1. **Prompt 1:** *"Write a Python class `Pipe` that implements Darcy-Weisbach pressure drop and friction factor calculation using Swamee-Jain equation."*
   - **Verification & Correction:** Verified formula accuracy against hand calculations. Adjusted friction factor switch to ensure exact $64/Re$ evaluation when $Re \le 2000$.

2. **Prompt 2:** *"Generate a multi-tab Streamlit interface for Newton's Law of Cooling with Matplotlib plots."*
   - **Verification & Correction:** Corrected logarithmic calculation for `time_to_target_temp` to prevent invalid domain errors when target temperature lies outside initial and ambient bounds.

3. **Prompt 3:** *"Create a Pandas script to filter reservoir rock data and generate a log-scale crossplot."*
   - **Verification & Correction:** Fixed log-scale axis limits when permeability contains zero or near-zero values.

---

## Local Setup Instructions
```bash
git clone <your-repo-url>
cd fluid-heat-suite
pip install -r requirements.txt
streamlit run app.py