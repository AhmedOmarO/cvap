# app.py
from flask import Flask, render_template, request, jsonify, session, flash, redirect, url_for
import os
import json
from werkzeug.utils import secure_filename # For secure file handling
from resume_handler import ResumeHandler   # Your resume_handler.py

app = Flask(__name__)

# Basic Flask configurations
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'a-default-secret-key-for-dev')
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB Max file size

# Ensure the 'uploads' directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize ResumeHandler (this is the version that does NOT take db arguments)
resume_handler = ResumeHandler(app.config['UPLOAD_FOLDER'])

# Load FAQ responses from JSON file (basic FAQ functionality)
try:
    with open('faq_responses.json', 'r') as f:
        faq_responses = json.load(f)
except FileNotFoundError:
    app.logger.warning("faq_responses.json not found. Using empty FAQs.")
    faq_responses = {} # Default to empty dict if file not found
except json.JSONDecodeError:
    app.logger.error("Error decoding faq_responses.json. Using empty FAQs.")
    faq_responses = {}


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_faqs', methods=['GET'])
def get_faqs():
    if isinstance(faq_responses, dict):
        return jsonify({'faqs': list(faq_responses.keys())})
    return jsonify({'faqs': []}) # Return empty list if not a dict

@app.route('/get_response', methods=['POST'])
def get_response():
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({'response': "Invalid request."}), 400
    user_message = data.get('message', '')
    
    response_text = faq_responses.get(user_message, "I'm not sure about that. Please try an FAQ or rephrase.")
            
    return jsonify({'response': response_text})

# --- Resume Upload Route ---
@app.route('/upload_resume', methods=['GET', 'POST'])
def upload_resume():
    if request.method == 'POST':
        if 'resume' not in request.files:
            app.logger.warning("Upload attempt with no 'resume' file part.")
            return jsonify({
                'success': False, 'message': 'No file part in the request.',
                'word_count': 0, 'confidence_score': 0.0, 'extracted_text_path': None
            }), 400

        file = request.files['resume']
        if file.filename == '':
            app.logger.warning("Upload attempt with no file selected.")
            return jsonify({
                'success': False, 'message': 'No file selected for upload.',
                'word_count': 0, 'confidence_score': 0.0, 'extracted_text_path': None
            }), 400

        if file and resume_handler.allowed_file(file.filename):
            app.logger.info(f"Processing uploaded file: {file.filename}")
            # process_resume from the non-DB version of ResumeHandler:
            # returns (bool: overall_processing_success, ResumeValidationResult_object)
            overall_success, result_obj = resume_handler.process_resume(file)
            
            response_data = {
                'success': overall_success and result_obj.is_valid, # True if processing AND content validation pass
                'message': result_obj.message,
                'word_count': result_obj.word_count,
                'confidence_score': result_obj.confidence_score,
                'extracted_text_path': result_obj.extracted_text_path # Path to .txt if valid
            }
            
            if overall_success and result_obj.is_valid:
                app.logger.info(f"Resume validated: {file.filename}. Text saved to: {result_obj.extracted_text_path}")
            elif overall_success and not result_obj.is_valid:
                app.logger.warning(f"Resume processed but content invalid: {file.filename}. Message: {result_obj.message}")
            else: # overall_success is False (problem with file save or text extraction)
                app.logger.error(f"Resume processing failed for {file.filename}. Message: {result_obj.message}")

            return jsonify(response_data)
        else:
            app.logger.warning(f"Upload attempt with disallowed file type: {file.filename}")
            return jsonify({
                'success': False, 
                'message': f"Invalid file type: '{file.filename}'. Allowed: {', '.join(resume_handler.ALLOWED_EXTENSIONS)}.",
                'word_count': 0, 'confidence_score': 0.0, 'extracted_text_path': None
            }), 400

    # For GET request, just show the upload page
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True, port=5001) # Explicitly set port