from newspaper import Article
from transformers import pipeline

##This function will summarize the given text utilizng a AI model 
def summarize(url):
    article_text, article_title= scrape(url)

    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

    ARTICLE = summarizer(article_text)

    summary_text = ARTICLE[0]['summary_text']

    print("Title:", article_title)
    print("Summary:", summary_text)

    return summary_text, article_title

def biasAnalysis(url):
    article_text, article_title= scrape(url)

    pipe = pipeline("text-classification", model="cirimus/modernbert-large-bias-type-classifier")

    analysis = pipe(article_text)

    return analysis[0]['label'], analysis[0]['score']

def fakeAnalysis(url):
    isFake = False

    article_text, article_title= scrape(url)

    pipe = pipeline("text-classification", model="jy46604790/Fake-News-Bert-Detect")

    result = pipe(article_text)

    if result[0]['label'] == 'LABEL_0':
        isFake = True
    else:
        isFake = False

    return isFake

def scrape(url: str):
    article = Article(url)

    article.download()

    article.parse()

    article.nlp()

    text = article.text
    title = article.title

    return text, title
