from flask import Flask, render_template, request
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

# Get Groq API key
api_key = os.getenv("GROQ_API_KEY")

client = Groq(
    api_key=api_key
)



@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/result", methods=["POST"])
def result():

    # Get data from HTML form
    task = request.form.get("task")
    text = request.form.get("text")

    if not text:
        return render_template(
            "result.html",
            result="Please enter some text."
        )

    if task == "explain":

        prompt = f"""
        Explain the following topic in simple language
        suitable for a beginner student.

        Topic:
        {text}

        Include:
        1. Simple definition
        2. Important points
        3. Simple example
        """

    elif task == "summarize":

        prompt = f"""
        Summarize the following text for a student.

        Give:
        - Short summary
        - Important points
        - Key terms

        Text:
        {text}
        """

    elif task == "mcq":

        prompt = f"""
        Create 5 multiple-choice questions based on
        the following topic.

        For each question provide:
        1. Question
        2. Four options (A, B, C, D)
        3. Correct answer
        4. Short explanation

        Topic:
        {text}
        """

    elif task == "interview":

        prompt = f"""
        Generate 2 interview questions for a student
        about the following topic.

        Include:
        - Question
        - Expected answer
        - One short explanation

        Topic:
        {text}
        """

    else:
        return render_template(
            "result.html",
            result="Invalid task selected."
        )

    try:

        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful AI study assistant."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_completion_tokens=1500
        )

        ai_result = response.choices[0].message.content

        return render_template(
            "result.html",
            result=ai_result,
            task=task
        )

    except Exception as e:

        return render_template(
            "result.html",
            result=f"Error: {str(e)}"
        )

if __name__ == "__main__":
    app.run(port=5001,debug=True)