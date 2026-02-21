from flask import Flask, jsonify, send_from_directory
import pandas as pd

app = Flask(__name__)

# Read latest row from Google Sheets CSV
def get_latest_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSSW7zGEzVSZky-3dcNuuADCT_h8_GCMv6o2KZTMPOpjioSZJU-To92DWVtiEc9999aeCu2xI_p1ji2/pub?gid=0&single=true&output=csv"
    df = pd.read_csv(url)
    latest = df.iloc[-1]
    return latest


def analyze_soil(data):

    moisture = float(data["Moisture"])
    light = float(data["Light"])
    temperature = float(data["Temperature"])
    ph = float(data["pH"])

    crop_data = pd.read_csv("crop_data.csv")

    recommendations = []
    advice = []
    remedies = []
    soil_summary = []

    # Soil condition
    if ph < 6:
        soil_summary.append("Soil is slightly acidic.")
        remedies.append("Add agricultural lime or wood ash.")

    elif ph > 7.5:
        soil_summary.append("Soil is alkaline.")
        remedies.append("Add gypsum or organic compost.")

    else:
        soil_summary.append("Soil pH is in ideal range.")

    # Moisture logic
    if moisture < 300:
        advice.append("Irrigation recommended to improve yield.")
        remedies.append("Use drip irrigation or mulching.")

    # Temperature logic
    if temperature > 32:
        advice.append("High temperature detected. Irrigate early morning.")

    # Crop recommendation using dataset
    for _, row in crop_data.iterrows():
        score = 0

        if row["Min_pH"] <= ph <= row["Max_pH"]:
            score += 40

        if row["Min_Temp"] <= temperature <= row["Max_Temp"]:
            score += 30

        if moisture > 400 and row["Moisture_Level"] == "High":
            score += 30
        elif 200 < moisture <= 400 and row["Moisture_Level"] == "Medium":
            score += 30
        elif moisture <= 200 and row["Moisture_Level"] == "Low":
            score += 30

        if score >= 50:
            recommendations.append(f"{row['Crop']} ({score}%)")

    return {
        "soil_summary": soil_summary,
        "crops": recommendations,
        "advice": advice,
        "remedies": remedies
    }


@app.route("/analyze")
def analyze():
    data = get_latest_data()
    result = analyze_soil(data)
    return jsonify(result)


@app.route("/")
def home():
    return send_from_directory(".", "index.html")


@app.route("/<path:path>")
def static_files(path):
    return send_from_directory(".", path)


if __name__ == "__main__":
    app.run(debug=True)
