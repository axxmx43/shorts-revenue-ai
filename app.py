from fastapi import FastAPI
from pipeline import pipeline_status

app = FastAPI(title="Shorts Revenue AI", version="0.1.0")

@app.get("/")
def root():
    return {"service": "shorts-revenue-ai", "status": "ok"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/pipeline/status")
def status():
    return pipeline_status()
