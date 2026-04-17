import requests
import os
import streamlit as st

# HF_TOKEN = os.getenv("HF_TOKEN")
HF_TOKEN = st.secrets["HF_TOKEN"]

API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-base"

headers = {
    "Authorization": f"Bearer {HF_TOKEN}"
}

def generate_explanation(row, mean, std):
    user_id = row["user_id"]
    amount = row["amount"]

    z_score = (amount - mean) / std if std != 0 else 0

    prompt = f"""
#         You are a financial fraud detection system.

#         Explain why this transaction is anomalous.

#         Transaction:
#         - Amount: £{amount}
#         - Average: £{mean:.2f}
#         - Z-score: {z_score:.2f}

#         STRICT RULES:
#         - ONLY bullet points
#         - MAX 2 bullets
#         - Each bullet must be ONE short sentence
#         - Use numbers (comparisons)
#         - NO introductions
#         - NO explanations like "based on data"
#         - NO repetition
#         - Compare amount to average
#         - Mention z-score threshold

#         Example:
#         - £12000 is 3.4x higher than average (£3500)
#         - Z-score 3.9 indicates extreme deviation
#     """

    try:
        response = requests.post(
            API_URL,
            headers=headers,
            json={"inputs": prompt},
            timeout=15
        )

        output = response.json()[0]["generated_text"]

        return output.strip()

    except Exception:
        return f"""
        - £{amount} deviates significantly from mean (£{mean:.0f})
        - Potential anomaly based on statistical threshold
        """