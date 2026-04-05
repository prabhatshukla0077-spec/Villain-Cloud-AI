import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# ==========================================
# 1. CORE SYSTEM & API
# ==========================================
# Your API Key is integrated here. Keep this file safe!
API_KEY = "AIzaSyBPRvocNCncKxv29m2RLxHsML1SDNxSH0c"

# This variable holds Villain's ongoing memory
villain_chat = None

if API_KEY:
    genai.configure(api_key=API_KEY)
    
    # We build the Mastermind: We give him his brain and his permanent personality
    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash',
        system_instruction="You are Villain, an advanced, dark AI mastermind. The user's name is Prabhat. Keep your answers brief, futuristic, and slightly villainous."
    )
    
    # We open a continuous communication channel so he remembers the whole conversation
    villain_chat = model.start_chat(history=[])
else:
    print("WARNING: API Key not found!")

# ==========================================
# 2. THE CLOUD ROUTES
# ==========================================
@app.route('/')
def home():
    # This loads your futuristic index.html page
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_msg = request.json.get("message", "")
    
    if not villain_chat:
        return jsonify({"response": "SYSTEM ERROR: API Key missing or invalid."})
    
    try:
        # We send your message into his memory stream
        response = villain_chat.send_message(user_msg)
        
        # Clean up the text so it looks perfect on your hacking terminal
        clean_text = response.text.replace('*', '').replace('#', '')
        
        return jsonify({"response": clean_text})
    
    except Exception as e:
        print(f"Error: {e}") # This helps track down bugs in the Render logs
        return jsonify({"response": "SYSTEM ERROR: Communication with the Motherbrain failed."})

# Render uses Gunicorn to run this, but this allows you to test it on your PC too
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
