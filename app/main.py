from typing import Optional

from fastapi import FastAPI
from scraper import article, author, text

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

## Once called, analyze will take information from the python modules and send it in JSON 
@app.get("/app/analyze")
def read_item(text: str, q: Optional[str] = None):

    summary = f"Summary of: {text}"
    credibility_score = 75  # example
    explanation = f"Analysis of '{text}' with optional param q={q}"

    return {
        "summary": summary,
        "credibility_score": credibility_score,
        "explanation": explanation
    }