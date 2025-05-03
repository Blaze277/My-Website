from flask import Flask, render_template, request
import requests
import datetime as dt

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    details = None  # default to None for GET
    if request.method == "POST":
        user_in = request.form['nm']
        BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
        API_KEY = "ab193535430985048ce1bf0d716651c9"
        CITY = user_in

        # Properly construct the URL with parameters
        url = f"{BASE_URL}?appid={API_KEY}&q={CITY}"

        response = requests.get(url).json()

        if response.get("cod") != 200:
            details = f"Error: {response.get('message', 'Unable to fetch weather')}"
        else:
            temp_k = response['main']['temp']
            temp_celsius = round(temp_k - 273.15, 2)
            wind_speed = response['wind']['speed']
            humidity = response['main']['humidity']

            details = f"""Temperature in {CITY} is {temp_celsius}°C. 
                        Humidity: {humidity}%. 
                        Wind Speed: {wind_speed} m/s."""

    return render_template("index.html", details=details)

@app.route("/features")
def features():
    return render_template("features.html")

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)
