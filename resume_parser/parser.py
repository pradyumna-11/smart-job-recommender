# resume_parser/parser.py
from pdfminer.high_level import extract_text
import spacy
import re

# Load spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    import subprocess
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")


# Sample skill set (you can extend this)
SKILL_DB = [
    "python", "java", "c++", "sql", "javascript", "react", "node.js", "aws",
    "power bi", "machine learning", "data analysis", "excel", "pandas", "numpy"
]

def extract_resume_text(pdf_path):
    return extract_text(pdf_path)

def extract_skills_from_text(text):
    doc = nlp(text.lower())
    extracted_skills = set()
    for token in doc:
        if token.text in SKILL_DB:
            extracted_skills.add(token.text)
    return list(extracted_skills)

def extract_education(text):
    education_keywords = ["b.tech", "b.e", "m.tech", "mca", "bachelor", "master", "phd"]
    education_found = []
    lines = text.lower().split("\n")
    
    for line in lines:
        for keyword in education_keywords:
            if keyword in line:
                education_found.append(line.strip())
                break  # Avoid duplicates if multiple keywords in the same line
    
    return education_found

def extract_experience(text):
    # Simple pattern to match "X years of experience"
    experience_pattern = r"(\d+)\s+years?\s+of\s+experience"
    matches = re.findall(experience_pattern, text.lower())

    total_experience = sum([int(x) for x in matches]) if matches else 0
    return total_experience


if __name__ == "__main__":
    resume_text = extract_resume_text("resume_sample.pdf")
    
    skills = extract_skills_from_text(resume_text)
    education = extract_education(resume_text)
    experience_years = extract_experience(resume_text)
    
    print("Extracted Skills:", skills)
    print("Education Info:", education)
    print("Total Experience (Years):", experience_years)

