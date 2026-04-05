import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from werkzeug.utils import secure_filename

app = Flask(__name__)

# --- CONFIGURATION ---
API_KEY = "AIzaSyBRBe6S5NQ5LSDZ9rzIwNlCMK3GtgyG44Q"
UPLOAD_FOLDER = 'temp_uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

if API_KEY:
    genai.configure(api_key=API_KEY)
    # UPDATED MODEL NAME: Using 'gemini-1.5-flash' explicitly
    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash',
        system_instruction="You are Villain, an advanced, dark AI mastermind. The user's name is Prabhat. You can see files and hear voice commands. Keep answers brief and villainous."
    )
    # This creates the session properly
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
    content_parts = []
    
    # Only add text if it exists
    if user_msg:
        content_parts.append(user_msg)
    
    try:
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)
            
            # Uploading the file to Gemini
            uploaded_file = genai.upload_file(path=filepath)
            content_parts.append(uploaded_file)
            os.remove(filepath)

        # Send the gathered parts
        response = chat_session.send_message(content_parts)
        clean_text = response.text.replace('*', '').replace('#', '')
        return jsonify({"response": clean_text})
    
    except Exception as e:
        # If it still fails, let's see the exact error message
        return jsonify({"response": f"VILLAIN CORE ERROR: {str(e)}"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
