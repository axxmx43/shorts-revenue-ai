"""Starter orchestration for the Shorts production workflow.

Integrations are intentionally stubbed until API credentials and channel access
are configured. This avoids accidental publishing or spending.
"""
from datetime import datetime, timezone

STAGES = [
    "research", "planning", "script", "voice_video", "quality_check",
    "approval", "publish", "analytics", "optimization",
]

def pipeline_status():
    return {
        "mode": "scaffold",
        "stages": STAGES,
        "ready_to_publish": False,
        "message": "Connect credentials and configure workflow before publishing.",
        "checked_at": datetime.now(timezone.utc).isoformat(),
    }


def run_pipeline(topic: str | None = None):
    """Placeholder entry point; integrations will be added in subsequent commits."""
    return {
        "topic": topic,
        "completed": [],
        "blocked_at": "research",
        "reason": "vidIQ/LLM/HeyGen/YouTube credentials are not configured yet.",
    }
