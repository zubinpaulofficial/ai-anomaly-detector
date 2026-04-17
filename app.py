import streamlit as st
import pandas as pd
from pipeline.ingest import run_pipeline
from utils import clean_explanation

st.set_page_config(page_title="AI Anomaly Detector", layout="wide")

st.title("🚨 AI Anomaly Detection System")
st.write("Detect unusual financial transactions and explain them using AI")

# -----------------------
# SESSION STATE INIT
# -----------------------
if "df" not in st.session_state:
    st.session_state.df = None

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
    
    if st.button("Run Detection"):
        with st.spinner("Detecting anomalies..."):
            results = run_pipeline(df)

        if not results:
            st.success("No anomalies detected")
        else:
            st.error(f"{len(results)} anomalies found")

            for r in results:
                st.subheader(f"⚠️ User {r['user_id']}")
                st.write(f"Amount: £{r['amount']}")

                cleaned = clean_explanation(r["explanation"])

                for sentence in cleaned:
                    st.write(f"• {sentence}")
    
    st.caption(f"Rows: {len(df)}")

else:
    st.warning("Please upload a file or use sample data")