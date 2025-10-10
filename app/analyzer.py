from newspaper import Article

def analyze(url):
    article_author, article_date, article_text, article_title, article_summary = scrape(url)


    

def scrape(url: str):
    article = Article(url)

    article.download()

    article.parse()

    article.nlp()

    author = article.authors
    date = article.publish_date
    text = article.text
    title = article.title
    summary = article.summary

    return author, date, text, title, summary

