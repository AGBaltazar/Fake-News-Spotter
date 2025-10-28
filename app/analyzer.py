from newspaper import Article
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
    article = Article(url)

    article.download()

    article.parse()

    article.nlp()

    text = article.text
    title = article.title
    authors = ", ".join(article.authors)
    date = article.publish_date.isoformat() if article.publish_date else "Unknown"

    return text, title, authors, date
