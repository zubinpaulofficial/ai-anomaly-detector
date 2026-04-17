import pandas as pd
from pipeline.detect import detect_anomalies
from pipeline.explain import generate_explanation


def run_pipeline(df):
    anomalies = detect_anomalies(df)

    results = []

    for _, row in anomalies.iterrows():
        explanation = generate_explanation(row)

        results.append({
            "user_id": row["user_id"],
            "amount": row["amount"],
            "explanation": explanation
        })

    return results