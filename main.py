import streamlit as st
import PyPDF2
import io
import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()
GROQ_API_KEY = "put tour api key from groq website"

# Set up Groq client
client = Groq(api_key=GROQ_API_KEY)

# Streamlit UI
st.set_page_config(page_title="AI Resume Critique", page_icon="📄", layout="centered")
st.title("📄 AI Resume Critique")
st.markdown("Upload your resume to get feedback from a fast, open-source AI model powered by **Groq**!")

uploaded_file = st.file_uploader("Upload your resume (PDF or TXT)", type=["pdf", "txt"])
job_role = st.text_input("Enter the job you want (optional)")
analyze = st.button("Analyze Resume")

# Resume text extraction
def extract_file(uploaded_file):
    if uploaded_file.type == "application/pdf":
        return extract_filepdf(io.BytesIO(uploaded_file.read()))
    return uploaded_file.read().decode("utf-8")

def extract_filepdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + '\n'
    return text

# Resume analysis using Groq + Mixtral
def analyze_resume_with_groq(resume_text, job_role):
    prompt = f"""
Please analyze this resume and provide constructive feedback.
Focus on the following aspects:
1. Content clarity and impact
2. Skills presentation
3. Experience descriptions
4. Specific improvements for {'general job applications' if not job_role else job_role}

Resume content:
{resume_text}

Provide your feedback in bullet points and make it clear and actionable.
"""
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {"role": "system", "content": "You are an expert career advisor and resume reviewer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=1000,
    )
    return response.choices[0].message.content.strip()

# Trigger analysis
if analyze and uploaded_file:
    try:
        file_content = extract_file(uploaded_file)

        if not file_content.strip():
            st.error("⚠️ File does not have any content.")
            st.stop()

        with st.spinner("Analyzing resume using Groq + Mixtral..."):
            analysis_result = analyze_resume_with_groq(file_content, job_role)

        st.markdown("## 🔍 Analysis Results")
        st.markdown(analysis_result)

    except Exception as e:
        st.error(f"❌ An error occurred: {e}")
