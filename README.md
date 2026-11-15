# Shorts Revenue AI

Automated YouTube Shorts production pipeline (Japanese + English; faceless-first).

## Current MVP
- FastAPI health and pipeline-status endpoints
- OpenAI-powered bilingual Shorts script generation endpoint
- Credential readiness checks
- Publishing is intentionally approval-gated (no unattended upload yet)

## Deploy
Render Web Service: https://shorts-revenue-ai.onrender.com
Dashboard: https://dashboard.render.com/web/srv-dbsuubff3r2c73bf3s70

Set secrets in Render → Environment (never commit secrets):
- `OPENAI_API_KEY` (required for script generation)
- `OPENAI_MODEL` (optional; defaults to `gpt-4.1-mini`)
- `HEYGEN_API_KEY`, `VIDIQ_API_KEY` (integration work)
- `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, `YOUTUBE_REFRESH_TOKEN` (OAuth/upload work)

## API
- `GET /` service info
- `GET /health` health check
- `GET /pipeline/status` credential readiness and stage status
- `POST /pipeline/script` JSON body: `{"topic":"...","language":"both","duration_seconds":45}`

Example:
```bash
curl -X POST https://shorts-revenue-ai.onrender.com/pipeline/script \
  -H "Content-Type: application/json" \
  -d '{"topic":"知らないと損するスマホ設定","language":"both","duration_seconds":45}'
```

## Planned workflow
vidIQ research → OpenAI topic/script → HeyGen video → automated QA → human approval → YouTube upload → analytics → iteration.

**Safety:** no video credits are spent and no public upload happens merely by checking status. Review generated scripts/videos and approve publishing first.
