# matcher/matcher.py
import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def load_jobs(path=None):
    if not path:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(current_dir, "..", "jobs_data", "jobs.csv")
    
    df = pd.read_csv(path)
    df.dropna(subset=["job_description"], inplace=True)
    return df
def match_resume_to_jobs(resume_skills, jobs_df, top_n=5):
    # Combine resume skills into a string
    resume_text = " ".join(resume_skills)

    # TF-IDF Vectorizer
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(jobs_df['job_description'].tolist() + [resume_text])

    # Last vector is the resume
    resume_vector = tfidf_matrix[-1]
    job_vectors = tfidf_matrix[:-1]

    # Calculate cosine similarity
    similarity_scores = cosine_similarity(resume_vector, job_vectors).flatten()
    jobs_df["match_score"] = similarity_scores

    # Return top N jobs
    return jobs_df.sort_values(by="match_score", ascending=False).head(top_n)

# Example Usage
if __name__ == "__main__":
    # Simulated extracted skills from resume
    resume_skills = ["python", "sql", "data analysis", "excel", "power bi"]

    jobs_df = load_jobs()
    matched_jobs = match_resume_to_jobs(resume_skills, jobs_df, top_n=5)

    print("Top Matching Jobs:")
    print(matched_jobs[["job_title", "location", "match_score", "job_description"]])
