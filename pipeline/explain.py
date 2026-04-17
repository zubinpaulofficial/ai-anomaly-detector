import requests

OLLAMA_URL = "http://localhost:11434/api/generate"

def generate_explanation(row, mean, std):
    user_id = row["user_id"]
    amount = row["amount"]

    # Calculate z-score safely
    z_score = (amount - mean) / std if std != 0 else 0

    prompt = f"""
    You are a financial fraud detection assistant.

    Explain why this transaction is anomalous.

    Transaction:
    - Amount: £{int(amount)}
    - Average: £{int(mean)}
    - Z-score: {round(z_score, 2)}

    Rules:
    - Output ONLY 3 bullet points
    - Each bullet must be short and clear
    - NO introductions or filler text
    - NO phrases like "based on data"

    Example:
    - Amount far exceeds normal behaviour
    - Significant deviation from historical pattern
    - Flagged as statistical outlier
    """

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        },
        timeout=10
    )

    return response.json()["response"].strip()