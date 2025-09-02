from fastapi import FastAPI
from backend.core.routes.issues import router as issues_router
from backend.core.config import get_settings

app = FastAPI(title="AI Bug Triage System", version="0.1.0")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/config-check")
def config_check():
    settings = get_settings()
    # Nur prüfen, ob der Token vorhanden ist (True/False)
    return {"GITHUB_TOKEN_loaded": bool(settings.GITHUB_TOKEN)}

# Router registrieren
app.include_router(issues_router)



