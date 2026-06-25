import streamlit as st
import pandas as pd
import psycopg2
from datetime import date
import ollama
import re
from dotenv import load_dotenv
import os

load_dotenv()

# ====================== DATABASE SETUP ======================
def init_db():
    conn = get_db_connection()
    if conn:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS patients (
                id SERIAL PRIMARY KEY,
                full_name TEXT NOT NULL,
                dob DATE NOT NULL,
                email TEXT NOT NULL,
                glucose FLOAT,
                haemoglobin FLOAT,
                cholesterol FLOAT,
                remarks TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        cur.close()
        conn.close()

def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST", "localhost"),
            database=os.getenv("DB_NAME", "health_db"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD"),
            port=os.getenv("DB_PORT", "5432")
        )
        return conn
    except Exception as e:
        st.error(f"Database Connection Failed: {str(e)}")
        return None

# ====================== AI REMARKS ======================
def generate_remarks(data):
    age = date.today().year - data['dob'].year
    prompt = f"""
You are a helpful medical AI assistant. Analyze the following blood test results and predict possible health risks.

Patient: {data['full_name']}
Age: {age} years
Glucose: {data['glucose']} mg/dL
Haemoglobin: {data['haemoglobin']} g/dL
Cholesterol: {data['cholesterol']} mg/dL

Provide a structured prediction in this exact format:

Risk Level: [Low/Medium/High]
Possible Condition: [Short name of possible condition or "No major risks detected"]
Short Explanation: [2-3 sentences of analysis. Do not give medical advice or recommend actions.]

Be concise and professional.
"""
    try:
        response = ollama.chat(model='llama3', messages=[{'role': 'user', 'content': prompt}])
        return response['message']['content'].strip()
    except Exception as e:
        st.warning("AI service unavailable.")
        return "AI analysis temporarily unavailable. Risk assessment could not be generated."

# ====================== VALIDATION ======================
def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_patient(data):
    errors = []
    if not data['full_name'].strip():
        errors.append("Full Name is required")
    if not is_valid_email(data['email']):
        errors.append("Invalid email format")
    if data['dob'] > date.today():
        errors.append("Date of Birth cannot be in the future")
    if not (0 <= data['glucose'] <= 500):
        errors.append("Glucose should be between 0-500 mg/dL")
    if not (5 <= data['haemoglobin'] <= 20):
        errors.append("Haemoglobin should be between 5-20 g/dL")
    if not (100 <= data['cholesterol'] <= 400):
        errors.append("Cholesterol should be between 100-400 mg/dL")
    return errors

# ====================== CRUD ======================
def create_patient(data):
    conn = get_db_connection()
    if not conn: return False
    try:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO patients (full_name, dob, email, glucose, haemoglobin, cholesterol, remarks)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (data['full_name'], data['dob'], data['email'],
              data['glucose'], data['haemoglobin'], data['cholesterol'], data['remarks']))
        conn.commit()
        return True
    except Exception as e:
        st.error(f"Error creating patient: {str(e)}")
        return False
    finally:
        if cur: cur.close()
        if conn: conn.close()

def get_all_patients():
    conn = get_db_connection()
    if not conn: return pd.DataFrame()
    try:
        df = pd.read_sql("""
            SELECT id, full_name, dob, email, glucose, haemoglobin, cholesterol, remarks, created_at
            FROM patients ORDER BY created_at DESC
        """, conn)
        return df
    finally:
        conn.close()

def update_patient(pid, data):
    conn = get_db_connection()
    if not conn: return False
    try:
        cur = conn.cursor()
        cur.execute("""
            UPDATE patients SET full_name=%s, dob=%s, email=%s, glucose=%s,
            haemoglobin=%s, cholesterol=%s, remarks=%s WHERE id=%s
        """, (data['full_name'], data['dob'], data['email'],
              data['glucose'], data['haemoglobin'], data['cholesterol'], data['remarks'], pid))
        conn.commit()
        return True
    except Exception as e:
        st.error(f"Error updating patient: {str(e)}")
        return False
    finally:
        if cur: cur.close()
        if conn: conn.close()

def delete_patient(pid):
    conn = get_db_connection()
    if not conn: return False
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM patients WHERE id=%s", (pid,))
        conn.commit()
        return True
    except Exception as e:
        st.error(f"Error deleting patient: {str(e)}")
        return False
    finally:
        if cur: cur.close()
        if conn: conn.close()

# ====================== STREAMLIT APP ======================
st.set_page_config(page_title="MIRA Health Predictor", layout="wide")
st.markdown("""
    <style>
        .main > div {padding-top: 1rem !important;}
        h1 {margin-bottom: 0.3rem !important;}
        .block-container {padding-top: 1rem !important;}
        .stSubheader {margin-top: 0.5rem !important;}
    </style>
""", unsafe_allow_html=True)

col1, col2 = st.columns([0.8, 10])
with col1:
    st.markdown("🩺")
with col2:
    st.title("MIRA - Medical Intelligence Health Predictor")

init_db()

menu = st.sidebar.selectbox("Menu", ["Add New Patient", "View All Patients"])
st.sidebar.caption("Junior AI/ML Developer Task - Gokul Infocare")

# ====================== ADD NEW PATIENT ======================
if menu == "Add New Patient":
    st.subheader("Enter Patient Details")
   
    with st.form("add_patient"):
        full_name = st.text_input("Full Name*")
        dob = st.date_input(
            "Date of Birth*",
            value=date(2000, 1, 1),
            min_value=date(1950, 1, 1),
            max_value=date.today()
        )
        email = st.text_input("Email Address*")
       
        col1, col2, col3 = st.columns(3)
        with col1: 
            glucose = st.number_input("Glucose (mg/dL)", min_value=0.0, value=90.0, step=0.1)
        with col2: 
            haemoglobin = st.number_input("Haemoglobin (g/dL)", min_value=0.0, value=13.5, step=0.1)
        with col3: 
            cholesterol = st.number_input("Cholesterol (mg/dL)", min_value=0.0, value=180.0, step=0.1)
        
        submitted = st.form_submit_button("Submit & Get AI Prediction")
       
        if submitted:
            data = {
                "full_name": full_name.strip(),
                "dob": dob,
                "email": email.strip(),
                "glucose": glucose,
                "haemoglobin": haemoglobin,
                "cholesterol": cholesterol
            }
           
            errors = validate_patient(data)
            if errors:
                for err in errors:
                    st.error(err)
            else:
                with st.spinner("Generating AI Health Risk Prediction..."):
                    data["remarks"] = generate_remarks(data)
               
                if create_patient(data):
                    st.success(" Patient record saved successfully with AI prediction!")
                    st.write("**AI Prediction:**")
                    st.write(data["remarks"])

# ====================== VIEW ALL PATIENTS ======================
else:
    st.subheader("All Patient Records")
   
    # Initialize session state
    if 'message' not in st.session_state:
        st.session_state.message = None
    if 'message_type' not in st.session_state:
        st.session_state.message_type = None
    if 'original_df' not in st.session_state:
        st.session_state.original_df = None

    # Show persistent message
    if st.session_state.message:
        if st.session_state.message_type == "success":
            st.success(st.session_state.message)
        elif st.session_state.message_type == "error":
            st.error(st.session_state.message)
        st.session_state.message = None
        st.session_state.message_type = None

    df = get_all_patients()
   
    if not df.empty:
        # Store original dataframe for comparison
        if st.session_state.original_df is None or len(st.session_state.original_df) != len(df):
            st.session_state.original_df = df.copy()

        edited_df = st.data_editor(
            df,
            hide_index=False,
            width='stretch',
            # use_container_width=True,
            column_config={
                "id": st.column_config.NumberColumn(disabled=True),
                "created_at": st.column_config.DatetimeColumn(disabled=True),
                "remarks": st.column_config.TextColumn(disabled=False, width="medium"),
            },
            key="patient_editor"  # Important for consistency
        )
       
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("💾 Save Changes", type="primary"):
                try:
                    success_count = 0
                    updated_count = 0
                    
                    # Compare edited vs original
                    for idx, row in edited_df.iterrows():
                        original_row = st.session_state.original_df.loc[
                            st.session_state.original_df['id'] == row['id']
                        ].iloc[0]
                        
                        # Check if row has changed
                        if not row.equals(original_row):
                            if update_patient(row['id'], row.to_dict()):
                                success_count += 1
                            updated_count += 1
                    
                    if success_count > 0:
                        st.session_state.message = f" {success_count} record(s) updated successfully!"
                        st.session_state.message_type = "success"
                    elif updated_count == 0:
                        st.session_state.message = "ℹ️ No changes detected."
                        st.session_state.message_type = "success"
                    else:
                        st.session_state.message = " Failed to update some records."
                        st.session_state.message_type = "error"
                    
                    # Refresh original data
                    st.session_state.original_df = None
                    st.rerun()
                    
                except Exception as e:
                    st.session_state.message = f" Error saving changes: {str(e)}"
                    st.session_state.message_type = "error"
                    st.rerun()
        
        with col2:
            delete_id = st.number_input("Delete by ID", min_value=1, step=1, key="delete_input")
            if st.button("🗑️ Delete Record", type="secondary"):
                if delete_patient(delete_id):
                    st.session_state.message = f" Record {delete_id} deleted successfully!"
                    st.session_state.message_type = "success"
                    st.session_state.original_df = None  # Reset for refresh
                    st.rerun()
                else:
                    st.session_state.message = f" Failed to delete record {delete_id}"
                    st.session_state.message_type = "error"
                    st.rerun()
    else:
        st.info("No patient records found yet.")
















