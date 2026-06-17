import streamlit as st
import pdfplumber
import pandas as pd
from placement_predictor import predict_placement

st.title("AI Career Intelligence Platform")

uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

# ---------- Extract Resume Text ----------
def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
    return text

# ---------- Extract Skills ----------
def extract_skills(resume_text):
    with open("skills_master.txt") as f:
        skills_list = f.read().splitlines()
    found_skills = []
    for skill in skills_list:
        if skill.lower() in resume_text.lower():
            found_skills.append(skill)
    return found_skills

# ---------- Extract Resume Features ----------
def extract_internships(text):
    keywords = ["internship","intern","trainee"]
    return sum(text.lower().count(word) for word in keywords)

def extract_projects(text):
    keywords = ["project","developed","implemented","designed"]
    return sum(text.lower().count(word) for word in keywords)

def extract_certifications(text):
    keywords = ["certification","certificate","certified"]
    return sum(text.lower().count(word) for word in keywords)

def extract_workshops(text):
    keywords = ["workshop","training","bootcamp"]
    return sum(text.lower().count(word) for word in keywords)

def extract_coding_score(text):
    coding_skills = [
        "python","java","c++","sql",
        "machine learning","deep learning",
        "data structures","algorithms"
    ]
    return sum(1 for skill in coding_skills if skill in text.lower())

# ---------- Job Compatibility ----------
def match_roles(user_skills):
    df = pd.read_csv("job_description.csv")
    results = []
    for _, row in df.iterrows():
        role = row["role"]
        role_skills = row["skills"].split()
        matched = set(user_skills) & set(role_skills)
        match_percent = (len(matched)/len(role_skills))*100
        missing = set(role_skills) - set(user_skills)
        results.append({
            "role": role,
            "match": round(match_percent,2),
            "missing": list(missing)
        })
    return sorted(results,key=lambda x:x["match"],reverse=True)

# ---------- Main Program ----------
if uploaded_file is not None:

    resume_text = extract_text_from_pdf(uploaded_file)

    # Resume Analysis
    skills = extract_skills(resume_text)
    technical_skills = len(skills)
    internships = extract_internships(resume_text)
    projects = extract_projects(resume_text)
    certifications = extract_certifications(resume_text)
    workshops = extract_workshops(resume_text)
    coding_score = extract_coding_score(resume_text)

    st.subheader("Resume Analysis")
    st.write("Technical Skills:", technical_skills)
    st.write("Internships:", internships)
    st.write("Projects:", projects)
    st.write("Certifications:", certifications)
    st.write("Workshops:", workshops)
    st.write("Coding Score:", coding_score)
    st.write("Extracted Skills:", skills)

    # Job Compatibility
    st.subheader("Job Compatibility")
    roles = match_roles(skills)
    for r in roles[:3]:
        st.write("Role:", r["role"])
        st.write("Match %:", r["match"])
        st.write("Missing Skills:", r["missing"])
        st.write("---")

    # Placement Prediction
    st.header("Placement Prediction")
    cgpa = st.number_input("Enter CGPA", 0.0, 10.0)
    communication = st.slider("Communication Score",0,10)
    backlogs = st.number_input("Backlogs",0,10)

    if st.button("Predict Placement Probability"):
        features = [
            cgpa,
            communication,
            backlogs,
            internships,
            projects,
            technical_skills,
            certifications,
            workshops,
            coding_score
        ]
        prediction = predict_placement(features)
        st.success(f"Placement Probability: {prediction}%")

        if prediction >= 85:
            st.success("Excellent Placement Chances")
        elif prediction >= 70:
            st.info("Good Placement Chances")
        elif prediction >= 50:
            st.warning("Average Placement Chances")
        else:
            st.error("Low Placement Probability - Improve Skills")