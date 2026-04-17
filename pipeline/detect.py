from sklearn.ensemble import IsolationForest

def detect_anomalies(df):
    model = IsolationForest(contamination=0.1, random_state=42)

    df["anomaly"] = model.fit_predict(df[["amount"]])

    # compute average
    avg_amount = df["amount"].mean()

    # relative feature
    df["is_high"] = df["amount"] > (avg_amount * 3)
    df["avg_amount"] = avg_amount

    anomalies = df[df["anomaly"] == -1]

    return anomalies.drop(columns=["anomaly"])