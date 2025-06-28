from flask import Flask, render_template
import requests

app = Flask(__name__)

WEATHER_API_KEY = "9c232fdd060b3a1fda4c78ec782afd1f"

def get_location():
    try:
        response = requests.get("https://ipinfo.io/json", timeout=5)
        response.raise_for_status()
        data = response.json()
        return data.get("city", "Unknown")
    except Exception as e:
        print("Location error:", e)
        return None

def get_weather(city):
    try:
        url = (
            f"http://api.openweathermap.org/data/2.5/weather?"
            f"q={city}&appid={WEATHER_API_KEY}&units=metric"
        )
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        return {
            "city": data["name"],
            "temperature": f"{data['main']['temp']} °C",
            "description": data["weather"][0]["description"].title(),
            "humidity": f"{data['main']['humidity']}%",
            "wind": f"{data['wind']['speed']} m/s",
        }
    except Exception as e:
        print("Weather fetch error:", e)
        return None

def get_background_class(description):
    """Return CSS class name based on weather description."""
    desc = description.lower()
    if "cloud" in desc:
        return "cloudy"
    elif "rain" in desc:
        return "rainy"
    elif "clear" in desc:
        return "clear"
    elif "snow" in desc:
        return "snowy"
    elif "storm" in desc or "thunder" in desc:
        return "stormy"
    else:
        return "default"

@app.route("/")
def index():
    city = get_location()
    weather = get_weather(city) if city else None
    background_class = get_background_class(weather["description"]) if weather else "default"
    return render_template("index.html", weather=weather, bg_class=background_class)

if __name__ == "__main__":
    app.run(debug=True)
