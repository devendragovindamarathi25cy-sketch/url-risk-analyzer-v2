from flask import Flask, render_template, request

app = Flask(__name__, template_folder="templates")

def analyze_url(url):
    score = 0
    reasons = []

    if url.startswith("http://"):
        score += 1
        reasons.append("Uses HTTP instead of HTTPS")

    if "login" in url.lower() or "verify" in url.lower():
        score += 2
        reasons.append("Suspicious keyword found")

    if url.count(".") > 4:
        score += 1
        reasons.append("Too many dots in URL")

    if score >= 4:
        risk = "HIGH RISK"
    elif score >= 2:
        risk = "MEDIUM RISK"
    elif score == 1:
        risk = "LOW RISK"
    else:
        risk = "SAFE"

    return risk, score, reasons


@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    score = None
    reasons = []

    if request.method == "POST":
        url = request.form["url"]
        result, score, reasons = analyze_url(url)

    return render_template("index.html",
                           result=result,
                           score=score,
                           reasons=reasons)


if __name__ == "__main__":
    app.run()
