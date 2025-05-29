# GenMediPlan - AI-Powered Healthcare Analysis System

GenMediPlan is an intelligent healthcare analysis system that uses AI to analyze patient reports and provide treatment recommendations. The system processes PDF medical reports, extracts relevant information, and uses advanced language models to generate comprehensive treatment plans.

## Features

- PDF medical report upload and processing
- AI-powered analysis of patient data
- Structured treatment recommendations
- Risk factor identification
- Monitoring plan generation
- Modern, responsive web interface

## Tech Stack

### Backend
- FastAPI (Python web framework)
- OpenAI GPT-4 for analysis
- PyPDF2 for PDF processing
- Pydantic for data validation

### Frontend
- React
- Material-UI
- React Router
- Axios for API calls

## Project Structure

```
genmediplan/
├── app/                              # Core application logic
│   ├── main.py                       # FastAPI entrypoint
│   ├── routes.py                     # API endpoints
│   ├── controller.py                 # Logic for handling uploaded PDFs
│   └── config.py                     # Environment/config variables
│
├── data/
│   ├── raw/                          # Uploaded raw PDFs
│   ├── extracted/                    # Extracted structured JSON from PDF
│   └── samples/                      # Demo or synthetic sample PDFs
│
├── models/                           # AI and ML models
│   ├── embedder.py                   # Embeds structured patient data
│   ├── predictor.py                  # Generative AI for treatment response
│   └── plan_generator.py            # Converts prediction to a full plan
│
├── pdf_parser/                       # PDF processing and data extraction
│   ├── extract_text.py               # Extracts plain text from PDF
│   ├── extract_tables.py             # Extracts tables, charts
│   └── parser.py                     # Combines and formats as structured dict
│
├── prompts/                          # Prompt templates for the LLM
│   └── treatment_prompt.txt
│
├── utils/                           # Utility functions
│   ├── logger.py                     # Custom logging
│   ├── preprocessor.py               # Cleans and standardizes patient data
│   └── validator.py                  # Checks for missing/invalid fields
│
├── frontend/                        # React frontend application
│   ├── src/
│   │   ├── components/              # React components
│   │   ├── App.js                   # Main application component
│   │   └── index.js                 # Application entry point
│   └── package.json                 # Frontend dependencies
│
├── tests/                           # Test files
│   ├── test_parser.py
│   ├── test_predictor.py
│   └── test_end_to_end.py
│
├── requirements.txt                 # Python dependencies
└── README.md                        # Project documentation
```

## Setup and Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/genmediplan.git
cd genmediplan
```

2. Set up the Python environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Set up the frontend:
```bash
cd frontend
npm install
```

4. Create a `.env` file in the root directory with your configuration:
```
OPENAI_API_KEY=your_api_key_here
SECRET_KEY=your_secret_key_here
```

5. Start the backend server:
```bash
uvicorn app.main:app --reload
```

6. Start the frontend development server:
```bash
cd frontend
npm start
```

## Usage

1. Open your browser and navigate to `http://localhost:3000`
2. Upload a medical report PDF using the upload interface
3. View the AI-generated analysis and treatment recommendations
4. Download or share the generated treatment plan

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Security

- All uploaded files are processed securely
- No patient data is stored permanently
- API keys and sensitive information are managed through environment variables

## Support

For support, please open an issue in the GitHub repository or contact the development team. 