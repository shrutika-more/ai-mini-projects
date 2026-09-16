from flask import Flask, render_template, request
from main import translate_text

app = Flask(__name__)


@app.route("/index")
def home():
    return render_template("index.html")

@app.route("/translate", methods=["POST"])
def translate():

    text = request.form["text"] 
    source = request.form["source"]
    target = request.form["target"]

    output = translate_text(   
        text,
        source,
        target
    )

    return render_template(
        "result.html",
        original=text,
        source=source,
        target=target,
        output=output
    )


if __name__ == "__main__":
    app.run(port=5004,debug=True)