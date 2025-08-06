from flask import Flask, render_template, request
from weather_scraper import get_weather_data

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    weather = None
    if request.method == "POST":
        weather = get_weather_data()
    return render_template("index.html", weather=weather)

if __name__ == "__main__":
    app.run(debug=True)
