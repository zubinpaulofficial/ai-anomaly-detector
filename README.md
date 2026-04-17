# AI Anomaly Detection System

A production-style data application that detects anomalous financial transactions using statistical methods and explains them using AI.

---

## Overview

This project simulates a real-world fraud detection system used in financial platforms. It combines:

* **Statistical anomaly detection (Z-score)**
* **AI-generated explanations (LLM)**
* **Interactive data visualization (Plotly)**
* **End-to-end data pipeline architecture**

Users can upload transaction data or use a sample dataset to identify unusual activity and understand *why* a transaction is flagged.

---

## Features

### Anomaly Detection

* Uses **Z-score based detection**
* Flags transactions where deviation > 2 standard deviations
* Classifies risk levels:

  * 🔴 High Risk (>3σ)
  * 🟠 Medium Risk (>2σ)
  * 🟡 Low Risk

---

### AI Explanations

* Integrates with **HuggingFace LLM API**
* Generates concise, data-driven explanations
* Includes:

  * Deviation from mean
  * Relative magnitude
  * Statistical reasoning

---

### Interactive Visualization

* Built using **Plotly**
* Features:

  * Histogram of transaction distribution
  * Highlighted anomalies
  * Mean and threshold markers
  * Clean hover insights

---

### Intelligent Pipeline

* Modular architecture:

  * `detect.py` → anomaly detection
  * `ingest.py` → pipeline orchestration
  * `explain.py` → AI integration
  * `plots.py` → visualization layer
* Optimised:

  * Limits LLM calls (`TOP_K`) for efficiency
  * Fallback explanations if API fails

---

## Architecture

```text
User Input (CSV / Sample Data)
        ↓
Data Processing (Pandas)
        ↓
Anomaly Detection (Z-score)
        ↓
Top-K Anomalies
        ↓
AI Explanation (LLM API)
        ↓
Visualization (Plotly)
        ↓
Streamlit UI
```

---

## Live Demo

[*\[Streamlit App Link]*](https://ai-anomaly-detector-zubin.streamlit.app/)

---

## Tech Stack

* **Python**
* **Pandas / NumPy**
* **Streamlit**
* **Plotly**
* **HuggingFace Inference API**
* **Scikit-learn (optional extensions)**

---

## Project Structure

```text
ai-anomaly-detector/
│
├── app.py
├── utils.py
│
├── pipeline/
│   ├── detect.py
│   ├── ingest.py
│   └── explain.py
│
├── visualization/
│   └── plots.py
│
├── data/
│   └── transactions_2.csv
│
├── requirements.txt
└── README.md
```

---

## Running Locally

### 1. Clone the repo

```bash
git clone https://github.com/your-username/ai-anomaly-detector.git
cd ai-anomaly-detector
```

### 2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. API Key Setup (Optional)

If you're running this project locally, you may need to provide your HuggingFace API key so the app can generate AI explanations.

However, if you're deploying via Streamlit Cloud and have already added your key in the app settings, you can skip this step.

For local development, create `.streamlit/secrets.toml`:

```toml
HF_TOKEN = "your_huggingface_token"
```

---

### 5. Run app

```bash
streamlit run app.py
```

---

## Example Output

* Detects high-value anomalies (e.g. £25,000 transactions)
* Provides explanation like:

  * “£25,000 is 6.2x higher than average (£4,000)”
  * “Z-score of 4.4 indicates extreme statistical deviation”

---

## Key Highlights

* Designed like a **real-world fraud detection system**
* Combines **data engineering + analytics + AI**
* Optimised for **performance and cost (LLM calls)**
* Clean UI suitable for **stakeholder demos**

---

## Future Improvements

* Per-user behavioural anomaly detection
* Isolation Forest / ML-based detection
* Time-series anomaly tracking
* Real-time streaming pipeline (Kafka)
* Dashboard enhancements (filters, drill-down)

---

## Author

**Zubin Paul**
Data Engineer | Data Analyst
[LinkedIn](#) | [GitHub](#)

---