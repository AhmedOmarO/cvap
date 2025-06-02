from llm_handler import LLMHandler

def test_faq_generation():
    # Sample resume text for testing
    sample_resume = """
    John Doe
    Software Engineer
    
    EXPERIENCE
    Senior Software Engineer | Tech Corp (2019-Present)
    - Led development of cloud-based applications using Python and AWS
    - Managed team of 5 developers for microservices architecture implementation
    - Improved system performance by 40% through optimization
    
    Software Developer | StartUp Inc (2017-2019)
    - Developed full-stack web applications using React and Node.js
    - Implemented CI/CD pipelines using Jenkins
    
    EDUCATION
    Master of Science in Computer Science
    Stanford University (2015-2017)
    
    SKILLS
    - Programming: Python, JavaScript, Java
    - Tools: Docker, Kubernetes, AWS
    - Frameworks: React, Node.js, Django
    """

    try:
        # Initialize LLM handler
        llm = LLMHandler()
        print("✅ LLM Handler initialized successfully")

        # Generate FAQs
        print("\nGenerating FAQs...")
        faqs = llm.generate_faqs_from_resume(sample_resume)

        if faqs:
            print("\n✅ FAQs generated successfully!")
            print(f"\nGenerated {len(faqs)} FAQ pairs:")
            print("-" * 50)
            for question, answer in faqs.items():
                print(f"\nQ: {question}")
                print(f"A: {answer}")
                print("-" * 50)
        else:
            print("❌ No FAQs were generated")

    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    test_faq_generation() 