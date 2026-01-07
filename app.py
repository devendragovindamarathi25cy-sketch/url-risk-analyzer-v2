from flask import Flask, render_template, request

app = Flask(__name__)

def url_risk_check(url):
    score = 0
    reasons = []

    if url.startswith("http://") is False and url.startswith("https://") is False:
        score += 1
        reasons.append("URL does not use HTTPS")

    suspicious_words = ["login", "verify", "secure", "bank", "update"]
    for word in suspicious_words:
        if word in url.lower():
            score += 1
            reasons.append(f"Suspicious word found: {word}")

    if score == 0:
        risk = "Low Risk"
    elif score <= 2:
        risk = "Medium Risk"
    else:
        risk = "High Risk"

    return risk, score, reasons


@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    score = None
    reasons = []

    if request.method == "POST":
        url = request.form.get("url")
        result, score, reasons = url_risk_check(url)

    return render_template("index.html",
                           result=result,
                           score=score,
                           reasons=reasons)


if __name__ == "__main__":
    app.run()
