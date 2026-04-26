from flask import Flask, render_template, request, jsonify
from fuzzy_engine import FuzzyEngine

app = Flask(__name__)
engine = FuzzyEngine()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/check", methods=["POST"])
def check():
    data = request.get_json()

    rasio   = float(data.get("rasio", 0))
    frekuensi = float(data.get("frekuensi", 0))
    urgensi = float(data.get("urgensi", 0))

    result = engine.evaluate(rasio, frekuensi, urgensi)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True, port=5001)
