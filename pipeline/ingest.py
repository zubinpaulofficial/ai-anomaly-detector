from pipeline.detect import detect_anomalies
from pipeline.explain import generate_explanation

def run_pipeline(df):
    anomalies, mean, std = detect_anomalies(df)

    # convert dataframe → list of dicts
    anomalies = anomalies.to_dict(orient="records")

    # 🔥 Sort anomalies by severity
    anomalies = sorted(anomalies, key=lambda x: abs(x["z_score"]), reverse=True)

    TOP_K = 3  # limit LLM calls

    results = []

    for i, row in enumerate(anomalies):
        if i < TOP_K:
            explanation = generate_explanation(row, mean, std)
        else:
            explanation = f"""
- Amount (£{row['amount']}) exceeds anomaly threshold
- Z-score of {row['z_score']:.2f} indicates deviation
"""

        results.append({
            "user_id": row["user_id"],
            "amount": row["amount"],
            "z_score": row["z_score"],
            "explanation": explanation
        })

    return results, mean, std