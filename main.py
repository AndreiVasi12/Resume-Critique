import streamlit as st
import PyPDF2
import io
import os
from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()

st.set_page_config(page_title="AI Resume Critique",page_icon="",layout="centered")
st.title("AI Resume Critique")
st.markdown("Upload your resume to get feedback from the AI made for your needs ! ")

OPEN_AI_KEY = os.getenv("OPEN_AI_KEY")

uploaded_file=st.file_uploader("Upload your resume (PDF or TXT)",type =["pdf","txt"])
job_role = st.text_input("Enter the job you want(optional)")
analyze= st.button("Analyze Resume")

def extract_file(uploaded_file):
    if uploaded_file.type == "application/pdf" :
        return extract_filepdf(io.BytesIO(uploaded_file.read()))
    return uploaded_file.read().decode("utf-8")

def extract_filepdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()+'\n'
    return  text

if analyze and uploaded_file:
    try :
        file_content = extract_file(uploaded_file)

        if not file_content.strip():
            st.error("File does not have any content")
            st.stop()

        prompt = f"""Please analyze this resume and provide constructive feedback. 
        Focus on the following aspects:
        1. Content clarity and impact
        2. Skills presentation
        3. Experience descriptions
        4. Specific improvements for {job_role if job_role else 'general job applications'}

        Resume content:
        {file_content}

        Please provide your analysis in a clear, structured format with specific recommendations."""
        client = OpenAI(api_key=OPEN_AI_KEY)
        response = client.chat.completions.create(model="gpt-4o-mini",
                                                  messages=[
                                                      {"role":"system","content":"You are an expert cv reviewer with experience"},
                                                      {"role":"user", "content": prompt}
                                                  ],temperature = 0.7,max_tokens=1000)
        st.markdown("##Analysis Results")
        st.markdown(response.choices[0].message.content)
    except Exception as e:
       st.error(f"An error appeard : {e}")