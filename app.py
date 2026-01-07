from flask import Flask, render_template, request

app = Flask(__name__)

def check_url_risk(url):
    score = 0
    reasons = []

    if url.startswith("http://"):
        score += 1
        reasons.append("Uses insecure HTTP")

    if any(word in url.lower() for word in ["login", "verify", "secure", "account", "update"]):
        score += 1
        reasons.append("Contains suspicious keywords")

    if url.count('.') > 3:
        score += 1
        reasons.append("Too many dots")

    if score == 0:
        risk = "Safe"
    elif score == 1:
        risk = "Low Risk"
    elif score == 2:
        risk = "Medium Risk"
    else:
        risk = "High Risk"

    return risk, score, reasons

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    score = None
    reasons = None

    if request.method == "POST":
        url = request.form.get("url")
        result, score, reasons = check_url_risk(url)

    return render_template("index.html", result=result, score=score, reasons=reasons)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
