from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os
from app.analyzer import summarize, biasAnalysis, fakeAnalysis


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
    summary: Optional[str] = None
    bias_score: Optional[int] = None
    fake_score: Optional[str] = None
    bias_label: Optional[str] = None

## Once called, analyze will send the url to the backend scraper to analyze and retrieve information
@app.post("/app/analyze")
def get_item(url: Url):
    parsed_url = url.url
    print(f"Received URL: {parsed_url}")
    try:
        title, authors, summary = summarize(parsed_url)
        print(f"Received from Analyzer: {title, authors, summary}")
        bias_label, bias_score = biasAnalysis(parsed_url)
        fake_label, fake_score = fakeAnalysis(parsed_url)

        label_map = {"LABEL_0": "Fake News", "LABEL_1": "Real News"}
        fake_text = f"{label_map.get(fake_label, fake_label)} ({fake_score:.2f})"
 
        return {
            "title": title,
            "authors": authors,
            "summary": summary,
            "fake_score": fake_text,
            "bias_label": bias_label,
            "bias_score": bias_score
        }
    except Exception as e:
        print(f"Backend  Error: {e}")