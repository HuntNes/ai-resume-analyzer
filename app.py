import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import re
from datetime import datetime

# 1. Ayarları Yükle
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Model Seçimi
MODEL_NAME = "gemini-2.5-flash"

# --- SAYFA AYARLARI ---
st.set_page_config(
    page_title="Smart Resume Analyzer",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS STYLES ---
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

# --- YARDIMCI FONKSİYONLAR ---

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

# --- GÜVENLİ GEÇMİŞ YÖNETİMİ (SESSION STATE) ---
# Dosya yerine RAM kullanıyoruz. Herkesin geçmişi kendine özel oluyor.

if 'history' not in st.session_state:
    st.session_state['history'] = []

def save_to_session_history(company, analysis):
    score = extract_score(analysis)
    new_entry = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "company": company if company else "General Application",
        "score": score,
        "analysis": analysis
    }
    # Listeye ekle (En başa)
    st.session_state['history'].insert(0, new_entry)

# --- SIDEBAR ---
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
        submit = st.button("🚀 ANALYZE RESUME")
    
    with tab2:
        st.subheader("Session History")
        st.info("⚠️ This history is private to you and will be cleared when you refresh the page.")
        
        # Session State'ten oku
        if not st.session_state['history']:
            st.write("No analysis yet.")
        else:
            for item in st.session_state['history']:
                header_text = f"{item['date']} | {item['company']} | {item.get('score', '?')}"
                with st.expander(header_text):
                    st.write(item['analysis'])

# --- ANA EKRAN ---
st.header("AI-Powered Resume Optimizer")
st.subheader("Beat the ATS and land your dream job.")
st.divider()

# --- AI MANTIĞI ---

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

            ### 🎯 Match Score: [Score]%
            (One short sentence summary)

            ### ✅ Missing Keywords
            * (List only the most critical missing skills, comma-separated or short list)

            ### 🌟 Top Strengths
            * (List max 3 key strengths in short bullet points)

            ### ⚠️ Recommendations
            * (List max 3 specific, actionable changes. Keep them very short.)
            """
            
            try:
                response = get_gemini_response(input_prompt)
                
                # --- Session State'e Kaydet ---
                save_to_session_history(company_name, response)

                st.markdown('<div class="success-box">✅ Analysis Completed!</div>', unsafe_allow_html=True)
                st.markdown(response)
                
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.info("👈 Please enter Company Name, JD and upload Resume.")