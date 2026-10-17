# SWYNEX-Intelligent-Feature

## Task 3: Intelligent Feature

Builds on Task 2 (Model Integration). This version adds:
1. **Error handling** - missing/corrupt FAQ file, empty or too-long user input, model load failures, and runtime errors are all caught with clear messages instead of the program crashing.
2. **A simple web interface** - a lightweight Flask app so anyone can ask a question in a browser instead of using the terminal.
3. **Expanded evaluation with explicit failure cases.**

### Files
- `qa_engine.py` - the core AI logic (model + error handling), used by both the web app and evaluation script
- `app.py` - simple Flask web interface
- `evaluate.py` - evaluation script; prints accuracy and lists failure cases separately
- `faq_data.csv` - FAQ dataset (20 Q&A pairs)
- `requirements.txt` - dependencies

### How to Run

**Web interface:**
```bash
pip install -r requirements.txt
python app.py
```
Then open the link shown in the terminal (usually http://127.0.0.1:5000) in a browser.

**Evaluation (accuracy + failure cases):**
```bash
python evaluate.py
```

### Error Handling Covered
- Missing or empty FAQ CSV file
- Malformed rows in the CSV (skipped instead of crashing)
- Empty user input ("Please type a question first.")
- Overly long input (>500 characters)
- Model loading failure (e.g., no internet on first run)
- Unexpected errors during matching (caught and shown as a friendly message)

### Known Failure Case
Query: "Where can I get a letter proving I am a student here?"
Expected: Bonafide certificate FAQ
Model returned: Transcript FAQ (score 0.51)
Reason: With only 20 FAQs and short questions, the model confuses similar "document request" questions. Fix: add more paraphrased FAQs per topic and raise the score threshold.

### Security
No API keys are used or stored in this repository.

Submitted as part of the SWYNEX Technologies Internship - Task 3.
