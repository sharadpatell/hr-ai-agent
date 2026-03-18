import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime
from urllib.parse import urlparse


URLS = [
    "https://www.simplilearn.com/hr-interview-questions-answers-article",
    "https://www.indeed.com/career-advice/interviewing/hr-interview-questions",
    "https://www.geeksforgeeks.org/hr-interview-questions/",
    "https://www.interviewbit.com/hr-interview-questions/",
    "https://www.indiabix.com/hr-interview/questions-and-answers/",
    "https://www.hibob.com/blog/hr-interview-questions/",
    "https://www.gsdcouncil.org/blogs/mastering-interview-questions-for-hr-position-candidates",
    "https://www.fita.in/top-hr-interview-questions-and-answers/",
    "https://www.themuse.com/advice/interview-questions-and-answers",
    "https://prepinsta.com/interview-preparation/hr-interview-questions/",
    "https://www.naukri.com/blog/frequently-asked-hr-interview-questions-and-answers/",
    "https://www.linkedin.com/pulse/27-most-common-job-interview-questions-answers-jeff-haden"
]


LOG_FILE = "logs/scraper.log"


def log(message):
    os.makedirs("logs", exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write(f"{datetime.now()} | {message}\n")


def get_domain_name(url):
    domain = urlparse(url).netloc
    return domain.replace("www.", "").replace(".", "_")


def scrape_site(url):
    try:
        log(f"START scraping: {url}")

        # response = requests.get(url, timeout=10)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
        }

        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code != 200:
            log(f"FAILED request: {url} | Status: {response.status_code}")
            return ""

        soup = BeautifulSoup(response.text, "html.parser")
        paragraphs = soup.find_all("p")

        text = "\n".join([
            p.get_text().strip()
            for p in paragraphs
            if p.get_text().strip()
        ])

        log(f"SUCCESS scraping: {url} | Paragraphs: {len(paragraphs)}")

        return text

    except Exception as e:
        log(f"ERROR scraping: {url} | Error: {str(e)}")
        return ""


def save_data():
    os.makedirs("data/raw", exist_ok=True)

    total_docs = 0

    for url in URLS:
        text = scrape_site(url)

        if not text:
            log(f"EMPTY content skipped: {url}")
            continue

        domain_name = get_domain_name(url)
        file_path = f"data/raw/{domain_name}.txt"

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(text)

        total_docs += 1

        log(f"SAVED file: {file_path} | Length: {len(text)}")

    log(f"TOTAL FILES SAVED: {total_docs}")


if __name__ == "__main__":
    log("===== SCRAPER STARTED =====")
    save_data()
    log("===== SCRAPER COMPLETED =====\n")