from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os
from app.analyzer import fakeAnalysis, biasAnalysis, summarize, scrape

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
    title: Optional[str] = None
    authors: Optional[list[str]] = None
    date: Optional[str] = None
    summary: Optional[str] = None
    credibility_score: Optional[int] = None
    fake_score: Optional[str] = None
    bias_label: Optional[str] = None

## Once called, analyze will send the url to the backend scraper to analyze and retrieve information
@app.post("/app/analyze", response_model=Output)
def get_item(url: Url):
    parsed_url = url.url
    try:
        summary, title = summarize(parsed_url)
        bias_label, bias_score = biasAnalysis(parsed_url)
        is_fake = fakeAnalysis(parsed_url)
    except Exception as e:
        return {
            "title": "",
            "authors": [],
            "date": "",
            "summary": "",
            "credibility_score": 0,
            "fake_score": f"Error: {str(e)}",
            "bias_label": "Error"
        }
    fake_text = "Possibly Fake News Article" if is_fake else "Article appears to be Real!"

    return {
        "title": title,
        "authors": [],
        "date": "",
        "summary": summary,
        "credibility_score": round(bias_score * 100),
        "fake_score": fake_text,
        "bias_label": bias_label
    }