import re

def clean_explanation(text: str):
    if not text:
        return []

    # -----------------------
    # REMOVE WEIRD TOKENS
    # -----------------------
    text = re.sub(r"\[.*?\]", "", text)

    # -----------------------
    # FIX BROKEN FORMATTING
    # -----------------------
    text = text.replace("\n", " ")  # join broken lines
    text = text.replace("•", "-")   # normalize bullets

    # Fix common LLM glitches
    text = text.replace("Z Score", "Z-score")
    text = text.replace("Z  score", "Z-score")
    text = text.replace("Z score", "Z-score")

    # -----------------------
    # SPLIT INTO BULLETS
    # -----------------------
    parts = re.split(r"\s*-\s*", text)

    cleaned = []
    buffer = ""

    for part in parts:
        part = part.strip()

        if not part:
            continue

        # Merge short broken fragments
        if buffer:
            buffer += " " + part
            cleaned.append(buffer.strip())
            buffer = ""
        else:
            if len(part.split()) < 4:
                buffer = part
            else:
                cleaned.append(part)

    # -----------------------
    # REMOVE JUNK / FILLER
    # -----------------------
    cleaned = [
        p for p in cleaned  # ✅ FIXED (was 'parts' before ❌)
        if not any(x in p.lower() for x in [
            "here's why",
            "based on",
            "following reasons",
            "i identify",
            "this transaction is anomalous due to"
        ])
    ]

    # -----------------------
    # TRIM VERBOSITY
    # -----------------------
    cleaned = [p.strip() for p in cleaned if len(p.split()) > 3]

    # Limit to top 2 strongest points (dashboard clarity)
    return cleaned[:2]