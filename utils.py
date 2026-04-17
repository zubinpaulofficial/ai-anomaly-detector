import re

def clean_explanation(text: str):
    if not text:
        return []

    # Remove weird tokens like [3D K]
    text = re.sub(r"\[.*?\]", "", text)

    # Fix broken lines (join lines that shouldn't be separate bullets)
    text = text.replace("\n", " ")

    # Normalize bullet markers
    text = text.replace("•", "-")

    # Split into bullet candidates
    parts = re.split(r"\s*-\s*", text)

    cleaned = []
    buffer = ""

    for part in parts:
        part = part.strip()

        if not part:
            continue

        # If previous line looks incomplete, merge it
        if buffer:
            buffer += " " + part
            cleaned.append(buffer.strip())
            buffer = ""
        else:
            # If sentence looks incomplete (ends abruptly), store temporarily
            if len(part.split()) < 4:
                buffer = part
            else:
                cleaned.append(part)

    return cleaned