import fitz

SKILLS = [
    "Python","Java","C++","C","SQL","MySQL","MongoDB",
    "Machine Learning","Deep Learning","Artificial Intelligence",
    "Data Science","Pandas","NumPy","Scikit-Learn",
    "TensorFlow","PyTorch","Flask","FastAPI",
    "HTML","CSS","JavaScript","React","Node.js",
    "Git","GitHub","Docker","Kubernetes",
    "AWS","Azure","Linux","Networking",
    "Cyber Security","DSA","OOP","DBMS"
]


def extract_resume_text(uploaded_file):

    text = ""

    pdf = fitz.open(
        stream=uploaded_file.read(),
        filetype="pdf"
    )

    for page in pdf:
        text += page.get_text()

    pdf.close()

    return text


def detect_skills(text):

    found = []

    lower_text = text.lower()

    for skill in SKILLS:

        if skill.lower() in lower_text:
            found.append(skill)

    return found


def missing_skills(found_skills):

    return [skill for skill in SKILLS if skill not in found_skills]


def calculate_ats_score(text, found_skills):

    score = 0

    # Skills
    score += min(len(found_skills) * 2, 40)

    # Projects
    if "project" in text.lower():
        score += 15

    # Internship
    if "internship" in text.lower():
        score += 15

    # Education
    if "b.tech" in text.lower() or "bachelor" in text.lower():
        score += 10

    # Certifications
    if "certificate" in text.lower() or "certification" in text.lower():
        score += 10

    # Contact Information
    if "@" in text:
        score += 5

    if score > 100:
        score = 100

    return score