# 🚀 AI-Powered Smart Resume Optimizer

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Framework-red)
![AI](https://img.shields.io/badge/AI-Google%20Gemini-orange)
![Status](https://img.shields.io/badge/Status-Live-success)

**Smart Resume Optimizer** is an AI-driven web application designed to help job seekers optimize their resumes for Applicant Tracking Systems (ATS). By leveraging **Google's Gemini 2.5 Flash** model, it analyzes resumes against job descriptions to provide a match score, identify missing keywords, and offer actionable improvement suggestions.

🔗 **[Click Here to Try the Live Demo](https://ai-resume-analyzer-iegzghghymg6l4ofhvpliy.streamlit.app/)**

---

## ✨ Key Features

* **📄 PDF Resume Parsing:** Extracts text from PDF resumes using `PyPDF2`.
* **🤖 AI Analysis:** Uses Google Gemini Generative AI to compare the resume with the job description.
* **📊 Smart Scoring:** Provides a percentage-based match score (ATS Logic).
* **🔍 Keyword Detection:** Identifies critical skills and keywords missing from the resume.
* **💾 Local History:** Saves past analyses (Company Name, Date, Score) to a JSON file for easy tracking.
* **⚡ Fast & Responsive:** Built with Streamlit for a seamless user experience.

---

## 🛠️ Tech Stack

* **Language:** Python
* **Frontend:** Streamlit
* **AI Model:** Google Gemini 2.5 Flash
* **Libraries:** `google-generativeai`, `python-dotenv`, `PyPDF2`

---

## 🚀 How to Run Locally

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/HuntNes/ai-resume-analyzer.git](https://github.com/HuntNes/ai-resume-analyzer.git)
    cd ai-resume-analyzer
    ```

2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up Environment Variables:**
    * Create a `.env` file.
    * Add your Google API Key: `GOOGLE_API_KEY=your_api_key`

4.  **Run the App:**
    ```bash
    streamlit run app.py
    ```

---

### 👨‍💻 Author

**Muhammed Enes Çam**
* [GitHub Profile](https://github.com/HuntNes)