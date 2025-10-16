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

    return summary_text

def biasAnalysis(url):
    article_text= scrape(url)

    pipe = pipeline("text-classification", model="d4data/bias-detection-model")

    analysis = pipe(article_text)

    return analysis

## def fakeAnalisys(url):


def scrape(url: str):
    article = Article(url)

    article.download()

    article.parse()

    article.nlp()

    author = article.authors
    date = article.publish_date
    text = article.text
    title = article.title

    return author, date, text, title

## def sendToDom():