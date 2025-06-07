from google import genai
from google.genai import types
import os
from typing import Dict
from dotenv import load_dotenv
import json

class LLMHandler:
    def __init__(self):
        # Load environment variables
        load_dotenv()
        
        # Try to get API key from environment
        self.api_key = os.getenv('GOOGLE_API_KEY')
        
        if not self.api_key:
            raise ValueError("Google API key not found in environment variables")
        
        # Initialize the Gemini client
        self.client = genai.Client(api_key=self.api_key)
        
        # Store the resume text
        self.resume_text = None

    def set_resume_text(self, text: str):
        """Set the resume text to be used for generating answers
        
        Args:
            text: The resume text content
        """
        self.resume_text = text

    def generate_faqs_from_resume(self, resume_text: str) -> Dict[str, str]:
        """
        Generate FAQs from resume text using Google's Gemini AI model.
        Returns a dictionary of question-answer pairs.
        """
        try:
            # Store the resume text for future use
            self.set_resume_text(resume_text)
            
            # Prepare the prompt with specific formatting instructions
            prompt = f"""
            You are a recrutier that is screening my resume what would you like to know about me? generate 3 questions and answers that you would like to ask me.

            Resume text:
            {resume_text}

            Please generate the FAQ pairs in this exact format:
            Q: [Question]
            A: [Answer]

            Generate at least 3 but no more than 4 relevant questios.
            Make sure each answer is detailed and specific to the resume content.
            """

            # Generate content using Gemini
            short_config = types.GenerateContentConfig(max_output_tokens=2000)
            
            response = self.client.models.generate_content(
                model="gemini-2.0-flash-lite",
                contents=prompt,
                config=short_config,
            )
            
            # Get the generated text
            generated_text = response.text

            # Parse the response into Q&A pairs
            faqs = {}
            current_question = None
            current_answer = []

            for line in generated_text.split('\n'):
                line = line.strip()
                if not line:
                    continue
                
                if line.startswith('Q:'):
                    if current_question and current_answer:
                        faqs[current_question] = ' '.join(current_answer)
                    current_question = line[2:].strip()
                    current_answer = []
                elif line.startswith('A:'):
                    current_answer = [line[2:].strip()]
                elif current_answer is not None:
                    current_answer.append(line)

            # Add the last Q&A pair
            if current_question and current_answer:
                faqs[current_question] = ' '.join(current_answer)

            return faqs

        except Exception as e:
            print(f"Error generating FAQs: {str(e)}")
            return {} 

    def generate_answer(self, question: str) -> str:
        """Generate an answer for a user's question based on the resume content
        
        Args:
            question: The user's question
            
        Returns:
            str: The generated answer
        """
        try:
            if not self.resume_text:
                return "No resume has been uploaded yet. Please upload a resume first."

            prompt = f"""You are an AI assistant helping to answer questions about a resume.
            Please provide a clear and concise answer based on the resume content.
            If the information is not in the resume, say so.

            Resume text:
            {self.resume_text}

            Question: {question}

            Please provide a detailed answer based on the resume content.
            """
            
            short_config = types.GenerateContentConfig(max_output_tokens=2000)
            response = self.client.models.generate_content(
                model="gemini-2.0-flash-lite",
                contents=prompt,
                config=short_config,
            )
            
            return response.text
            
        except Exception as e:
            print(f"Error generating answer: {str(e)}")
            return None 