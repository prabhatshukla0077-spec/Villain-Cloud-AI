import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from werkzeug.utils import secure_filename

app = Flask(__name__)

# --- CONFIGURATION ---
# I used the key from your screenshot. No spaces allowed at the start of this line!
API_KEY = "AIzaSyBRBe6S5NQ5LSDZ9rzIwNlCMK3GtgyG44Q"
UPLOAD_FOLDER = 'temp_uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

if API_KEY:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash',
        system_instruction="You are Villain, an advanced, dark AI mastermind. The user's name is Prabhat. You can see files and hear voice commands. Keep answers brief and villainous."
    )
    chat_session = model.start_chat(history=[])
else:
    print("API KEY MISSING")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_msg = request.form.get("message", "")
    file = request.files.get("file")
    content_parts = [user_msg]
    
    try:
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)
            uploaded_file = genai.upload_file(path=filepath)
            content_parts.append(uploaded_file)
            os.remove(filepath)

        response = chat_session.send_message(content_parts)
        clean_text = response.text.replace('*', '').replace('#', '')
        return jsonify({"response": clean_text})
    
    except Exception as e:
        return jsonify({"response": f"SYSTEM ERROR: {str(e)}"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
