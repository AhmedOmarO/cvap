from flask import Flask, render_template, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
import json
import os
import threading

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///faq_responses.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'supersecretkey'  # Needed for session management
db = SQLAlchemy(app)

class SubmittedQuestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, server_default=db.func.now())
    question = db.Column(db.String(500), nullable=False)
    answer = db.Column(db.Text, nullable=False)

# Initialize the database
with app.app_context():
    if not os.path.exists('faq_responses.db'):
        db.create_all()

# Load FAQ responses from JSON file
with open('faq_responses.json', 'r') as f:
    faq_responses = json.load(f)

# Dictionary to hold locks for each user
user_locks = {}

def get_user_lock(user_id):
    """Retrieve or create a lock for the given user."""
    if user_id not in user_locks:
        user_locks[user_id] = threading.Lock()
    return user_locks[user_id]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_faqs', methods=['GET'])
def get_faqs():
    return jsonify({'faqs': list(faq_responses.keys())})

@app.route('/get_response', methods=['POST'])
def get_response():
    data = request.get_json()
    user_message = data.get('message', '')

    # Identify user (use session ID or a user token if available)
    user_id = session.get('user_id', request.remote_addr)  # Fallback to IP if no session

    lock = get_user_lock(user_id)

    # Ensure only one request per user is processed at a time
    with lock:
        response_text = faq_responses.get(user_message, "I'm not sure about that. Try an FAQ!")
        
        # Save question and answer to the database
        try:
            submitted_question = SubmittedQuestion(question=user_message, answer=response_text)
            db.session.add(submitted_question)
            db.session.commit()
        except Exception as e:
            print(f"Error saving question and answer: {e}")

    return jsonify({'response': response_text})

if __name__ == '__main__':
    app.run(debug=True)
