from flask import Flask, render_template, request
from main import generate_text

app = Flask(__name__)

@app.route("/home")
def home():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    prompt = request.form.get("prompt", "").strip()
    content_type = request.form.get("content_type", "Essay")
    tone = request.form.get("tone", "Professional")
    length = request.form.get("length", "Medium")

    if not prompt:
        return render_template(
            "index.html",
            error="Please enter a topic or instructions.",
            prompt=prompt,
            content_type=content_type,
            tone=tone,
            length=length
        )

    result = generate_text(
        prompt,
        content_type,
        tone,
        length
    )

    return render_template(
        "result.html",
        prompt=prompt,
        content_type=content_type,
        tone=tone,
        length=length,
        result=result
    )

if __name__ == "__main__":
    app.run(port=5003,debug=True)