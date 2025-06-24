# analysis/skill_analysis.py
from collections import Counter
import pandas as pd

def extract_top_skills(jobs_df, top_n=10):
    skill_keywords = [
        "python", "sql", "excel", "aws", "azure", "cloud",
        "power bi", "machine learning", "ml", "tableau",
        "spark", "java", "c++", "pandas", "data analysis", "react", "node"
    ]
    
    counter = Counter()
    for desc in jobs_df["job_description"].dropna():
        text = desc.lower()
        for skill in skill_keywords:
            if skill in text:
                counter[skill] += 1

    return pd.DataFrame(counter.most_common(top_n), columns=["Skill", "Frequency"])
