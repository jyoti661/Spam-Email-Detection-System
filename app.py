from flask import Flask, render_template, request
import joblib
from spam import analyze_email
from collections import Counter

app = Flask(__name__)

# Load ML model
model = joblib.load("spam_model.pkl")
SPAM_THRESHOLD = 0.15

# -------- Routes --------
@app.route("/", methods=["GET", "POST"])
def index():
    results = []

    if request.method == "POST":
        email_text = request.form.get("email")

        # ---------- RULE-BASED ANALYSIS ----------
        rule_result = analyze_email(email_text)

        # ---------- ML ANALYSIS ----------
        ml_prob = model.predict_proba([email_text])[0][1]

        # ---------- HYBRID DECISION ----------
        final_is_spam = rule_result["is_spam"] or ml_prob > 0.3

        final_probability = max(
            rule_result["spam_probability"],
            round(ml_prob * 100, 2)
        )

        # ---------- TOP SPAM WORDS ----------
        keyword_counts = Counter(rule_result["matched_keywords"])
        top_spam_words = keyword_counts.most_common(5)

        results.append({
            "is_spam": final_is_spam,
            "spam_score": rule_result["spam_score"],
            "spam_probability": final_probability,
            "summary": rule_result["summary"],
            "risk_level": rule_result["risk_level"],
            "matched_keywords": rule_result["matched_keywords"],
            "top_spam_words": top_spam_words
        })

    return render_template("index.html", results=results)

if __name__ == "__main__":
    app.run(debug=True)
