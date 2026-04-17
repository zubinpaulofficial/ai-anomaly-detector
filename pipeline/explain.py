import requests

OLLAMA_URL = "http://localhost:11434/api/generate"

def generate_explanation(row):
    user_id = row["user_id"]
    amount = row["amount"]

    prompt = f"""
    You are a financial fraud detection assistant.

    Explain why the following transaction is anomalous.

    Transaction:
    - User ID: {user_id}
    - Amount: £{amount}

    Rules:
    - Be concise and direct
    - DO NOT include introductions, summaries, or filler text
    - DO NOT say things like "Based on the provided data"
    - DO NOT repeat the question
    - Output ONLY bullet points
    - Each bullet point must be a short, clear reason
    - Each bullet must be a COMPLETE sentence on ONE line

    Output format:
    - Reason 1
    - Reason 2
    - Reason 3
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