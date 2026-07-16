import streamlit as st
from google import genai

client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"]
)

# ----------------------------
# AI Resume Review
# ----------------------------

def ai_resume_review(resume_text):

    prompt = f"""
You are an expert ATS Resume Reviewer.

Analyze the following resume.

Give your answer in this format.

## Overall ATS Score (out of 100)

## Overall Review

## Resume Strengths

## Weaknesses

## Missing Sections

## Technical Skills Evaluation

## Suggested Improvements

## Best Suitable Job Roles

## HR Interview Questions (5)

## Technical Interview Questions (5)

## 30-Day Improvement Roadmap

Resume:

{resume_text}
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt
    )

    return response.text