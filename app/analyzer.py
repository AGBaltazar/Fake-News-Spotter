from newspaper import Article
from transformers import AutoTokenizer, pipeline, TFAutoModelForSequenceClassification, AutoModelForSequenceClassification

##Changed from utilizing AI for the Summary to Newspaper3k due to limitations
def summarize(url):
    title, authors, summary= scrape(url)
    return title, authors, summary  

def biasAnalysis(url):
    title, authors, summary= scrape(url)
    tokenizer = AutoTokenizer.from_pretrained("d4data/bias-detection-model")
    model = TFAutoModelForSequenceClassification.from_pretrained("d4data/bias-detection-model")

    classifier = pipeline('text-classification', model=model, tokenizer=tokenizer) 
    bias_result = classifier(summary)
    print(f"Bias Score: {bias_result}")
    
    return bias_result[0]['label'], bias_result[0]['score']


def fakeAnalysis(url):
    article_title, authors, summary= scrape(url)
    tokenizer = AutoTokenizer.from_pretrained("jy46604790/Fake-News-Bert-Detect")
    model = AutoModelForSequenceClassification.from_pretrained("jy46604790/Fake-News-Bert-Detect")
    classifier= pipeline(summary, model=model, tokenizer=tokenizer)
    result = classifier(summary)
    return result[0]['label'] == 'LABEL_0'

def scrape(url: str):
    article = Article(url)

    article.download()

    article.parse()

    article.nlp()

    summary = article.summary
    title = article.title
    authors = ", ".join(article.authors)

    return title, authors, summary