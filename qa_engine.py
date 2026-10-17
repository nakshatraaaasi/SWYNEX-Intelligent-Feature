"""
Core Q&A engine with error handling (Task 3: Intelligent Feature).
Reused by both app.py (web interface) and evaluate.py.
"""

import csv
import os
from sentence_transformers import SentenceTransformer, util

MODEL_NAME = "all-MiniLM-L6-v2"
THRESHOLD = 0.40


class FAQLoadError(Exception):
    pass


def load_faq(path="faq_data.csv"):
    if not os.path.exists(path):
        raise FAQLoadError(f"FAQ file not found: {path}")
    questions, answers = [], []
    try:
        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if not row.get("question") or not row.get("answer"):
                    continue  # skip malformed rows instead of crashing
                questions.append(row["question"])
                answers.append(row["answer"])
    except csv.Error as e:
        raise FAQLoadError(f"Could not parse FAQ file: {e}")
    if not questions:
        raise FAQLoadError("FAQ file is empty or invalid.")
    return questions, answers


class SmartFAQBot:
    def __init__(self, faq_path="faq_data.csv"):
        self.questions, self.answers = load_faq(faq_path)
        try:
            self.model = SentenceTransformer(MODEL_NAME)
        except Exception as e:
            raise RuntimeError(
                "Could not load the AI model. Check your internet connection "
                f"for the first-time download. Details: {e}"
            )
        self.q_embeddings = self.model.encode(self.questions, convert_to_tensor=True)

    def get_answer(self, query):
        # --- error handling for bad input ---
        if query is None or not str(query).strip():
            return {
                "answer": "Please type a question first.",
                "score": 0.0,
                "matched_question": None,
                "status": "empty_input",
            }
        query = str(query).strip()
        if len(query) > 500:
            return {
                "answer": "That question is too long, please shorten it.",
                "score": 0.0,
                "matched_question": None,
                "status": "input_too_long",
            }

        try:
            q_emb = self.model.encode(query, convert_to_tensor=True)
            scores = util.cos_sim(q_emb, self.q_embeddings)[0]
            best = int(scores.argmax())
            score = float(scores[best])
        except Exception as e:
            return {
                "answer": "Something went wrong while processing your question. Please try again.",
                "score": 0.0,
                "matched_question": None,
                "status": f"model_error: {e}",
            }

        if score < THRESHOLD:
            return {
                "answer": "I don't know this yet. Please contact the college office.",
                "score": round(score, 2),
                "matched_question": None,
                "status": "low_confidence",
            }

        return {
            "answer": self.answers[best],
            "score": round(score, 2),
            "matched_question": self.questions[best],
            "status": "ok",
        }
