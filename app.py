import os
import uuid
import json, docx, csv
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from dotenv import load_dotenv
import fitz  # PyMuPDF
from pyngrok import ngrok

'''
DEFAULT_PROMPT = """
    Bạn là một trợ lý AI phân tích nội dung tài liệu. 
    Trả lời chính xác, ngắn gọn và súc tích, dựa hoàn toàn vào nội dung tài liệu được cung cấp.
    Trả lời và giải thích câu hỏi dưới dạng danh sách hoặc liệt kê. 
    Nếu tài liệu không có đủ thông tin để trả lời, hãy nói rõ ràng rằng không có thông tin.
    """
full_prompt = f"{DEFAULT_PROMPT}\n\nTài liệu:\n{context[:30000]}\n\nCâu hỏi: {question}"
'''

# Cấu hình Gemini API
load_dotenv()
key = os.environ.get("GEMINI_API_KEY")
llm = os.environ.get("ModelName")
genai.configure(api_key=key)  # Hoặc dùng os.environ.get("GEMINI_API_KEY")
model = genai.GenerativeModel(llm)

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
HISTORY_FILE = 'history.json'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
if not os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, 'w') as f:
        json.dump({}, f)

def read_file_content(path):
    ext = path.lower().split('.')[-1]
    if ext == 'txt':
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    elif ext == 'pdf':
        return read_pdf(path)
    elif ext == 'docx':
        return read_docx(path)
    else:
        return f"(Không hỗ trợ định dạng .{ext})"

def read_pdf(path):
    text = ""
    doc = fitz.open(path)
    for page in doc:
        text += page.get_text()
    doc.close()
    return text

def read_docx(path):
    doc = docx.Document(path)
    return '\n'.join(p.text for p in doc.paragraphs)

def answer_with_gemini(context, question):
    prompt = f"Tài liệu:\n{context[:30000]}\n\nCâu hỏi: {question}"  # Giới hạn kích thước
    response = model.generate_content(prompt)
    return response.text.strip()

def load_history():
    if not os.path.exists(HISTORY_FILE):
        return {}

    try:
        with open(HISTORY_FILE, "r", encoding='utf-8') as f:
            content = f.read().strip()
            if not content:
                return {}  # Nếu file rỗng, trả về dict rỗng
            return json.loads(content)
    except json.JSONDecodeError:
        return {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file:
        file_id = str(uuid.uuid4())
        filename = file_id + "_" + file.filename
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        return jsonify({'success': True, 'file_id': file_id, 'filename': filename})
    return jsonify({'success': False})

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    filename = data['filename']
    question = data['question']
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    context = read_file_content(filepath)
    if context.startswith("(Không hỗ trợ"):
        return jsonify({'answer': context})

    answer = answer_with_gemini(context, question)

    # Load & ghi lại lịch sử
    history = load_history()
    if filename not in history:
        history[filename] = []
    history[filename].append({'question': question, 'answer': answer})

    try:
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
    except Exception as e:
        return jsonify({'answer': f"Lỗi khi lưu lịch sử: {str(e)}"})

    return jsonify({'answer': answer})

@app.route('/history')
def history():
    with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
        data = load_history()
    return render_template('history.html', data=data)

if __name__ == '__main__':
    # Lấy port từ biến môi trường hoặc mặc định là 5000
    port = int(os.environ.get("PORT", 5000))

    # Tạo tunnel ngrok tới port đó
    # public_url = ngrok.connect(port)
    # print(" * Ngrok tunnel URL:", public_url)

    # Chạy Flask app trên port đó
    app.run(debug=True, port=port)
