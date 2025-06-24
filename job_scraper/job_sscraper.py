# job_scraper.py
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

BASE_URL = "https://in.indeed.com/jobs?q=data+analyst&start="
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/113.0.0.0 Safari/537.36"
}


def scrape_indeed_jobs(pages=3):
    job_list = []

    for page in range(pages):
        print(f"Scraping page {page + 1}...")
        url = BASE_URL + str(page * 10)
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        jobs = soup.find_all("a", class_="tapItem")

        for job in jobs:
            title = job.find("h2", class_="jobTitle").text.strip() if job.find("h2", class_="jobTitle") else None
            company = job.find("span", class_="companyName").text.strip() if job.find("span", class_="companyName") else None
            location = job.find("div", class_="companyLocation").text.strip() if job.find("div", class_="companyLocation") else None
            summary = job.find("div", class_="job-snippet").text.strip().replace('\n', ' ') if job.find("div", class_="job-snippet") else None

            job_list.append({
                "title": title,
                "company": company,
                "location": location,
                "description": summary
            })

        time.sleep(1)  # Be respectful to the server
        print(response.text[:1000])  # Just first 1000 characters to inspect


    return pd.DataFrame(job_list)

if __name__ == "__main__":
    df = scrape_indeed_jobs(pages=5)
    df.to_csv("../jobs_data/jobs.csv", index=False)
    print("✅ Job data saved to jobs_data/jobs.csv")
