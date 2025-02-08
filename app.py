from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

# Set your OpenAI API key (use environment variables for security)
# openai.api_key = os.getenv("OPENAI_API_KEY")

# Sample resume data
resume_data = {
    "name": "John Doe",
    "experience": "10 years in data science, specializing in machine learning and big data.",
    "skills": ["Python", "SQL", "Machine Learning", "Data Visualization"],
    "education": "M.Sc. in Data Science from XYZ University"
}

@app.route("/")
def index():
    return "Welcome to the Resume Chatbot!"

@app.route("/ask", methods=["POST"])
def ask():
    # question = request.json.get("question")
    # if not question:
    #     return jsonify({"error": "Please provide a question"}), 400
    
    # # Generate a response using OpenAI
    # response = openai.Completion.create(
    #     engine="text-davinci-003",
    #     prompt=f"Based on this resume data: {resume_data}, answer the following question: {question}",
    #     max_tokens=150
    # )
    
    # answer = response.choices[0].text.strip()
    return resume_data #jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(debug=True)


