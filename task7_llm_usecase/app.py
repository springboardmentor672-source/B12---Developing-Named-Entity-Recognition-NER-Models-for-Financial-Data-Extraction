from flask import Flask, render_template, request
from groq import Groq
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    if request.method == "POST":
        email_text = request.form["email"]
        tone = request.form["tone"]

        prompt = f"""
You are a professional corporate communication assistant.

Rewrite the following email in a {tone} tone.
Keep the meaning the same.
Improve clarity and professionalism.

Email:
{email_text}
"""

        try:
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0.9,
            )

            result = response.choices[0].message.content

        except Exception as e:
            result = f"Error: {str(e)}"

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)