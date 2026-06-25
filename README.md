# 🩺 MIRA - Medical Intelligence Health Predictor

A Streamlit-based healthcare application developed as part of the **Junior AI/ML Developer Technical Assessment**. The application allows users to manage patient records, store them in PostgreSQL, and generate AI-powered health risk assessments using **Ollama (Llama 3)**.

---

## Features

- ✅ Create, Read, Update, and Delete (CRUD) patient records
- ✅ PostgreSQL database integration
- ✅ AI-powered health risk analysis using Ollama (Llama 3)
- ✅ Input validation (email, date of birth, blood test values)
- ✅ Responsive Streamlit user interface
- ✅ Persistent data storage
- ✅ Error handling and user-friendly notifications

---

## Tech Stack

| Component | Technology |
|-----------|------------|
| Frontend | Streamlit |
| Backend | Python |
| Database | PostgreSQL |
| Database Driver | psycopg2 |
| AI Model | Ollama (Llama 3) |
| Environment Variables | python-dotenv |

---

## Project Structure

```text
health-prediction-app/
│── app.py
│── requirements.txt
│── .env.example
│── README.md
│── .gitignore
```

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/health-prediction-app.git
cd health-prediction-app
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it:

Windows:

```bash
venv\Scripts\activate
```

Linux/macOS:

```bash
source venv/bin/activate
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

If you don't have a `requirements.txt`, you can install manually:

```bash
pip install streamlit pandas psycopg2-binary python-dotenv ollama
```

---

### 4. Configure PostgreSQL

Create a database named:

```text
health_db
```

Create a `.env` file:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=health_db
DB_USER=postgres
DB_PASSWORD=your_password
```

---

### 5. Install and run Ollama

Download Ollama:

https://ollama.com/download

Pull the model:

```bash
ollama pull llama3
```

Start the Ollama service (if it's not already running):

```bash
ollama serve
```

---

### 6. Run the application

```bash
streamlit run app.py
```

The application will be available at:

```
http://localhost:8501
```

---

## AI Integration

The application uses **Ollama with the Llama 3 model** to generate structured health risk assessments based on patient blood parameters.

The generated response includes:

- Health risk level
- Possible health concerns
- Brief AI-generated explanation

---

## Screenshots

Add screenshots here after uploading them to your repository.

Example:

```
images/home.png
images/patient-list.png
images/ai-prediction.png
```

---

## Future Improvements

- Authentication and user login
- Search and filter patients
- Export patient records to CSV/PDF
- Dashboard with health statistics
- Integration with external healthcare APIs

---

## Author

**Sindhiya Maria**

Submitted as part of the **Junior AI/ML Developer Technical Assessment**.
