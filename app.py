from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# FAQ stored in Flask (More scalable)
faq_responses = {
    "📌 What is Ahmed Omar's current job?": "Ahmed Omar Eissa is a Senior Data Scientist at Uber, working in Competition Analytics | Global Strategy and Planning.",
    "📌 What are Ahmed Omar’s key skills?": "His skills include Python, SQL, A/B Testing, Machine Learning, PowerBI, Tableau, Data Engineering, and Geo-Spatial Analysis.",
    "Can you share your top technical experiences and their business impact?": """
    Certainly! Here are three key technical projects I’ve led that had a significant business impact at Uber:

1️⃣ 📈 Automated Uber’s Restaurant Sales Process – $6M+ Annual Savings

I built an automated workflow for restaurant acquisition, reducing manual effort and improving efficiency.
This resulted in $6M in annual cost savings, a shorter sales cycle, and increased Gross Bookings (GB).
By accelerating merchant onboarding, Uber expanded its market presence and revenue growth.
2️⃣ 📊 Developed Self-Service Analytics Tools – Empowered 100+ Stakeholders

I designed and implemented self-service analytics platforms, enabling operations, sales, and finance teams to access insights without technical support.
This reduced reliance on data teams, accelerated decision-making, and improved operational efficiency.
The tools streamlined reporting and forecasting, leading to better strategic planning.
3️⃣ 🔬 Led A/B Testing for Customer Retention – Improved Engagement & CLV

I designed and executed A/B testing experiments to refine Uber’s customer engagement and retention strategies.
These insights helped shape marketing campaigns, pricing models, and operational policies, ensuring data-backed decisions.
The results directly increased customer lifetime value (CLV) and optimized business performance.
Each of these projects combined technical innovation with strategic impact, driving efficiency, cost savings, and business growth at Uber.""",

    "📌 What are Ahmed Omar’s achievements at Uber?": "Ahmed developed a Global Merchant-Focused Expansion Strategy, automated restaurant sales saving $6M per year, designed A/B Testing experiments, and built self-service analytics tools.",
    "📌 What companies has Ahmed worked for?": """ 
    <div class="message-section">
    Ahmed has a total of 10 years of experices, 
    He joined Uber 7 years ago and currently working as a senior data scientist @ Uber (2018 - Present).
    Before joing Uber, he wored as a business intellegence engineer @ Vodafone in Cairo (2017 - 2018).Ahmed also worked as a consultant @ ProCons-4it (2016 - 2017) building BI solutions to many customers in the middle east. 
    His career started as an <b>intern</b> in <b>SAP</b>, where he got intensitve trainings about data science, machine learning and AI. 
     </div>
     """,
    "📌 What is Ahmed Omar’s experience in Data Science?": """

        <div class="message-section">
            <div class="message-title"><span class="emoji">📌</span> Ahmed Omar Eissa: A Well-Rounded Data Scientist</div>
            <p>Ahmed Omar Eissa is a well-rounded Data Scientist with a strong foundation in 
            <span class="highlight">data engineering, machine learning, business analytics, and leadership</span>. With <b>10 years of experience</b>, he has worked across <b>strategy, automation, and data-driven decision-making</b> at a global scale. His expertise spans  <span class="highlight">technical depth, business impact, and leadership exposure</span>.</p>
        </div>

        <div class="message-section">
            <div class="message-title"><span class="emoji">1️⃣</span> A Data Scientist with Strong Engineering Skills</div>
            <ul class="message-bullet">
                <li>Proficient in <span class="highlight">SQL, Python, Spark, Hive, and Airflow</span>, ensuring efficient <span class="highlight">data processing and pipeline automation</span>.</li>
                <li>Designed and maintained <span class="highlight">centralized data infrastructure</span>, improving <span class="highlight">data accessibility and reliability</span> for analytics teams.</li>
                <li>Developed <span class="highlight">forecasting models and real-time dashboards</span> using tools like <span class="highlight">FB Prophet, Tableau, and PowerBI</span> to drive strategic insights.</li>
                <li>Created <span class="highlight">self-service analytics platforms</span>, reducing dependency on engineering teams and accelerating decision-making across business units.</li>
            </ul>
        <p></p> 
        </div>

        <div class="message-section">
            <div class="message-title"><span class="emoji">2️⃣</span> A Business-Oriented Data Scientist Driving Impact</div>
            <ul class="message-bullet">
                <li>Automated <span class="highlight">Uber’s restaurant sales process</span>, saving <span class="highlight">$6M annually</span>, shortening sales cycles, and boosting <span class="highlight">Gross Bookings (GB)</span>.</li>
                <li>Developed <span class="highlight">competition analytics solutions</span> that provided <span class="highlight">market intelligence</span> to inform <span class="highlight">global expansion strategies</span>.</li>
                <li>Designed <span class="highlight">A/B testing frameworks</span> to optimize <span class="highlight">customer engagement and retention</span>, ensuring data-driven decision-making.</li>
                <li>Built <span class="highlight">scalable analytics solutions</span> that empowered <span class="highlight">100+ stakeholders in Sales, Operations, and Finance</span> to extract insights efficiently.</li>
            </ul>
        <p></p>
        </div>

        <div class="message-section">
            <div class="message-title"><span class="emoji">3️⃣</span> A Leader with Cross-Functional Influence</div>
            <ul class="message-bullet">
                <li><span class="highlight">Partnered with Sales, Product, and Ops teams</span> to integrate <span class="highlight">data science into strategic decision-making</span>, ensuring business success.</li>
                <li>Mentored and trained <span class="highlight">junior data scientists and analysts</span>, fostering a data-driven culture across teams.</li>
                <li>Led the <span class="highlight">development of automation packages</span>, reducing <span class="highlight">development time and improving deployment efficiency</span> for analytics solutions.</li>
                <li>Acted as a <span class="highlight">bridge between engineering and business teams</span>, translating complex data insights into <span class="highlight">actionable business strategies</span>.</li>
            </ul>
        <p></p>
        </div>

        <div class="message-section">
            <div class="message-title"><span class="emoji">🌟</span> Why This Matters?</div>
            <ul class="message-bullet">
                <li><span class="emoji">📌</span> <b>Technical Strength:</b> Expertise in <span class="highlight">data engineering, machine learning, and analytics</span> ensures robust and scalable solutions.</li>
                <li><span class="emoji">📌</span> <b>Business Impact:</b> Projects drive <span class="highlight">cost savings, operational efficiency, and revenue growth</span>.</li>
                <li><span class="emoji">📌</span> <b>Leadership & Collaboration:</b> Experience in <span class="highlight">cross-functional teamwork, mentorship, and data democratization</span>.</li>
            </ul>
        </div>

""",

    # "📌 What is Ahmed’s educational background?": "Ahmed holds a BSc in Petroleum Engineering from Suez University (2009-2014), graduating with a Very Good with Honor Degree.",
    # "📌 What programming languages and tools does Ahmed use?": "Ahmed works with Python, SQL, Airflow, Spark, Hive, Tableau, PowerBI, Streamlit, Plotly, and Shell scripting.",
    # # "📌 How can I contact Ahmed Omar?": "You can reach Ahmed via email (aoeo92@gmail.com).",
    # "📌 What are Ahmed's contributions to analytics?": "Ahmed has built real-time dashboards, forecasting models using FB Prophet, and self-service analytics tools to support decision-making.",
    # "📌 What are Ahmed’s past roles at Uber?": "Ahmed has worked as a Senior Data Scientist (2024-Present), Data Scientist II (2022-2024), Senior Data Analyst (2021-2022), Data Analyst (2019-2021), and Associate Data Analyst (2018-2019).",
    # "📌 Can you describe your role as a Senior Data Scientist at Uber?": "As a Senior Data Scientist at Uber, I focus on Competition Analytics within Global Strategy and Planning. I develop a Global Merchant-Focused Expansion Strategy, allowing teams to identify high-value merchants, geographies, cuisines, and segments for growth.",
    # "📌 What’s an example of a high-impact project you worked on?": "One of my biggest achievements was automating the restaurant sales process at Uber, reducing costs by $6M per year and improving time to sale. I partnered with Sales & Product teams to implement this successfully.",
    # "📌 How do you handle stakeholder communication?": "Communication is critical in my role. I tailor my message based on the audience—using dashboards, reports, and direct presentations for executives, and technical documentation and automation for engineering teams.",
    # "📌 How do you approach problem-solving in a data-driven environment?": "I follow a structured approach: define the problem, analyze historical data, generate hypotheses, run experiments, validate insights, and automate solutions. This ensures efficiency and measurable impact.",
    # "📌 What is your experience with A/B testing?": "I have designed multiple A/B testing experiments to optimize customer retention and engagement. By running controlled experiments, I ensured that Uber's policies and promotions were backed by statistical evidence.",
    # "📌 What programming languages and tools do you use daily?": "My primary tools include Python, SQL, Airflow, Spark, Hive, Tableau, PowerBI, Streamlit, Plotly, and Shell scripting. I use machine learning, probability, and geo-spatial analysis in my day-to-day work.",
    # "📌 What is your leadership experience?": "I have mentored junior analysts and data scientists, guiding them on best practices in analytics and strategy development. I also lead discussions on competitive analytics and business intelligence within Uber.",
    # "📌 Why did you transition from Petroleum Engineering to Data Science?": "My passion for problem-solving and data-driven decision-making led me to pivot from petroleum engineering to analytics and data science. Over the years, I built a strong foundation in data analysis, machine learning, and business intelligence.",
    # "📌 How can I contact Ahmed Omar?": "You can reach Ahmed via email (aoeo92@gmail.com)."

}


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_faqs', methods=['GET'])
def get_faqs():
    # Send only the questions to the frontend
    return jsonify({'faqs': list(faq_responses.keys())})

@app.route('/get_response', methods=['POST'])
def get_response():
    data = request.get_json()
    user_message = data.get('message', '')

    # Get answer from dictionary or provide default response
    response_text = faq_responses.get(user_message, "I'm not sure about that. Try an FAQ!")
    
    return jsonify({'response': response_text})

if __name__ == '__main__':
    app.run(debug=True)
