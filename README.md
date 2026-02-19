# AI-Text-PDF-Summarizer
Full-stack AI application to summarize text and PDF documents using LLMs



📌 Project Overview
The AI Text & PDF Summarizer is a full-stack web application that summarizes long text passages and multi-page PDF documents using Large Language Models (LLMs). It provides both paragraph and bullet-point summary modes to improve readability and quick information extraction.
This project demonstrates end-to-end integration of frontend, backend, API communication, and document processing.




🛠️ Tech Stack
Backend
Python
Flask (REST API development)
Groq LLM API (Large Language Model inference)
PyPDF2 (PDF text extraction)
Flask-CORS (Cross-origin support)
python-dotenv (Secure API key handling)
Frontend
HTML5
CSS3 (Custom UI styling)
JavaScript (Fetch API for backend communication)
Version Control
Git & GitHub



⚙️ How It Works
User enters text or uploads a PDF file.
Frontend sends data to Flask backend using Fetch API.
Backend:
Extracts text (if PDF uploaded)
Sends content to LLM API
Receives generated summary
Summary is returned as JSON response.
Frontend renders formatted summary (bullet list or paragraph).



Features
✅ Text summarization
✅ Multi-page PDF summarization
✅ Bullet and paragraph summary modes
✅ Real-time API response
✅ Clean and responsive UI
✅ Secure API key management using environment variables
