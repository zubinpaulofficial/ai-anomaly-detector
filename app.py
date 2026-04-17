import streamlit as st
import pandas as pd
from pipeline.ingest import run_pipeline
from utils import clean_explanation
import numpy as np
from visualization.plots import plot_transaction_distribution

st.set_page_config(page_title="AI Anomaly Detector", layout="wide")

st.title("🚨 AI Anomaly Detection System")
st.write("Detect unusual financial transactions and explain them using AI")

# -----------------------
# SESSION STATE INIT
# -----------------------
if "df" not in st.session_state:
    st.session_state.df = None

if "results" not in st.session_state:
    st.session_state.results = None

if "mean" not in st.session_state:
    st.session_state.mean = None

if "std" not in st.session_state:
    st.session_state.std = None

# -----------------------
# FILE UPLOAD
# -----------------------
uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file:
    st.session_state.df = pd.read_csv(uploaded_file)

# -----------------------
# SAMPLE DATA BUTTON
# -----------------------
st.info("Or use sample data below")

if st.button("Use Sample Data"):
    try:
        st.session_state.df = pd.read_csv("data/transactions_2.csv")
        st.success("Sample dataset loaded")
    except Exception as e:
        st.error(f"Failed to load sample data: {e}")

df = st.session_state.df

# -----------------------
# RUN DETECTION
# -----------------------
if df is not None:
    st.write("### Data Preview")
    st.dataframe(df)
    st.caption(f"Rows: {len(df)}")

    if st.button("Run Detection"):
        with st.spinner("Detecting anomalies..."):
            results, mean, std = run_pipeline(df)

            # Store in session state
            st.session_state.results = results
            st.session_state.mean = mean
            st.session_state.std = std

    results = st.session_state.results
    mean = st.session_state.mean
    std = st.session_state.std


    if mean is not None and std is not None:
        upper = mean + 2 * std
        lower = mean - 2 * std
    else:
        upper, lower = None, None

    if results is not None:
        results = sorted(results, key=lambda x: abs(x["z_score"]), reverse=True)

    # -----------------------
    # DISPLAY RESULTS
    # -----------------------
    if results is not None:
        if not results:
            st.success("No anomalies detected")
        else:
            st.error(f"{len(results)} anomalies found")

            anomaly_ratio = len(results) / len(df)

            if anomaly_ratio > 0.1:
                st.error("🚨 High anomaly rate — potential fraud pattern")
            elif anomaly_ratio > 0.05:
                st.warning("⚠️ Moderate anomaly activity")
            else:
                st.success("✅ Low anomaly activity")

            for r in results:
                st.subheader(f"⚠️ User {r['user_id']}")

                # risk severity
                if abs(r["z_score"]) > 3:
                    st.error("🔴 High Risk")
                elif abs(r["z_score"]) > 2:
                    st.warning("🟠 Medium Risk")
                else:
                    st.info("🟡 Low Risk")

                # Amount + Z-score
                st.write(f"Amount: £{int(r['amount']):,}")
                st.write(f"Z-Score: {round(r['z_score'], 2)}")

                # Explanation
                cleaned = clean_explanation(r["explanation"])
                for sentence in cleaned:
                    st.write(f"• {sentence}")

    # -----------------------
    # VISUALIZATION
    # -----------------------
    if mean is not None:
        st.write("### Transaction Distribution")

        fig = plot_transaction_distribution(df, results, mean, std)

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Please upload a file or use sample data")