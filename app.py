from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from pipeline import pipeline_status, run_pipeline

app = FastAPI(title="Shorts Revenue AI", version="0.2.0")

class ScriptRequest(BaseModel):
    topic: str = Field(min_length=2, max_length=500)
    language: str = "both"
    duration_seconds: int = Field(default=45, ge=15, le=180)

@app.get("/")
def root():
    return {"service": "shorts-revenue-ai", "status": "ok", "version": "0.2.0"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/pipeline/status")
def status():
    return pipeline_status()

@app.post("/pipeline/script")
def script(req: ScriptRequest):
    result = run_pipeline(req.topic, req.language, req.duration_seconds)
    if not result.get("ok"):
        raise HTTPException(status_code=503, detail=result)
    return result
