from sklearn.ensemble import IsolationForest

def detect_anomalies(df):
    model = IsolationForest(contamination=0.1, random_state=42)

    df["anomaly"] = model.fit_predict(df[["amount"]])

    # 🔥 Add statistical context
    mean = df["amount"].mean()
    std = df["amount"].std()

    df["avg_amount"] = mean
    df["z_score"] = (df["amount"] - mean) / std

    anomalies = df[df["anomaly"] == -1]

    return anomalies.drop(columns=["anomaly"]), mean, std