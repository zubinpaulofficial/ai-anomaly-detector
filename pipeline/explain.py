import requests

OLLAMA_URL = "http://localhost:11434/api/generate"

def generate_explanation(row, mean, std):
    user_id = row["user_id"]
    amount = row["amount"]

    # Calculate z-score safely
    z_score = (amount - mean) / std if std != 0 else 0

    prompt = f"""
        You are a financial fraud detection system.

        Explain why this transaction is anomalous.

        Transaction:
        - Amount: £{amount}
        - Average: £{mean:.2f}
        - Z-score: {z_score:.2f}

        STRICT RULES:
        - ONLY bullet points
        - MAX 2 bullets
        - Each bullet must be ONE short sentence
        - Use numbers (comparisons)
        - NO introductions
        - NO explanations like "based on data"
        - NO repetition
        - Compare amount to average
        - Mention z-score threshold

        Example:
        - £12000 is 3.4x higher than average (£3500)
        - Z-score 3.9 indicates extreme deviation
    """

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": "llama3",
                "prompt": prompt,
                "stream": False
            },
            timeout=60
        )

        return response.json()["response"].strip()

    except Exception:
        # FALLBACK LOGIC
        return f"""
        - Amount (£{amount}) is significantly higher than average (£{mean:.2f})
        - Z-score of {z_score:.2f} indicates strong statistical deviation
        - Transaction exceeds expected behaviour range
        """