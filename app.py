from flask import Flask, render_template, request
import numpy as np

app = Flask(__name__)

# PM2.5 AQI breakpoints (US EPA)
AQI_BREAKPOINTS = [
    (0.0, 12.0, 0, 50),
    (12.1, 35.4, 51, 100),
    (35.5, 55.4, 101, 150),
    (55.5, 150.4, 151, 200),
    (150.5, 250.4, 201, 300),
    (250.5, 500.4, 301, 500),
]

def calculate_aqi(pm25):
    for c_low, c_high, aqi_low, aqi_high in AQI_BREAKPOINTS:
        if c_low <= pm25 <= c_high:
            return round(
                ((aqi_high - aqi_low) / (c_high - c_low)) *
                (pm25 - c_low) + aqi_low
            )
    return None

def classify_aqi(aqi):
    if aqi <= 50:
        return "Good 🟢", "Air quality is satisfactory."
    elif aqi <= 100:
        return "Moderate 🟡", "Sensitive individuals should reduce outdoor activity."
    elif aqi <= 150:
        return "Unhealthy for Sensitive Groups 🟠", "Limit prolonged exertion."
    elif aqi <= 200:
        return "Unhealthy 🔴", "Avoid outdoor activities."
    elif aqi <= 300:
        return "Very Unhealthy 🟣", "Health alert!"
    else:
        return "Hazardous ⚫", "Emergency conditions."

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        pm25 = float(request.form["pm25"])
        aqi = calculate_aqi(pm25)
        category, advice = classify_aqi(aqi)

        result = {
            "pm25": pm25,
            "aqi": aqi,
            "category": category,
            "advice": advice
        }

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
