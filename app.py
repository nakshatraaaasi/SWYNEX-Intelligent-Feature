"""
Simple web interface for the Student FAQ Bot (Task 3: Intelligent Feature).
Run: python app.py
Then open http://127.0.0.1:5000 in your browser.
"""

from flask import Flask, render_template_string, request
from qa_engine import SmartFAQBot, FAQLoadError

app = Flask(__name__)

try:
    bot = SmartFAQBot()
    load_error = None
except FAQLoadError as e:
    bot = None
    load_error = str(e)
except RuntimeError as e:
    bot = None
    load_error = str(e)

PAGE = """
<!doctype html>
<html>
<head>
  <title>Student FAQ Bot</title>
  <style>
    body { font-family: Arial, sans-serif; max-width: 600px; margin: 40px auto; }
    input[type=text] { width: 80%; padding: 8px; }
    button { padding: 8px 16px; }
    .answer { margin-top: 20px; padding: 12px; background: #f0f4ff; border-radius: 8px; }
    .error { color: #b00020; }
    .meta { color: #666; font-size: 0.85em; }
  </style>
</head>
<body>
  <h2>🎓 Student FAQ Bot</h2>
  <form method="POST">
    <input type="text" name="query" placeholder="Ask a question..." value="{{ query or '' }}">
    <button type="submit">Ask</button>
  </form>

  {% if load_error %}
    <p class="error">System error: {{ load_error }}</p>
  {% elif result %}
    <div class="answer">
      <strong>{{ result.answer }}</strong>
      <p class="meta">
        confidence: {{ result.score }}
        {% if result.matched_question %} | matched FAQ: "{{ result.matched_question }}"{% endif %}
      </p>
    </div>
  {% endif %}
</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    query = None
    if request.method == "POST":
        query = request.form.get("query", "")
        if bot:
            result = bot.get_answer(query)
    return render_template_string(PAGE, result=result, query=query, load_error=load_error)


if __name__ == "__main__":
    app.run(debug=True)
