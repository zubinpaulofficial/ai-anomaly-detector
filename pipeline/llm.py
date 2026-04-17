import subprocess
import re

def call_llm(prompt):
    result = subprocess.run(
        ["ollama", "run", "llama3"],
        input=prompt.encode(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    output = result.stdout.decode()

    # Remove terminal artifacts
    output = re.sub(r'\[.*?K', '', output)

    return output.strip()