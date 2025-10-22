from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os
from app.analyzer import fakeAnalysis, biasAnalysis, summarize 

app = FastAPI()

# Path to the frontend folder
frontend_path = os.path.join(os.path.dirname(__file__), "../frontend")

# Serve static files (CSS, JS, images, etc.)
app.mount("/static", StaticFiles(directory=frontend_path), name="static")

# Serve index.html at root
@app.get("/")
async def serve_index():
    index_file = os.path.join(frontend_path, "index.html")
    return FileResponse(index_file)

class Url(BaseModel):
    url: str

class Output(BaseModel):
    summary: str
    credibility_score: int
    fake_score: str
    bias_label: str

## Once called, analyze will send the url to the backend scraper to analyze and retrieve information
@app.post("/app/analyze", response_model=Output)
def get_item(url: Url):
    ##We need to access the url within the model, thus we us url.url
    parsed_url = url.url
    fake_score = fakeAnalysis(parsed_url)
    ## Bias analysis and summarize return tuples thus we need to extract them
    bias_label, bias_score = biasAnalysis(parsed_url)
    summary = summarize(parsed_url)[0]

    if fake_score == True:
        to_string = "Possibly Fake News Article"
    else:
        to_string = "Article appears to be Real!"

    return {"summary": summary, "credibility_score": bias_score, "fake_score": to_string, "bias_label":bias_label}