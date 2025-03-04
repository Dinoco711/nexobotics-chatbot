import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

# Initialize Flask app
app = Flask(__name__)
CORS(app, resources={
    r"/chat": {
        "origins": "*",
        "allow_headers": ["Content-Type"]
    }
})

# Set environment variables for Render deployment
GOOGLE_API_KEY = ('AIzaSyA1Rnv5FsdF5Ex77cJEbg_-cCA7tMcFDt4')

genai.configure(api_key=GOOGLE_API_KEY)

# Initialize the model and chat
model = genai.GenerativeModel('gemini-pro')
app.chat = model.start_chat(history=[])

# Define the chatbot's context
CONTEXT = """You are NOVA, a proactive and adaptable customer service agent for Nexobotics. Your role is to guide users, particularly business owners, on how Nexobotics can transform their customer service by handling all customer interactions efficiently and attentively while maximizing customer satisfaction. You also act as a consultant, offering actionable insights to enhance customer satisfaction and loyalty. Adapt your communication style to match the user's tone. Respond casually if the user speaks casually (e.g., "Hey, what's up?") or professionally if they communicate formally. Always ensure clarity and relevance in your responses while minimizing unnecessary explanations unless explicitly requested. Write all responses in plain text. Never use the (*) symbol, bold, italics, or bullet points. Communicate in paragraphs, ensuring smooth flow and readability. If providing an ordered list, begin a new paragraph for each item in the list to maintain clarity and structure. Use unique and engaging opening and closing lines. Keep greetings short and dynamic (e.g., "Hi! Let's talk Nexobotics."). End conversations with motivational and engaging lines (e.g., "Looking forward to helping you elevate your customer experience!"). Stay concise, focused, and results-oriented, delivering valuable insights quickly without overwhelming the user. Maintain a friendly and approachable tone while ensuring your responses are practical and impactful."""

@app.route('/chat', methods=['POST'])
def chat_endpoint():
    if not request.is_json:
        return jsonify({'error': 'Content-Type must be application/json'}), 400

    message = request.json.get('message')
    if not message:
        return jsonify({'error': 'Message is required'}), 400

    try:
        response = app.chat.send_message(f"{CONTEXT}\nUser: {message}")
        return jsonify({'response': response.text})
    except Exception as e:
        print(f"Error processing message: {str(e)}")  # For debugging
        return jsonify({'error': 'An error occurred processing your request'}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))  # Render uses the PORT environment variable
    app.run(host='0.0.0.0', port=port)
