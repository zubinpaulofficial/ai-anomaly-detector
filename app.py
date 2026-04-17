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

        fig, ax = plt.subplots(figsize=(7, 3.5))

        # White background
        fig.patch.set_facecolor("white")
        ax.set_facecolor("white")

        # Histogram
        counts, bins, patches = ax.hist(
            df["amount"],
            bins=20,
            alpha=0.7
        )

        # Mean line
        ax.axvline(mean, linestyle="dashed", linewidth=2, label="Mean")

        # Highlight anomalies (thin vertical lines)
        if results:
            anomaly_amounts = [r["amount"] for r in results]

            for amt in anomaly_amounts:
                ax.axvline(amt, linewidth=2, alpha=0.6, label="Anomaly")

        # Remove duplicate legend entries
        handles, labels = ax.get_legend_handles_labels()
        unique = dict(zip(labels, handles))
        ax.legend(unique.values(), unique.keys())

        # Clean styling
        ax.set_title("Transaction Distribution", fontsize=10)
        ax.set_xlabel("Amount (£)", fontsize=6)
        ax.set_ylabel("Frequency", fontsize=6)

        # Light grid (not dark)
        ax.grid(alpha=0.2)

        # Remove top/right borders
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        st.pyplot(fig)

    else:
        st.warning("Please upload a file or use sample data")