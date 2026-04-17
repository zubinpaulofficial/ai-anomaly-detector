from pipeline.detect import detect_anomalies
from pipeline.explain import generate_explanation

def run_pipeline(df):
    anomalies, mean, std = detect_anomalies(df)

    results = []

    for _, row in anomalies.iterrows():
        explanation = generate_explanation(row, mean, std)

        results.append({
            "user_id": row["user_id"],
            "amount": row["amount"],
            "z_score": row["z_score"],
            "explanation": explanation
        })

    return results, mean, std