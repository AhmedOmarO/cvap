from google import genai
from google.genai import types
import os
from typing import Dict
from dotenv import load_dotenv

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

    def generate_faqs_from_resume(self, resume_text: str) -> Dict[str, str]:
        """
        Generate FAQs from resume text using Google's Gemini AI model.
        Returns a dictionary of question-answer pairs.
        """
        try:
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