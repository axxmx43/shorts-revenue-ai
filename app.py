import os
import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from pipeline import pipeline_status, run_pipeline

app = FastAPI(title="Shorts Revenue AI", version="0.3.0")

class ScriptRequest(BaseModel):
    topic: str = Field(min_length=2, max_length=500)
    language: str = "both"
    duration_seconds: int = Field(default=45, ge=15, le=180)

@app.get("/")
def root():
    return {"service": "shorts-revenue-ai", "status": "ok", "version": "0.3.0"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/pipeline/status")
def status():
    return pipeline_status()

@app.get("/youtube/oauth/check")
def youtube_oauth_check():
    """Verify the stored YouTube OAuth refresh token without exposing credentials."""
    client_id = os.getenv("YOUTUBE_CLIENT_ID")
    client_secret = os.getenv("YOUTUBE_CLIENT_SECRET")
    refresh_token = os.getenv("YOUTUBE_REFRESH_TOKEN")
    if not all((client_id, client_secret, refresh_token)):
        return {
            "ok": False,
            "connected": False,
            "reason": "Missing one or more YouTube OAuth environment variables.",
            "required": ["YOUTUBE_CLIENT_ID", "YOUTUBE_CLIENT_SECRET", "YOUTUBE_REFRESH_TOKEN"],
        }
    try:
        response = httpx.post(
            "https://oauth2.googleapis.com/token",
            data={
                "client_id": client_id,
                "client_secret": client_secret,
                "refresh_token": refresh_token,
                "grant_type": "refresh_token",
            },
            timeout=20,
        )
        if response.status_code != 200:
            # Do not return Google's response body: it can contain sensitive diagnostic data.
            return {
                "ok": False,
                "connected": False,
                "reason": "Google rejected the refresh token. Re-authorize the YouTube account.",
                "google_status": response.status_code,
            }
        token_data = response.json()
        return {
            "ok": True,
            "connected": True,
            "token_type": token_data.get("token_type"),
            "expires_in": token_data.get("expires_in"),
            "message": "YouTube OAuth refresh succeeded. No video was uploaded.",
        }
    except httpx.HTTPError:
        raise HTTPException(status_code=502, detail="Could not reach Google's OAuth endpoint.")

@app.post("/pipeline/script")
def script(req: ScriptRequest):
    result = run_pipeline(req.topic, req.language, req.duration_seconds)
    if not result.get("ok"):
        raise HTTPException(status_code=503, detail=result)
    return result
