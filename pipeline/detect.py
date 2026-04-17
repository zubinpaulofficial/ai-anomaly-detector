import pandas as pd

def detect_anomalies(df):
    # Ensure correct data types
    df = df.copy()
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")

    # Drop invalid rows
    df = df.dropna(subset=["amount"])

    # -----------------------
    # GLOBAL STATISTICS
    # -----------------------
    mean = df["amount"].mean()
    std = df["amount"].std()

    # Avoid division by zero
    if std == 0:
        df["z_score"] = 0
    else:
        df["z_score"] = (df["amount"] - mean) / std

    # -----------------------
    # ANOMALY LOGIC
    # -----------------------
    # Only keep strong anomalies
    anomalies = df[abs(df["z_score"]) > 2]

    # -----------------------
    # CLEAN OUTPUT
    # -----------------------
    anomalies = anomalies[["user_id", "amount", "z_score"]]

    return anomalies, mean, std