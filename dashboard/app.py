from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

@app.route("/")
def dashboard():

    df = pd.read_csv("data/prioritized_vulnerabilities.csv")

    vulnerabilities = df.to_dict(orient="records")

    total_vulns = len(df)
    high_risk = len(df[df["risk_score"] >= 5])
    medium_risk = len(df[(df["risk_score"] < 5) & (df["risk_score"] >= 3)])

    return render_template(
        "index.html",
        vulnerabilities=vulnerabilities,
        total_vulns=total_vulns,
        high_risk=high_risk,
        medium_risk=medium_risk
    )


if __name__ == "__main__":
    app.run(debug=True)