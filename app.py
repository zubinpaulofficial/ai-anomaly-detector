import streamlit as st
import pandas as pd
from pipeline.ingest import run_pipeline
from utils import clean_explanation
import matplotlib.pyplot as plt

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
    st.session_state.df = pd.DataFrame({
        "user_id": [1, 2, 3, 4, 5, 6, 7, 8],
        "amount": [100, 200, 150, 300, 12000, 250, 180, 15000]
    })

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

    results = st.session_state.results
    mean = st.session_state.mean

    # -----------------------
    # DISPLAY RESULTS
    # -----------------------
    if results is not None:
        if not results:
            st.success("No anomalies detected")
        else:
            st.error(f"{len(results)} anomalies found")

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

        fig, ax = plt.subplots()

        # Histogram
        ax.hist(df["amount"], bins=15, alpha=0.7)

        # Mean line
        ax.axvline(mean, linestyle="dashed", linewidth=2)

        # Highlight anomalies
        if results:
            anomaly_amounts = [r["amount"] for r in results]
            ax.scatter(anomaly_amounts, [0]*len(anomaly_amounts))

        # Labels
        ax.set_title("Transaction Distribution")
        ax.set_xlabel("Transaction Amount (£)")
        ax.set_ylabel("Frequency")

        st.pyplot(fig)

    else:
        st.warning("Please upload a file or use sample data")