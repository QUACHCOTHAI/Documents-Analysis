
# 📘 Document Q&A Web App (Powered by Gemini)

This web app allows users to upload documents (PDF, DOCX, TXT), ask questions based on the content, and view a history of Q&A interactions per document. It uses the **Gemini 1.5 API** via the official Python SDK.

## 🚀 Features

- Upload documents and extract text (supports PDF, DOCX, TXT).
- Ask questions about the uploaded document using a chatbot interface.
- View and persist Q&A history per document.
- Uses Gemini Flash model for fast and accurate responses.
- Clean and responsive UI (HTML + CSS + JS).
- Built with **Flask** (Python).

## 📁 Project Structure

```
document_qa_gemini/
│
├── app.py                   # Main Flask backend
├── history.json             # Stores chat history per document
├── uploads/                 # Stores uploaded documents
├── templates/
│   ├── index.html           # Main Q&A interface
│   └── history.html         # History view
├── .env                     # API key configuration (see below)
├── requirements.txt         # Required Python packages
└── README.md                # This file
```

## ⚙️ Setup Instructions

### 1. Clone or download this project

```bash
git clone https://github.com/yourname/document-qa-gemini.git
cd document-qa-gemini
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set your Gemini API key

Create a `.env` file in the root directory and add:

```env
GEMINI_API_KEY=your_api_key_here
Model_Name=your_model_name
```

> 🔑 You can get your API key from https://aistudio.google.com/app/apikey

### 4. Run the app

```bash
python app.py
```

Visit `http://127.0.0.1:5000` in your browser.

## 📝 Requirements

- Python 3.8+
- Flask
- google-generativeai
- python-dotenv
- PyMuPDF (`fitz`)
- python-docx

> All included in `requirements.txt`

## 📌 Notes

- Q&A context is limited to ~30,000 characters due to model input limits.
- History is stored in `history.json` with Unicode-safe encoding.
- Uploaded documents are stored locally in `uploads/`.
