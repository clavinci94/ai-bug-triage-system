from fastapi import APIRouter, Query
from typing import List

from backend.core.models.schemas import IssueIn, IssueOut, ClassificationOut
from backend.core.services.github import fetch_issues
from backend.core.services.classifier import predict, train_model

router = APIRouter(prefix="/issues", tags=["issues"])


@router.get("/import", response_model=List[IssueOut])
async def import_issues(
    owner: str = Query(..., example="tiangolo"),
    repo: str = Query(..., example="fastapi"),
    state: str = Query("open", regex="^(open|closed|all)$")
):
    """Importiert Issues aus GitHub (öffentlich)."""
    return await fetch_issues(owner, repo, state)


@router.post("/classify", response_model=ClassificationOut)
def classify_issue(issue: IssueIn, save: bool = False):
    """
    Klassifiziert ein einzelnes Issue mit ML.
    Optional: Speichert das Issue mit vorgeschlagenem Label in issues.csv.
    """
    return predict(issue, save=save)


@router.post("/retrain")
def retrain():
    """Trainiert das Modell neu mit issues.csv."""
    model = train_model()
    if model is None:
        return {"status": "failed", "reason": "Keine Trainingsdaten gefunden"}
    return {"status": "ok", "message": "Modell neu trainiert"}

    model = train_model()
    if model is None:
        return {"status": "failed", "reason": "Keine Trainingsdaten gefunden"}
    return {"status": "ok", "message": "Modell neu trainiert"}

@router.post("/classify", response_model=ClassificationOut)
def classify_issue(issue: IssueIn):
    """
    Klassifiziert ein einzelnes Issue mit ML (Naive Bayes).
    """
    return predict(issue)

import pandas as pd
from backend.core.services.classifier import CSV_PATH


@router.get("/dataset")
def get_dataset(limit: int = 20):
    """
    Gibt die gespeicherten Trainingsdaten aus issues.csv zurück (default: 20 Zeilen).
    """
    if not CSV_PATH.exists():
        return {"status": "failed", "reason": "issues.csv nicht gefunden"}

    df = pd.read_csv(CSV_PATH)
    return df.head(limit).to_dict(orient="records")
