from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import json
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///faq_responses.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class FAQResponse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(500), nullable=False)
    answer = db.Column(db.Text, nullable=False)

class SubmittedQuestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(500), nullable=False)
    answer = db.Column(db.Text, nullable=False)

# Initialize the database
with app.app_context():
    if not os.path.exists('faq_responses.db'):
        db.create_all()
        # Load FAQ responses from JSON file and populate the database
            # for question, answer in faq_responses.items():
            #     faq_response = FAQResponse(question=question, answer=answer)
            #     db.session.add(faq_response)
            # db.session.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_faqs', methods=['GET'])
def get_faqs():
    # Send only the questions to the frontend
        with open('faq_responses.json', 'r') as f:
            faq_responses = json.load(f)
    questions = [faq.question for faq in faqs]
    return jsonify({'faqs': questions})

@app.route('/get_response', methods=['POST'])
def get_response():
    data = request.get_json()
    user_message = data.get('message', '')

    # Store the submitted question in the database

    # Get answer from database or provide default response
    faq_response = FAQResponse.query.filter_by(question=user_message).first()
    response_text = faq_response.answer if faq_response else "I'm not sure about that. Try an FAQ!"
    submitted_question = SubmittedQuestion(question=user_message,answer=response_text)
    db.session.add(submitted_question)
    db.session.commit()

    return jsonify({'response': response_text})

if __name__ == '__main__':
    app.run(debug=True)
