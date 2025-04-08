import os
import json
import requests
from pathlib import Path
from io import BytesIO
from PyPDF2 import PdfReader
from transformers import pipeline
from keybert import KeyBERT

# Initialize the models
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
kw_model = KeyBERT()

ARTICLES_DIR = Path("articles")
OUTPUT_DIR = Path("drafts")
OUTPUT_DIR.mkdir(exist_ok=True)

# Download PDF from URL
def download_pdf(url):
    response = requests.get(url)
    if response.status_code == 200:
        return BytesIO(response.content)
    else:
        raise Exception(f"Failed to download PDF from {url}")

# Extract text from PDF
def extract_pdf_text(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# Summarize text
def summarize(text):
    chunks = [text[i:i+1000] for i in range(0, len(text), 1000)]
    summary = ""
    for chunk in chunks:
        summary += summarizer(chunk, max_length=100, min_length=30, do_sample=False)[0]['summary_text'] + " "
    return summary.strip()

# Extract keywords
def extract_keywords(text):
    return kw_model.extract_keywords(text, stop_words='english', top_n=5)

# Draft video script
def draft_video_script(title, summary, keywords):
    return f"""# 🎬 Video Scenario for LinkedIn

**Title**: {title}

**Problem**: People are struggling with...

**Insight**: {summary}

**Key Topics**: {', '.join([kw[0] for kw in keywords])}

**Ending Hook**: What if we could use this to improve X? Let's talk!

---"""

# Process article from URL
def process_article(url):
    pdf_file = download_pdf(url)
    text = extract_pdf_text(pdf_file)
    title = url.split("/")[-1].replace(".pdf", "")
    summary = summarize(text)
    keywords = extract_keywords(text)
    script = draft_video_script(title, summary, keywords)

    out_path = OUTPUT_DIR / f"{title}.md"
    with open(out_path, "w") as f:
        f.write(script)

# Read configuration file with URLs
def read_config(config_file="config.json"):
    with open(config_file, "r") as file:
        config = json.load(file)
    return config["pdf_urls"]

if __name__ == "__main__":
    # Read URLs from config file
    urls = read_config()
    
    # Process each URL in the config file
    for url in urls:
        process_article(url)

