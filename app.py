from flask import Flask, render_template, request
import datetime as dt
import requests
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    details = None  # default to None for GET
    if request.method == "POST":
        user_in = request.form['nm']
        BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
        API_KEY = os.getenv("OPENWEATHER_API_KEY")  # Get API key from environment

        # Properly construct the URL with parameters
        url = f"{BASE_URL}?appid={API_KEY}&q={user_in}"

        try:
            response = requests.get(url)
            response.raise_for_status()  # Check if the request was successful
            data = response.json()

            if data.get("cod") != 200:
                details = f"Error: {data.get('message', 'Unable to fetch weather')}"
            else:
                temp_k = data['main']['temp']
                temp_celsius = round(temp_k - 273.15, 2)
                wind_speed = data['wind']['speed']
                humidity = data['main']['humidity']

                details = f"""Temperature in {user_in} is {temp_celsius}°C. 
                            Humidity: {humidity}%. 
                            Wind Speed: {wind_speed} m/s."""

        except requests.exceptions.RequestException as e:
            details = f"Error: {str(e)}"

    return render_template("index.html", details=details)

@app.route("/features")
def features():
    return render_template("features.html")

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)
