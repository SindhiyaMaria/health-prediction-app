# 🩺 MIRA - Medical Intelligence Health Predictor

A Streamlit-based healthcare application developed as part of the Junior AI/ML Developer Technical Assessment. The application allows users to manage patient records, store them in PostgreSQL, and generate AI-powered health risk assessments using **Groq** (Llama 3.3).

## Features
✅ Create, Read, Update, and Delete (CRUD) patient records  
✅ PostgreSQL database integration  
✅ AI-powered health risk analysis using **Groq API** (Llama 3.3-70b-versatile)  
✅ Input validation (email, date of birth, blood test values)  
✅ Responsive Streamlit user interface  
✅ Persistent data storage  
✅ Error handling and user-friendly notifications  

## Tech Stack
| Component       | Technology                  |
|-----------------|-----------------------------|
| Frontend        | Streamlit                   |
| Backend         | Python                      |
| Database        | PostgreSQL                  |
| Database Driver | psycopg2                    |
| AI Model        | Groq (Llama 3.3-70b-versatile) |
| Environment     | python-dotenv               |

## Project Structure
health-prediction-app/
├── app.py
├── requirements.txt
├── .env.example
├── README.md
├── .gitignore
text## Installation

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/health-prediction-app.git
cd health-prediction-app
2. Create & activate virtual environment
Bashpython -m venv venv
# Windows
venv\Scripts\activate
# Linux/macOS
source venv/bin/activate
3. Install dependencies
Bashpip install -r requirements.txt
Or manually:
Bashpip install streamlit pandas psycopg2-binary python-dotenv groq
4. Setup PostgreSQL & Environment
Create database health_db, then create .env file:
envDB_HOST=localhost
DB_PORT=5432
DB_NAME=health_db
DB_USER=postgres
DB_PASSWORD=your_password
GROQ_API_KEY=your_groq_api_key_here
Get Groq API key: https://console.groq.com/keys
5. Run the app
Bashstreamlit run app.py
App will be live at http://localhost:8501
AI Integration
The app uses Groq with the llama-3.3-70b-versatile model to generate structured health risk predictions based on glucose, haemoglobin, and cholesterol levels.
Future Improvements

User authentication
Search & filter functionality
Export to CSV/PDF
Analytics dashboard
External healthcare API integration


Author
Sindhiya Maria

