import requests
from bs4 import BeautifulSoup
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification



bias_tokenizer = AutoTokenizer.from_pretrained("cirimus/modernbert-large-bias-type-classifier")
bias_model = AutoModelForSequenceClassification.from_pretrained("cirimus/modernbert-large-bias-type-classifier")

fake_tokenizer = AutoTokenizer.from_pretrained("jy46604790/Fake-News-Bert-Detect")
fake_model = AutoModelForSequenceClassification.from_pretrained("jy46604790/Fake-News-Bert-Detect")

##This function will summarize the given text utilizng a AI model 
def summarize(url):
    article_text, article_title, authors, date = scrape(url)
    
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

    max_tokens = 1024
    truncated_text = " ".join(article_text.split()[:max_tokens])

    ARTICLE = summarizer(truncated_text, max_length=150, min_length=30, do_sample=False)

    summary_text = ARTICLE[0]['summary_text']

    return summary_text, article_title

def biasAnalysis(url):
    article_text, article_title, authors, date = scrape(url)
    pipe = pipeline("text-classification", model=bias_model, tokenizer=bias_tokenizer)
    analysis = pipe(article_text, truncation=True, padding=True, max_length=512)
    return analysis[0]['label'], analysis[0]['score']

def fakeAnalysis(url):
    article_text, article_title, authors, date = scrape(url)
    pipe = pipeline("text-classification", model=fake_model, tokenizer=fake_tokenizer)
    result = pipe(article_text, truncation=True, padding=True, max_length=512)
    return result[0]['label'] == 'LABEL_0'

def scrape(url: str):
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        # Extract the title if available
        title = soup.title.string.strip() if soup.title else "Unknown Title"

        # Find all paragraphs inside <article> first, fallback to all <p> tags
        article_tag = soup.find("article")
        if article_tag:
            paragraphs = [p.get_text().strip() for p in article_tag.find_all("p")]
        else:
            paragraphs = [p.get_text().strip() for p in soup.find_all("p")]

        # Join all text together
        article_text = " ".join(paragraphs)

        # Optional metadata
        authors = "Unknown"
        date = "Unknown"

        if not article_text:
            article_text = "No article content found."

        return article_text, title, authors, date

    except Exception as e:
        print(f"Scraping error for {url}: {e}")
        return "", "Error", "Error", "Error"