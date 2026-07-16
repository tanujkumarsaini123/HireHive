import streamlit as st
from google import genai

client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"]
)

def ask_hirehive(question):

    prompt = f"""
You are HireHive AI.

You are an expert Career Mentor, Placement Trainer and Software Engineer.

Answer only career, placement, interview, resume, ATS score, DSA,
programming, Python, Java, C++, AI, Machine Learning, Data Science,
Cloud Computing, Cyber Security and Software Engineering questions.

If someone asks anything unrelated, politely reply:
"I only answer career and placement related questions."

Question:
{question}
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt,
    )

    return response.text