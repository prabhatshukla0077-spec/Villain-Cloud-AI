import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from werkzeug.utils import secure_filename

app = Flask(__name__)

# --- CONFIGURATION ---
  OPENROUTER_API_KEY = "AIzaSyBRBe6S5NQ5LSDZ9rzIwNlCMK3GtgyG44Q"

# Model list — openrouter/free auto-picks any available free model.
# Others are fallbacks in case of rate limits.
MODELS = [
    "openrouter/auto",                          # auto-picks best free model available
    "meta-llama/llama-3.3-70b-instruct:free",  # llama fallback
    "deepseek/deepseek-chat-v3-0324:free",      # deepseek fallback
    "qwen/qwen3-235b-a22b:free",               # qwen fallback
    "google/gemma-3-27b-it:free",               # gemma fallback
]

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
        # If a document or image is uploaded
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)
            
            # Upload to Google's temporary File API
            uploaded_file = genai.upload_file(path=filepath)
            content_parts.append(uploaded_file)
            
            # Clean up local file
            os.remove(filepath)

        # Send both text and file to Villain
        response = chat_session.send_message(content_parts)
        clean_text = response.text.replace('*', '').replace('#', '')
        
        return jsonify({"response": clean_text})
    
    except Exception as e:
        return jsonify({"response": f"SYSTEM ERROR: {str(e)}"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
