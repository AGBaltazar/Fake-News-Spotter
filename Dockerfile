# Use official Python 3.12 slim image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Ensure NLTK data for newspaper3k NLP
RUN python -m nltk.downloader punkt punkt_tab

# Copy all project files
COPY . .

ENV PYTHONPATH=/app

# Expose port for FastAPI
EXPOSE 8080

# Run FastAPI app with uvicorn
CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "8080"]
