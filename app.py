from flask import Flask, render_template, request
import re

app = Flask(__name__)

# Banned / risky patterns (REAL LOGIC, NOT AI)
BANNED_KEYWORDS = [
    "login", "verify", "update", "secure", "account",
    "bank", "paypal", "free", "win", "reward"
]

SHORTENERS = [
    "bit.ly", "tinyurl", "t.co", "goo.gl", "ow.ly"
]


def analyze_url(url):
    score = 0
    reasons = []

    # Rule 1: IP address in URL
    if re.search(r"https?://\d+\.\d+\.\d+\.\d+", url):
        score += 2
        reasons.append("URL contains IP address")

    # Rule 2: URL shortener
    for s in SHORTENERS:
        if s in url.lower():
            score += 2
            reasons.append("URL uses shortener service")
            break

    # Rule 3: Suspicious keywords
    for word in BANNED_KEYWORDS:
        if word in url.lower():
            score += 1
            reasons.append(f"Suspicious keyword found: {word}")

    # Rule 4: Too many dots
    if url.count(".") > 4:
        score += 1
        reasons.append("URL contains too many dots")

    # Risk level
    if score >= 5:
        risk = "HIGH RISK"
    elif score >= 3:
        risk = "MEDIUM RISK"
    elif score >= 1:
        risk = "LOW RISK"
    else:
        risk = "SAFE"

    return risk, score, reasons


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    score = None
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
