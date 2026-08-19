import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Data Dashboard", page_icon="📊", layout="wide")

st.title("📊 Module C: Rock & Fluid Data Dashboard")
st.markdown("Upload petrophysical rock or fluid data, filter by properties, and analyze key distributions.")

# File Uploader
uploaded_file = st.file_uploader("Upload CSV Data File", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else:
    st.info("No file uploaded. Displaying default sample reservoir dataset.")
    try:
        df = pd.read_csv("sample_data.csv")
    except Exception:
        df = pd.DataFrame(
            {
                "Sample_ID": ["S1", "S2", "S3"],
                "Porosity_pct": [18.4, 15.2, 8.1],
                "Permeability_mD": [120.5, 45.2, 2.1],
            }
        )

# Display Summary Statistics
st.subheader("Raw Data Preview")
st.dataframe(df, use_container_width=True)

st.subheader("Summary Statistics")
st.dataframe(df.describe(), use_container_width=True)

# Interactive Filtering & Visualizations
if "Porosity_pct" in df.columns:
    st.sidebar.header("Filter Options")
    min_phi = float(df["Porosity_pct"].min())
    max_phi = float(df["Porosity_pct"].max())

    phi_cutoff = st.sidebar.slider(
        "Show samples where Porosity (%) >=",
        min_value=min_phi,
        max_value=max_phi,
        value=min_phi,
    )

    filtered_df = df[df["Porosity_pct"] >= phi_cutoff]

    st.subheader(f"Filtered Data (Porosity >= {phi_cutoff:.1f}%)")
    st.write(f"Showing **{len(filtered_df)}** of **{len(df)}** total samples.")
    st.dataframe(filtered_df, use_container_width=True)

    # Charts
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Chart 1: Porosity Distribution")
        fig1, ax1 = plt.subplots()
        ax1.hist(filtered_df["Porosity_pct"], bins=6, color="skyblue", edgecolor="black")
        ax1.set_xlabel("Porosity (%)")
        ax1.set_ylabel("Sample Count")
        ax1.grid(True, alpha=0.3)
        st.pyplot(fig1)

    with col2:
        if "Permeability_mD" in filtered_df.columns:
            st.markdown("### Chart 2: Porosity vs. Permeability Crossplot")
            fig2, ax2 = plt.subplots()
            ax2.scatter(filtered_df["Porosity_pct"], filtered_df["Permeability_mD"], color="darkgreen", alpha=0.7)
            ax2.set_yscale("log")
            ax2.set_xlabel("Porosity (%)")
            ax2.set_ylabel("Permeability (mD) [Log Scale]")
            ax2.grid(True, alpha=0.3)
            st.pyplot(fig2)

    # Export Filtered Data
    filtered_csv = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download Filtered CSV",
        data=filtered_csv,
        file_name="filtered_rock_data.csv",
        mime="text/csv",
    )