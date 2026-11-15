"""Shorts Revenue AI: safe MVP orchestration and script generation."""
import os
from datetime import datetime, timezone
import httpx

STAGES = ["research", "planning", "script", "voice_video", "quality_check", "approval", "publish", "analytics", "optimization"]

def configured():
    return {
        "openai": bool(os.getenv("OPENAI_API_KEY")),
        "heygen": bool(os.getenv("HEYGEN_API_KEY")),
        "vidiq": bool(os.getenv("VIDIQ_API_KEY")),
        "youtube_oauth": all(os.getenv(k) for k in ("YOUTUBE_CLIENT_ID", "YOUTUBE_CLIENT_SECRET", "YOUTUBE_REFRESH_TOKEN")),
    }

def pipeline_status():
    c = configured()
    blockers = [k for k, v in c.items() if not v]
    return {
        "mode": "mvp",
        "stages": STAGES,
        "integrations": c,
        "ready_to_publish": not blockers,
        "publish_safety": "approval_required",
        "blockers": blockers,
        "message": "Credentials are checked; publishing remains approval-gated.",
        "checked_at": datetime.now(timezone.utc).isoformat(),
    }

def generate_script(topic: str, language: str = "both", duration_seconds: int = 45):
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY is not configured in Render.")
    prompt = f"""Create one original YouTube Shorts script about: {topic}
Language: {language} (both means Japanese and English versions).
Target duration: {duration_seconds} seconds. Faceless format, strong first 2 seconds,
clear value/story, concise spoken narration, visual/B-roll cues, and a natural CTA.
Avoid unsupported factual claims. Return JSON with keys title_ja,title_en,hook_ja,hook_en,
script_ja,script_en,visuals,description_ja,description_en,hashtags."""
    with httpx.Client(timeout=60) as client:
        r = client.post("https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
            json={"model": os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
                  "messages":[{"role":"system","content":"You are an expert Shorts producer. Output valid JSON only."},
                             {"role":"user","content":prompt}],
                  "response_format":{"type":"json_object"}})
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"]

def run_pipeline(topic: str | None = None, language: str = "both", duration_seconds: int = 45):
    if not topic or not topic.strip():
        return {"ok": False, "blocked_at": "planning", "reason": "topic is required"}
    try:
        script = generate_script(topic.strip(), language, duration_seconds)
    except Exception as e:
        return {"ok": False, "blocked_at": "script", "reason": str(e), "status": pipeline_status()}
    return {"ok": True, "topic": topic, "script": script, "next": "Review script, then video generation; upload requires OAuth and approval."}
