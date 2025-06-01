# CV Assistant Portal (CVAP)

A Flask-based web application that serves as an interactive CV/Resume assistant. This application provides dynamic responses to frequently asked questions about professional experience, skills, and qualifications.

## Overview

CVAP is designed to make CV/Resume information more accessible and interactive. Instead of reading through a static document, users can ask questions and get specific, relevant information about professional experience, skills, and achievements.

## Features

- 🤖 Interactive FAQ System
- 💬 Real-time Response Generation
- 🎨 Clean and Modern Web Interface
- 🔄 RESTful API Endpoints
- 📱 Mobile-Responsive Design

## Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQLite
- **API**: RESTful Architecture

## Getting Started

### Prerequisites

- Python 3.x
- pip (Python package installer)

### Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/AhmedOmarO/cvap.git
   cd cvap
   ```

2. **Set Up Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

1. **Start the Flask Server**
   ```bash
   python app.py
   ```

2. **Access the Application**
   - Open your web browser
   - Navigate to `http://localhost:5000`
   - Start interacting with the CV Assistant!

## Project Structure

```
cvap/
├── app.py              # Main Flask application
├── requirements.txt    # Project dependencies
├── templates/         # HTML templates
│   └── index.html    # Main page template
├── static/           # Static files (CSS, JS)
└── instance/         # Instance-specific files
    └── faq_responses.db  # SQLite database
```

## API Endpoints

- `GET /`: Main application interface
- `GET /get_faqs`: Retrieve list of available FAQs
- `POST /get_response`: Get response for a specific question

## Development

The application runs in debug mode by default, which provides:
- Detailed error messages
- Auto-reload on code changes
- Interactive debugger

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Future Enhancements

- [ ] Add authentication system
- [ ] Implement response caching
- [ ] Add analytics dashboard
- [ ] Support multiple CV profiles
- [ ] Add multilingual support

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

Ahmed Omar - [@AhmedOmarO](https://github.com/AhmedOmarO)

Project Link: [https://github.com/AhmedOmarO/cvap](https://github.com/AhmedOmarO/cvap) 