import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from pathlib import Path

from backend.core.models.schemas import IssueIn, ClassificationOut

CSV_PATH = Path("issues.csv")

# Modell als globaler Cache
_model = None


def train_model():
    """
    Trainiert ein Naive Bayes Modell basierend auf issues.csv.
    """
    global _model

    if not CSV_PATH.exists():
        _model = None
        return None

    df = pd.read_csv(CSV_PATH)

    if "label" not in df.columns or df["label"].isnull().all():
        _model = None
        return None

    X = (df["title"].fillna("") + " " + df["body"].fillna("")).tolist()
    y = df["label"].fillna("unlabeled").tolist()

    model = make_pipeline(TfidfVectorizer(), MultinomialNB())
    model.fit(X, y)

    _model = model
    return model


def predict(issue: IssueIn, save: bool = False) -> ClassificationOut:
    """
    Klassifiziert ein Issue und speichert es optional in issues.csv.
    """
    global _model
    if _model is None:
        _model = train_model()

    if _model is None:
        return ClassificationOut(
            category="unknown",
            confidence=0.0,
            rationale="Kein Trainingsdatensatz vorhanden."
        )

    text = f"{issue.title} {issue.body}"
    proba = _model.predict_proba([text])[0]
    label = _model.classes_[proba.argmax()]
    confidence = float(proba.max())

    result = ClassificationOut(
        category=label,
        confidence=confidence,
        rationale="ML-NaiveBayes auf issues.csv"
    )

    if save:
        save_issue(issue, label)

    return result


def save_issue(issue: IssueIn, label: str):
    """
    Speichert ein neues Issue in issues.csv mit vorgeschlagenem Label.
    """
    new_data = pd.DataFrame([{
        "title": issue.title,
        "body": issue.body,
        "label": label
    }])

    if CSV_PATH.exists():
        df = pd.read_csv(CSV_PATH)
        df = pd.concat([df, new_data], ignore_index=True)
    else:
        df = new_data

    df.to_csv(CSV_PATH, index=False)
