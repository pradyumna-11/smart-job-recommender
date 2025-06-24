# app/app.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import streamlit as st
from resume_parser.parser import extract_resume_text, extract_skills_from_text, extract_education, extract_experience
from matcher.matcher import load_jobs, match_resume_to_jobs
import tempfile
from analysis.skill_analysis import extract_top_skills
from analysis.plot import plot_top_skills
from analysis.forecast import prepare_skill_timeseries, forecast_skill_trend
import streamlit as st

st.set_page_config(page_title="Smart Job Recommender", layout="centered")

st.title("💼 Smart Job Recommender System")
st.write("Upload your resume (PDF) to get job recommendations.")

# File uploader
uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file.write(uploaded_file.read())
        temp_path = temp_file.name

    # Resume parsing
    resume_text = extract_resume_text(temp_path)
    skills = extract_skills_from_text(resume_text)
    education = extract_education(resume_text)
    experience = extract_experience(resume_text)

    st.subheader("📄 Resume Summary")
    st.write("**Skills:**", ", ".join(skills))
    st.write("**Education:**", education)
    st.write("**Experience:**", f"{experience} years")

    # Load jobs and match
    st.subheader("🔍 Top Job Matches")
    jobs_df = load_jobs()
    matched_jobs = match_resume_to_jobs(skills, jobs_df)
    st.subheader("📄 Job Recommendations")
    top_n = st.slider("Select number of jobs to display", min_value=5, max_value=50, value=20, step=5)

    # 🆕 Apply the limit dynamically
    top_matches = match_resume_to_jobs(skills, jobs_df,top_n)

    # 🆕 Display top job matches
    # for index, row in top_matches.iterrows():
    #     st.markdown(f"**{row['job_title']}** at `{row['organization']}`")
    #     st.write(f"📍 {row['location']}")
    #     st.write(f"🧠 Sector: {row['sector']}")
    #     st.write(f"🔗 [View Job Posting]({row['page_url']})", unsafe_allow_html=True)
    #     st.markdown("---")

    for idx, row in top_matches.iterrows():
        st.markdown(f"### {row['job_title']}")
        st.write(f"📍 {row['location']}  |  🔧 Match Score: **{row['match_score']:.2f}**")
        st.write(row['job_description'][:300] + "...")
        st.markdown(f"[🔗 View Job Posting]({row['page_url']})", unsafe_allow_html=True)
        st.markdown("---")

    # Seaborn + Matplotlib chart
    st.subheader("📊 In-Demand Tech Skills (From Job Descriptions)")
    skills_df = extract_top_skills(jobs_df)
    fig = plot_top_skills(skills_df)
    st.pyplot(fig)  # ✅ no warning, no deprecated usage
    

    st.subheader("🔮 Skill Demand Forecast")
    selected_skill = st.selectbox("Select a skill to forecast", skills_df["Skill"])
    skill_timeseries = prepare_skill_timeseries(jobs_df, selected_skill)
    forecast_fig = forecast_skill_trend(skill_timeseries)
    st.pyplot(forecast_fig)
