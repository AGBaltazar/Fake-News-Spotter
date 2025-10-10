from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI
from analyzer import analyze

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

class Url(BaseModel):
    url: str

class Output(BaseModel):
    summary: str
    credibility_score: int
    explanation: str

## Once called, analyze will send the url to the backend scraper to analyze
@app.post("/app/analyze")
def get_item(url: str, q: Optional[str] = None):

    analyze(url)
