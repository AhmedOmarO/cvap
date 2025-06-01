import os
from typing import Tuple, Optional
from werkzeug.utils import secure_filename
from PyPDF2 import PdfReader
from docx import Document
from dataclasses import dataclass
from flask import current_app
import uuid

@dataclass
class ResumeValidationResult:
    """Class to hold resume validation results"""
    is_valid: bool
    word_count: int
    confidence_score: float
    message: str

class ResumeHandler:
    """Handler for resume upload and validation"""
    
    ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}
    MIN_KEYWORDS = {'education'}
    MAX_WORD_COUNT = 1000
    
    def __init__(self, upload_folder: str):
        """Initialize the resume handler
        
        Args:
            upload_folder: Directory where resumes will be stored
        """
        self.upload_folder = upload_folder
        # Ensure upload directory exists
        os.makedirs(upload_folder, exist_ok=True)
    
    def allowed_file(self, filename: str) -> bool:
        """Check if file extension is allowed
        
        Args:
            filename: Name of the file to check
            
        Returns:
            bool: True if file extension is allowed
        """
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in self.ALLOWED_EXTENSIONS
    
    def save_file(self, file) -> Tuple[bool, str]:
        """Save uploaded file
        
        Args:
            file: File object from request
            
        Returns:
            Tuple[bool, str]: (success, filename/error message)
        """
        if file and self.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(self.upload_folder, filename)
            file.save(filepath)
            return True, filepath
        return False, "Invalid file type"
    
    #generate a function to generate a unique id for the resume
    def generate_unique_id(self) -> str:
        """Generate a unique ID for the resume
        
        Returns:
            str: Unique ID
        """
        return str(uuid.uuid4())

    ## TODO: map the unique id to the resume file name in a database table
    # def map_unique_id_to_filename(self, unique_id: str) -> str:
    #     """Map the unique ID to the resume file name in a database table
        
    #     Args:
    #         unique_id: Unique ID for the resume
    #     """
        # create a database table to map the unique id to the resume file name
        # the table should have the following columns:
        # - unique_id: str
        # - filename: str
        # - timestamp: datetime
        # - is_valid: bool
        # - confidence_score: float
        # - text: str
        # - is_processed: bool
        # - is_valid: bool
        # - is_processed: bool      
        


    def extract_text(self, filepath: str) -> Optional[str]:
        """Extract text from uploaded file
        
        Args:
            filepath: Path to the uploaded file
            
        Returns:
            Optional[str]: Extracted text or None if extraction failed
        """
        try:
            ext = filepath.rsplit('.', 1)[1].lower()
            
            if ext == 'pdf':
                reader = PdfReader(filepath)
                text = ""
                for page in reader.pages:
                    text += page.extract_text()
                return text
                
            elif ext == 'docx':
                doc = Document(filepath)
                return " ".join([paragraph.text for paragraph in doc.paragraphs])
                
            elif ext == 'txt':
                with open(filepath, 'r', encoding='utf-8') as f:
                    return f.read()
                    
        except Exception as e:
            current_app.logger.error(f"Error extracting text from {filepath}: {str(e)}")
            return None
    
    def count_words(self, text: str) -> int:
        """Count words in text, excluding common punctuation
        
        Args:
            text: Text to count words in
            
        Returns:
            int: Number of words
        """
        # Split by whitespace and filter out empty strings
        words = [word.strip('.,!?()[]{}:;"\'-') for word in text.split()]
        return len([word for word in words if word])
    
    def validate_resume(self, text: str) -> ResumeValidationResult:
        """Validate if the text appears to be a resume
        
        Args:
            text: Extracted text from the file
            
        Returns:
            ResumeValidationResult: Validation results
        """
        if not text:
            return ResumeValidationResult(
                is_valid=False,
                word_count=0,
                confidence_score=0.0,
                message="No text could be extracted from the file"
            )
        
        # Count words
        word_count = self.count_words(text)
        
        if word_count > self.MAX_WORD_COUNT:
            return ResumeValidationResult(
                is_valid=False,
                word_count=word_count,
                confidence_score=0.0,
                message=f"Text is too long ({word_count} words). Maximum allowed is {self.MAX_WORD_COUNT} words"
            )
        
        # Check for resume keywords
        text_lower = text.lower()
        keywords_found = sum(1 for keyword in self.MIN_KEYWORDS if keyword in text_lower)
        confidence_score = keywords_found / len(self.MIN_KEYWORDS)
        
        is_valid = confidence_score >= 0.6  # At least 60% of keywords found
        
        message = (
            "Resume validation successful!"
            if is_valid
            else "Text doesn't appear to be a resume. Missing key sections or information."
        )
        
        return ResumeValidationResult(
            is_valid=is_valid,
            word_count=word_count,
            confidence_score=confidence_score,
            message=message
        )
    
    def process_resume(self, file) -> Tuple[bool, ResumeValidationResult]:
        """Process and validate uploaded resume
        
        Args:
            file: Uploaded file object
            
        Returns:
            Tuple[bool, ResumeValidationResult]: (success, validation results)
        """
        # Save the file
        success, result = self.save_file(file)
        if not success:
            return False, ResumeValidationResult(
                is_valid=False,
                word_count=0,
                confidence_score=0.0,
                message=result
            )
        
        # Extract text
        text = self.extract_text(result)
        if text is None:
            return False, ResumeValidationResult(
                is_valid=False,
                word_count=0,
                confidence_score=0.0,
                message="Failed to extract text from file"
            )
        
        # Validate resume
        validation_result = self.validate_resume(text)
        
        # Clean up file if validation failed
        if not validation_result.is_valid:
            try:
                os.remove(result)
            except Exception as e:
                current_app.logger.error(f"Error removing file {result}: {str(e)}")
        else:
            ## save text to upload folder with the same name as the file
            # generate a unique id for the resume
            unique_id = self.generate_unique_id()
            # save text to upload folder with the same name as the file
            with open(os.path.join(self.upload_folder, unique_id + '.txt'), 'w') as f:
                f.write(text)
            
            # save the resume to the database
            
        return True, validation_result 