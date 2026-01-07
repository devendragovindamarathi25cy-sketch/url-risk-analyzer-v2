from flask import Flask, render_template, request
import re
from urllib.parse import urlparse

app = Flask(__name__)

def analyze_url(url):
    score = 0
    reasons = []

    # 1. HTTPS check
    if not url.startswith("https://"):
        score += 1
        reasons.append("HTTPS not used")

    # 2. URL shorteners
    shorteners = ["bit.ly", "tinyurl", "t.co", "goo.gl"]
    if any(s in url for s in shorteners):
        score += 2
        reasons.append("URL shortener detected")

    # 3. IP address instead of domain
    if re.match(r"https?://\d+\.\d+\.\d+\.\d+", url):
        score += 2
        reasons.append("IP address used instead of domain")

    # 4. Suspicious words
    suspicious_words = ["login", "verify", "secure", "update", "account"]
    if any(word in url.lower() for word in suspicious_words):
        score += 1
        reasons.append("Suspicious keyword in URL")

    # Risk level
    if score == 0:
        level = "Safe"
    elif score <= 2:
        level = "Low Risk"
    elif score <= 4:
        level = "Medium Risk"
    else:
        level = "High Risk"

    return level, score, reasons


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    score = 0
    reasons = []

    if request.method == "POST":
        url = request.form.get("url")
        result, score, reasons = analyze_url(url)

    return render_template(
        "index.html",
        result=result,
        score=score,
        reasons=reasons
    )


if __name__ == "__main__":
    app.run(debug=True)
