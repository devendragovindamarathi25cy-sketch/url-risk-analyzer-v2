from flask import Flask, render_template, request
import re

app = Flask(__name__)

def analyze_url(url):
    score = 0
    reasons = []

    if re.search(r"(bit\.ly|tinyurl|t\.co)", url):
        score += 2
        reasons.append("URL shortener used")

    if url.startswith("http://"):
        score += 1
        reasons.append("HTTPS not used")

    if re.search(r"(login|verify|update|secure|account)", url.lower()):
        score += 2
        reasons.append("Suspicious keywords found")

    if re.search(r"https?://\d+\.\d+\.\d+\.\d+", url):
        score += 2
        reasons.append("IP address used instead of domain")

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
    score = None
    reasons = []

    if request.method == "POST":
        url = request.form.get("url")
        if url:
            result, score, reasons = analyze_url(url)

    return render_template(
        "index.html",
        result=result,
        score=score,
        reasons=reasons
    )


if __name__ == "__main__":
    app.run(debug=True)