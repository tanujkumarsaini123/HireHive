from utils.career_advice import career_advice
from utils.recommendation import recommend_companies
from utils.pdf_generator import generate_report

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
        "Dashboard",
        "About"
    ]
)

# =====================================================
# HOME PAGE
# =====================================================

if page == "Home":

    st.title("💼 HireHive")

    st.subheader("AI Placement Assistant")

    st.write("""
Welcome to HireHive.

This application predicts whether a student is likely to get placed
using Machine Learning and provides personalized career guidance.
""")

    st.markdown("---")

    c1, c2, c3 = st.columns(3)

    c1.metric("Model", "Random Forest")
    c2.metric("Dataset", "45,000 Students")
    c3.metric("Accuracy", "100%")

    st.info("Select 'Placement Prediction' from the left sidebar to begin.")

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

    predict = st.button("Predict Placement")

    if predict:

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
        st.markdown("---")

        st.header("Prediction Result")

        if prediction == 1:
            st.success("🎉 Student is Likely to be Placed")
        else:
            st.error("❌ Student is Likely to be Not Placed")

        st.metric(
            "Placement Probability",
            f"{probability:.2f}%"
        )

        st.progress(probability / 100)

        st.write("")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Readiness Score",
                f"{round(probability/10,1)}/10"
            )

        with col2:

            if probability >= 80:
                status = "Excellent"

            elif probability >= 60:
                status = "Good"

            else:
                status = "Needs Improvement"

            st.metric("Status", status)

        st.markdown("---")

        # =====================================================
        # COMPANY RECOMMENDATION
        # =====================================================

        st.subheader("🏢 Recommended Companies")

        companies = recommend_companies(
            probability,
            cgpa,
            coding,
            internships
        )

        for company in companies:
            st.write(f"✅ {company}")

        st.markdown("---")

        # =====================================================
        # CAREER ADVICE
        # =====================================================

        st.subheader("🎯 Career Improvement Suggestions")

        tips = career_advice(
            cgpa,
            coding,
            communication,
            internships,
            projects,
            backlogs
        )

        for tip in tips:
            st.write(tip)

        st.markdown("---")

        # =====================================================
        # PDF REPORT
        # =====================================================

        st.subheader("📄 Placement Report")

        report_data = {
            "Age": age,
            "Gender": gender,
            "Degree": degree,
            "Branch": branch,
            "Prediction": "Placed" if prediction == 1 else "Not Placed",
            "Probability": probability,
            "Companies": companies,
            "Suggestions": tips
        }

        generate_report(
            "Placement_Report.pdf",
            report_data
        )

        with open("Placement_Report.pdf", "rb") as pdf_file:

            st.download_button(
                label="⬇ Download Placement Report",
                data=pdf_file,
                file_name="HireHive_Placement_Report.pdf",
                mime="application/pdf"
            )
            # =====================================================
# DASHBOARD
# =====================================================

elif page == "Dashboard":

    st.title("📊 Dashboard")

    c1, c2, c3 = st.columns(3)

    c1.metric("Dataset", "45,000 Students")
    c2.metric("Model", "Random Forest")
    c3.metric("Accuracy", "100%")

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

    st.info(
        "The chart shows which features contribute the most to placement prediction."
    )

# =====================================================
# ABOUT
# =====================================================

else:

    st.title("💼 About HireHive")

    st.write("""
HireHive is an AI-powered Placement Prediction System.

The project predicts a student's placement probability using Machine Learning and provides personalized career guidance and company recommendations.

### Project Workflow

1. Data Collection

2. Data Preprocessing

3. Feature Encoding

4. Random Forest Model Training

5. Placement Prediction

6. Career Guidance

7. Company Recommendation

### Technologies Used

- Python
- Streamlit
- Pandas
- Scikit-Learn
- Random Forest
- ReportLab (PDF Generation)

### Team Project

Developed as a Machine Learning academic project.
""")