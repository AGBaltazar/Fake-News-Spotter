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
    parsed_url = url.url
    try:
        fake_score = fakeAnalysis(parsed_url)
        bias_label, bias_score = biasAnalysis(parsed_url)
        summary = summarize(parsed_url)[0]
    except Exception as e:
        return {"summary": "", "credibility_score": 0, "fake_score": f"Error: {str(e)}", "bias_label": "Error"}

    to_string = "Possibly Fake News Article" if fake_score else "Article appears to be Real!"
    return {"summary": summary, "credibility_score": bias_score, "fake_score": to_string, "bias_label": bias_label}
