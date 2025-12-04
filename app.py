import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import json
from datetime import datetime
import re


load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

MODEL_NAME = "gemini-2.5-flash"
HISTORY_FILE = "history.json"

st.set_page_config(
    page_title="Smart Resume Analyzer",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .main { background-color: #f5f5f5; }
    [data-testid="stSidebar"] { min-width: 400px; max-width: 800px; }
    .stButton>button {
        width: 100%;
        background-color: #FF4B4B;
        color: white;
        font-weight: bold;
        border-radius: 10px;
        height: 50px;
    }
    .stTextArea textarea {
        background-color: #f0f2f6 !important;
        color: #000000 !important;
    }
    .success-box {
        padding: 20px;
        border-radius: 10px;
        background-color: #e6fffa;
        border-left: 5px solid #00cc99;
        margin-bottom: 20px;
        color: #004d3b;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text += page.extract_text()
    return text

def get_gemini_response(input_prompt):
    model = genai.GenerativeModel(MODEL_NAME)
    response = model.generate_content(input_prompt)
    return response.text

def extract_score(text):
    match = re.search(r'(\d{1,3})%', text)
    if match:
        return match.group(0)
    return "?%"


def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def save_to_history(company, analysis):
    history = load_history()
    score = extract_score(analysis)
    new_entry = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "company": company if company else "General Application",
        "score": score,
        "analysis": analysis
    }
    history.insert(0, new_entry)
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=4)

with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712035.png", width=120)
    st.title("📂 Control Panel")
    
    tab1, tab2 = st.tabs(["📝 New Analysis", "📜 History"])
    
    with tab1:
        company_name = st.text_input("Target Company Name:", placeholder="e.g. Google, Amazon...")
        st.subheader("Job Description")
        job_description = st.text_area("Paste JD:", height=200, placeholder="Required Skills...")
        st.subheader("Your Resume")
        uploaded_file = st.file_uploader("Upload PDF", type="pdf")
        st.markdown("---")
        submit = st.button("ANALYZE RESUME")
    
    with tab2:
        st.subheader("Past Analyses")
        history_data = load_history()
        if not history_data:
            st.info("No history found.")
        else:
            for item in history_data:
                header_text = f"{item['date']} | {item['company']} | {item.get('score', '?')}"
                with st.expander(header_text):
                    st.write(item['analysis'])

st.header("AI-Powered Resume Optimizer")
st.subheader("Beat the ATS and land your dream job.")
st.divider()


if submit:
    if uploaded_file is not None and job_description:
        with st.spinner("🔍 AI is analyzing..."):
            
            text = input_pdf_text(uploaded_file)
            
            input_prompt = f"""
            You are an expert HR & ATS system.
            
            JOB DESCRIPTION:
            {job_description}

            RESUME:
            {text}

            Analyze the resume. IMPORTANT: Keep your response VERY CONCISE, SHORT, and TO THE POINT.
            Do not use long paragraphs. Use short bullet points.

            Structure your response exactly like this:

            ### Match Score: [Score]%
            (One short sentence summary)

            ### Missing Keywords
            * (List only the most critical missing skills, comma-separated or short list)

            ### Top Strengths
            * (List max 3 key strengths in short bullet points)

            ### Recommendations
            * (List max 3 specific, actionable changes. Keep them very short.)
            """

            try:
                response = get_gemini_response(input_prompt)
                save_to_history(company_name, response)

                st.markdown('<div class="success-box">✅ Analysis Saved & Completed!</div>', unsafe_allow_html=True)
                st.markdown(response)
                
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.info("👈 Please enter Company Name, JD and upload Resume.")