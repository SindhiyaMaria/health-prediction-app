# MIRA - Medical Intelligence Health Predictor

## Overview
This is a complete submission for the **Junior AI/ML Developer** technical assessment at Gokul Infocare.

**Tech Stack:**
- **Frontend**: Streamlit (Python)
- **Backend**: Python + PostgreSQL
- **AI/ML**: Ollama (Llama 3) for local health risk prediction
- **ORM/Connection**: psycopg2

## Features Implemented
- Full CRUD operations (Create, Read, Update, Delete)
- Robust data validation
- Persistent storage with PostgreSQL
- AI-powered health risk prediction with structured output
- Clean, responsive UI

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd mira-health-predictor
   ```

2. **Install dependencies**
   ```bash
   pip install streamlit pandas psycopg2-binary python-dotenv ollama
   ```

3. **Setup PostgreSQL**
   - Create database `health_db`
   - Update `.env` file with your credentials

4. **Setup Ollama**
   ```bash
   # Install Ollama from https://ollama.com
   ollama pull llama3
   ollama serve
   ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

## AI Integration
The application uses **Ollama + Llama 3** (running locally) as the AI service to generate structured health risk predictions based on blood parameters. This satisfies the requirement for calling an external AI/ML service for disease risk prediction.

## Notes
- All sensitive credentials are loaded from `.env` (not committed)
- `.env` is gitignored
- Demo video will demonstrate all CRUD flows and AI prediction

---
**Submitted for Junior AI/ML Developer (WFH) position**

