from utils.career_advice import career_advice
from utils.recommendation import recommend_companies
from utils.pdf_generator import generate_report
from utils.chatbot import ask_hirehive
from utils.resume_ai import ai_resume_review
from utils.resume_analyzer import (
    extract_resume_text,
    detect_skills,
    calculate_ats_score,
    missing_skills
)

import streamlit as st
import pandas as pd
import joblib

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="HireHive",
    page_icon="💼",
    layout="wide"
)

# =====================================================
# LOAD MODEL
# =====================================================

model = joblib.load("models/placement_model.pkl")

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.title("💼 HireHive")

page = st.sidebar.radio(
    "Navigation",
    [
        "Home",
        "Placement Prediction",
        "📄 Resume Analyzer",
        "🤖 HireHive AI",
        "Dashboard",
        "About"
    ]
)

# =====================================================
# HOME
# =====================================================

if page == "Home":

    st.title("💼 HireHive")

    st.subheader("AI Placement Assistant")

    st.write("""
Welcome to HireHive.

This application predicts a student's placement probability using Machine Learning.

Features:
- Placement Prediction
- Resume Analyzer
- ATS Score
- AI Career Chatbot
- Company Recommendation
- Career Suggestions
""")

    st.markdown("---")

    c1, c2, c3 = st.columns(3)

    c1.metric("Model", "Random Forest")
    c2.metric("Dataset", "45,000 Students")
    c3.metric("Accuracy", "100%")

# =====================================================
# PLACEMENT PREDICTION
# =====================================================

elif page == "Placement Prediction":

    st.title("🎯 Placement Prediction")

    age = st.slider("Age",18,24,21)

    gender = st.selectbox(
        "Gender",
        ["Male","Female"]
    )

    degree = st.selectbox(
        "Degree",
        ["B.Tech","BCA","B.Sc","MCA"]
    )

    branch = st.selectbox(
        "Branch",
        ["CSE","ECE","ME","Civil","IT"]
    )

    cgpa = st.slider(
        "CGPA",
        5.0,
        10.0,
        7.5
    )

    internships = st.number_input(
        "Internships",
        0,
        5,
        1
    )

    projects = st.number_input(
        "Projects",
        0,
        10,
        2
    )

    coding = st.slider(
        "Coding Skills",
        1,
        10,
        6
    )

    communication = st.slider(
        "Communication Skills",
        1,
        10,
        6
    )

    aptitude = st.slider(
        "Aptitude Test Score",
        0,
        100,
        60
    )

    soft = st.slider(
        "Soft Skills",
        1,
        10,
        6
    )

    certifications = st.number_input(
        "Certifications",
        0,
        5,
        1
    )

    backlogs = st.number_input(
        "Backlogs",
        0,
        5,
        0
    )

    if st.button("Predict Placement"):

        gender_map = {
            "Female":0,
            "Male":1
        }

        degree_map = {
            "B.Sc":0,
            "B.Tech":1,
            "BCA":2,
            "MCA":3
        }

        branch_map = {
            "CSE":0,
            "Civil":1,
            "ECE":2,
            "IT":3,
            "ME":4
        }

        input_df = pd.DataFrame({

            "Age":[age],
            "Gender":[gender_map[gender]],
            "Degree":[degree_map[degree]],
            "Branch":[branch_map[branch]],
            "CGPA":[cgpa],
            "Internships":[internships],
            "Projects":[projects],
            "Coding_Skills":[coding],
            "Communication_Skills":[communication],
            "Aptitude_Test_Score":[aptitude],
            "Soft_Skills_Rating":[soft],
            "Certifications":[certifications],
            "Backlogs":[backlogs]

        })

        prediction = model.predict(input_df)[0]
        probability = model.predict_proba(input_df)[0][1] * 100

        st.header("Prediction Result")

        if prediction == 1:
            st.success("🎉 Student is Likely to be Placed")
        else:
            st.error("❌ Student is Likely to be Not Placed")

        st.metric(
            "Placement Probability",
            f"{probability:.2f}%"
        )

        st.progress(probability/100)

        companies = recommend_companies(
            probability,
            cgpa,
            coding,
            internships
        )

        st.subheader("🏢 Recommended Companies")

        for company in companies:
            st.success(company)

        tips = career_advice(
            cgpa,
            coding,
            communication,
            internships,
            projects,
            backlogs
        )

        st.subheader("🎯 Career Suggestions")

        for tip in tips:
            st.write("✅", tip)

        report_data = {
            "Age":age,
            "Gender":gender,
            "Degree":degree,
            "Branch":branch,
            "Prediction":"Placed" if prediction==1 else "Not Placed",
            "Probability":probability,
            "Companies":companies,
            "Suggestions":tips
        }

        generate_report(
            "Placement_Report.pdf",
            report_data
        )

        with open("Placement_Report.pdf","rb") as pdf:

            st.download_button(
                "📄 Download Placement Report",
                pdf,
                file_name="HireHive_Report.pdf",
                mime="application/pdf"
            )# =====================================================
# RESUME ANALYZER
# =====================================================

elif page == "📄 Resume Analyzer":

    st.title("📄 AI Resume Analyzer")

    st.write(
        "Upload your resume to analyze skills, ATS score and missing skills."
    )

    uploaded_file = st.file_uploader(
        "Upload Resume (PDF Only)",
        type=["pdf"]
    )

    if uploaded_file is not None:

        text = extract_resume_text(uploaded_file)
        with st.spinner("🤖 AI is analyzing your resume..."):

            ai_review = ai_resume_review(text)
        skills = detect_skills(text)

        ats_score = calculate_ats_score(
            text,
            skills
        )

        missing = missing_skills(skills)

        # --------------------------
        # ATS SCORE
        # --------------------------

        st.subheader("📊 ATS Score")

        st.metric(
            "Overall ATS Score",
            f"{ats_score}/100"
        )

        st.progress(ats_score / 100)

        # --------------------------
        # Resume Rating
        # --------------------------

        if ats_score >= 85:
            st.success("⭐⭐⭐⭐⭐ Excellent Resume")

        elif ats_score >= 70:
            st.success("⭐⭐⭐⭐ Very Good Resume")

        elif ats_score >= 50:
            st.warning("⭐⭐⭐ Average Resume")

        else:
            st.error("⭐⭐ Needs Improvement")

        st.markdown("---")
        st.subheader("🤖 AI Resume Review")

        st.write(ai_review)
        # --------------------------
        # Skills Found
        # --------------------------

        st.subheader("💻 Skills Detected")

        if len(skills) == 0:

            st.warning("No technical skills detected.")

        else:

            col1, col2 = st.columns(2)

            half = len(skills) // 2

            with col1:

                for skill in skills[:half]:
                    st.success(skill)

            with col2:

                for skill in skills[half:]:
                    st.success(skill)

        st.markdown("---")

        # --------------------------
        # Missing Skills
        # --------------------------

        st.subheader("❌ Recommended Skills")

        for skill in missing[:15]:

            st.write("🔹", skill)

        st.markdown("---")

        # --------------------------
        # Resume Statistics
        # --------------------------

        words = len(text.split())

        characters = len(text)

        c1, c2 = st.columns(2)

        c1.metric(
            "Words",
            words
        )

        c2.metric(
            "Characters",
            characters
        )

        st.markdown("---")

        # --------------------------
        # Resume Preview
        # --------------------------

        st.subheader("📄 Resume Content")

        st.text_area(
            "",
            text,
            height=350
        )

        st.markdown("---")

        # --------------------------
        # Resume Suggestions
        # --------------------------

        st.subheader("🎯 Resume Improvement Tips")

        if ats_score >= 85:

            st.success(
                "Excellent Resume. Keep updating projects and achievements."
            )

        else:

            tips = []

            if "internship" not in text.lower():
                tips.append("✔ Add Internship Experience")

            if "project" not in text.lower():
                tips.append("✔ Add More Projects")

            if "github" not in text.lower():
                tips.append("✔ Add GitHub Profile")

            if "linkedin" not in text.lower():
                tips.append("✔ Add LinkedIn Profile")

            if len(skills) < 8:
                tips.append("✔ Learn More Technical Skills")

            if ats_score < 60:
                tips.append("✔ Improve Resume Formatting")

            if len(tips) == 0:
                st.success("No major improvements required.")

            else:

                for tip in tips:
                    st.write(tip)

        st.markdown("---")

        # --------------------------
        # Download Report
        # --------------------------

        st.info(
            "AI Resume Review will be available in the next update."
        )# =====================================================
# HIREHIVE AI CHATBOT
# =====================================================

elif page == "🤖 HireHive AI":

    st.title("🤖 HireHive AI Assistant")

    st.write(
        """
Ask me anything about:

• Placements
• Resume Building
• ATS Score
• DSA
• Programming
• Python
• Java
• AI & ML
• Interviews
• Career Guidance
"""
    )

    # Chat History
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Show previous messages
    for message in st.session_state.messages:

        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    prompt = st.chat_input("Ask HireHive AI...")

    if prompt:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": prompt
            }
        )

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.spinner("HireHive AI is Thinking..."):

            try:

                answer = ask_hirehive(prompt)

            except Exception as e:

                answer = f"Error:\n\n{e}"

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

        with st.chat_message("assistant"):

            st.markdown(answer)

    st.markdown("---")

    if st.button("🗑 Clear Chat"):

        st.session_state.messages = []

        st.rerun()

# =====================================================
# DASHBOARD
# =====================================================

elif page == "Dashboard":

    st.title("📊 HireHive Dashboard")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Dataset",
        "45,000 Students"
    )

    c2.metric(
        "Model",
        "Random Forest"
    )

    c3.metric(
        "Accuracy",
        "100%"
    )

    st.markdown("---")

    st.subheader("Feature Importance")

    feature_df = pd.DataFrame({

        "Feature":[
            "Communication Skills",
            "Backlogs",
            "CGPA",
            "Projects",
            "Coding Skills",
            "Certifications",
            "Aptitude",
            "Internships"
        ],

        "Importance":[
            30.3,
            17.7,
            15.4,
            12.9,
            10.3,
            6.3,
            5.9,
            0.9
        ]

    })

    st.bar_chart(
        feature_df.set_index("Feature")
    )

    st.markdown("---")

    st.subheader("Model Information")

    st.info(
        """
Model Used : Random Forest

Training Accuracy : 100%

Dataset Size : 45,000 Records

Prediction Type : Binary Classification
"""
    )

    st.markdown("---")

    st.subheader("Project Highlights")

    st.success("✔ Placement Prediction")

    st.success("✔ Resume Analyzer")

    st.success("✔ ATS Score")

    st.success("✔ AI Career Chatbot")

    st.success("✔ Company Recommendation")

    st.success("✔ PDF Report Generation")

    st.success("✔ Career Suggestions")