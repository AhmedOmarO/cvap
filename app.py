# app.py
from flask import Flask, render_template, request, jsonify, session, flash, redirect, url_for
import os
import json
import logging
from werkzeug.utils import secure_filename
from resume_handler import ResumeHandler
from dotenv import load_dotenv
from llm_handler import LLMHandler

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

class FAQManager:
    def __init__(self, file_path='faq_responses.json'):
        self.file_path = file_path
        self.faqs = {}
        self.clear_faqs()

    def clear_faqs(self):
        self.faqs = {}
        self.save_faqs()

    def load_faqs(self):
        try:
            if os.path.exists(self.file_path):
                with open(self.file_path, 'r') as f:
                    self.faqs = json.load(f)
            return self.faqs
        except json.JSONDecodeError:
            return {}

    def save_faqs(self, new_faqs=None, mode='merge'):
        try:
            if new_faqs is not None:
                if mode == 'merge':
                    self.faqs.update(new_faqs)
                else:
                    self.faqs = new_faqs

            with open(self.file_path, 'w') as f:
                json.dump(self.faqs, f, indent=4)
            return True
        except Exception as e:
            app.logger.error(f"Error saving FAQs: {str(e)}")
            return False

app = Flask(__name__)

# Basic Flask configurations
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'a-default-secret-key-for-dev')
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB Max file size

# Ensure the 'uploads' directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize handlers
resume_handler = ResumeHandler(app.config['UPLOAD_FOLDER'])
faq_manager = FAQManager()
llm_handler = LLMHandler()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_faqs', methods=['GET'])
def get_faqs():
    faqs = faq_manager.load_faqs()
    return jsonify({'faqs': list(faqs.keys())})

@app.route('/get_response', methods=['POST'])
def get_response():
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({'response': "Invalid request."}), 400

    user_message = data.get('message', '')
    faqs = faq_manager.load_faqs()
    response_text = faqs.get(user_message, "I'm not sure about that. Please try an FAQ or rephrase.")
    return jsonify({'response': response_text})

@app.route('/manage_faqs', methods=['GET'])
def manage_faqs():
    faqs = faq_manager.load_faqs()
    return render_template('manage_faq.html', faqs=faqs)

@app.route('/save_faqs', methods=['POST'])
def save_faqs_route():
    questions = request.form.getlist('questions[]')
    answers = request.form.getlist('answers[]')
    
    new_faqs = {q.strip(): a.strip() for q, a in zip(questions, answers) if q and a}
    
    if faq_manager.save_faqs(new_faqs, mode='replace'):
        flash('FAQs have been successfully updated!', 'success')
    else:
        flash('Error saving FAQs. Please try again.', 'error')
    
    return redirect(url_for('manage_faqs'))

@app.route('/upload_resume', methods=['GET', 'POST'])
def upload_resume():
    app.logger.info("Uploading resume")
    
    if request.method == 'GET':
        return render_template('upload.html')

    try:
        if 'resume' not in request.files:
            app.logger.warning("Upload attempt with no 'resume' file part.")
            return jsonify({
                'success': False,
                'message': 'No file part in the request.',
                'word_count': 0,
                'confidence_score': 0.0,
                'extracted_text_path': None
            }), 400

        file = request.files['resume']
        if file.filename == '':
            app.logger.warning("Upload attempt with no file selected.")
            return jsonify({
                'success': False,
                'message': 'No file selected for upload.',
                'word_count': 0,
                'confidence_score': 0.0,
                'extracted_text_path': None
            }), 400

        if not resume_handler.allowed_file(file.filename):
            app.logger.warning(f"Upload attempt with disallowed file type: {file.filename}")
            return jsonify({
                'success': False,
                'message': f"Invalid file type: '{file.filename}'. Allowed: {', '.join(resume_handler.ALLOWED_EXTENSIONS)}.",
                'word_count': 0,
                'confidence_score': 0.0,
                'extracted_text_path': None
            }), 400

        app.logger.info(f"Processing uploaded file: {file.filename}")
        overall_success, result_obj = resume_handler.process_resume(file)
        app.logger.info(f"Resume processed: {overall_success}")
        app.logger.info(f"Resume result: {result_obj}")

        if overall_success and result_obj.is_valid and result_obj.extracted_text_path:
            app.logger.info(f"Resume validated: {file.filename}")
            flash('Resume uploaded and validated successfully!', 'success')
            
            # Check if it's an AJAX request
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({
                    'success': True,
                    'message': 'Resume uploaded and validated successfully!',
                    'word_count': result_obj.word_count,
                    'confidence_score': result_obj.confidence_score,
                    'redirect': url_for('manage_faqs')
                })
            else:
                # Regular form submission
                return redirect(url_for('manage_faqs'))
        else:
            error_message = result_obj.message if result_obj else "Unknown error occurred"
            app.logger.error(f"Resume processing failed: {error_message}")
            return jsonify({
                'success': False,
                'message': error_message,
                'word_count': result_obj.word_count if result_obj else 0,
                'confidence_score': result_obj.confidence_score if result_obj else 0.0,
                'extracted_text_path': None
            }), 400

    except Exception as e:
        app.logger.error(f"Error processing resume: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error processing resume: {str(e)}',
            'word_count': 0,
            'confidence_score': 0.0,
            'extracted_text_path': None
        }), 500

@app.route('/ask_question', methods=['POST'])
def ask_question():
    try:
        data = request.get_json()
        if not data or 'question' not in data:
            return jsonify({
                'success': False,
                'message': 'No question provided'
            }), 400

        question = data['question'].strip()
        if not question:
            return jsonify({
                'success': False,
                'message': 'Question cannot be empty'
            }), 400

        app.logger.info(f"Processing question: {question}")
        
        # Get the latest resume text
        latest_resume_path = None
        for filename in os.listdir(app.config['UPLOAD_FOLDER']):
            if filename.endswith('.txt'):
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                if latest_resume_path is None or os.path.getmtime(filepath) > os.path.getmtime(latest_resume_path):
                    latest_resume_path = filepath

        if latest_resume_path:
            with open(latest_resume_path, 'r') as f:
                resume_text = f.read()
                llm_handler.set_resume_text(resume_text)
        else:
            return jsonify({
                'success': False,
                'message': 'No resume has been uploaded yet. Please upload a resume first.'
            }), 400
        
        # Get answer from LLM
        answer = llm_handler.generate_answer(question)
        
        if not answer:
            return jsonify({
                'success': False,
                'message': 'Failed to generate answer'
            }), 500

        # Save the new Q&A pair
        new_faq = {question: answer}
        if faq_manager.save_faqs(new_faq, mode='merge'):
            return jsonify({
                'success': True,
                'message': 'Question answered successfully',
                'answer': answer
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to save the Q&A pair'
            }), 500

    except Exception as e:
        app.logger.error(f"Error processing question: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error processing question: {str(e)}'
        }), 500

@app.route('/delete_faq', methods=['POST'])
def delete_faq():
    try:
        data = request.get_json()
        if not data or 'question' not in data:
            return jsonify({
                'success': False,
                'message': 'No question provided for deletion'
            }), 400

        question = data['question']
        faqs = faq_manager.load_faqs()
        
        if question in faqs:
            del faqs[question]
            if faq_manager.save_faqs(faqs, mode='replace'):
                return jsonify({
                    'success': True,
                    'message': 'FAQ deleted successfully'
                })
            else:
                return jsonify({
                    'success': False,
                    'message': 'Failed to save changes after deletion'
                }), 500
        else:
            return jsonify({
                'success': False,
                'message': 'FAQ not found'
            }), 404

    except Exception as e:
        app.logger.error(f"Error deleting FAQ: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error deleting FAQ: {str(e)}'
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)