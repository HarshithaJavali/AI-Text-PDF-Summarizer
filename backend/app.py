# ------------------- LOAD ENV FIRST -------------------
from dotenv import load_dotenv
load_dotenv()   # ⬅️ THIS IS CRITICAL

# ------------------- IMPORTS -------------------
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from PyPDF2 import PdfReader
from groq import Groq

# ------------------- APP SETUP -------------------
app = Flask(__name__)
CORS(app)

# ------------------- DEBUG CHECK (OPTIONAL, SAFE) -------------------
print("GROQ_API_KEY loaded:", bool(os.getenv("GROQ_API_KEY")))

# ------------------- GROQ CLIENT -------------------
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

MODEL_NAME = "llama-3.1-8b-instant"

# ------------------- HELPER FUNCTION -------------------
def generate_summary(text, mode):
    if mode == "bullet":
        prompt = f"""
Summarize the following text into clear bullet points.
Use * for bullets.

Text:
{text}
"""
    else:
        prompt = f"""
Summarize the following text clearly in a paragraph.

Text:
{text}
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "You are a professional summarization assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content


# ------------------- TEXT SUMMARY API -------------------
@app.route("/summarize", methods=["POST"])
def summarize_text():
    data = request.get_json()

    text = data.get("text", "")
    mode = data.get("mode", "normal")

    if not text.strip():
        return jsonify({"error": "No text provided"}), 400

    summary = generate_summary(text, mode)

    return jsonify({
        "mode": mode,
        "summary": summary
    })


# ------------------- PDF SUMMARY API -------------------
@app.route("/summarize-pdf", methods=["POST"])
def summarize_pdf():
    if "file" not in request.files:
        return jsonify({"error": "No PDF file uploaded"}), 400

    pdf_file = request.files["file"]
    mode = request.form.get("mode", "normal")

    if pdf_file.filename == "":
        return jsonify({"error": "Empty file"}), 400

    reader = PdfReader(pdf_file)
    full_text = ""

    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            full_text += extracted + "\n"

    if not full_text.strip():
        return jsonify({"error": "No text extracted from PDF"}), 400

    summary = generate_summary(full_text, mode)

    return jsonify({
        "filename": pdf_file.filename,
        "mode": mode,
        "summary": summary
    })


# ------------------- RUN SERVER -------------------
if __name__ == "__main__":
    print("🚀 Starting Flask server...")
    app.run(host="127.0.0.1", port=5000, debug=True)
