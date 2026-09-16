from flask import Flask, render_template, request
from main import get_weather

app = Flask(__name__)


@app.route("/home")
def home():
    return render_template("index.html")

@app.route("/weather", methods=["POST"])
def weather():
    city = request.form.get("city", "Kolhapur").strip()
    state = request.form.get("state", "Maharashtra").strip()
    country = request.form.get("country", "India").strip()

    if not city or not state or not country:
        return render_template(
            "index.html",
            error="Please enter city, state and country.",
            city=city,
            state=state,
            country=country
        )

    try:
        result = get_weather(city, state, country)
    except Exception as e:
        print("WEATHER ERROR:", repr(e))
        return render_template(
            "index.html",
            error=f"Weather service error: {str(e)}",
            city=city,
            state=state,
            country=country
        )

    return render_template(
        "result.html",
        city=city,
        state=state,
        country=country,
        weather=result
    )


if __name__ == "__main__":
    app.run(port=5002,debug=True)