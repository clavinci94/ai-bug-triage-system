# 🤖 AI Bug Triage System

Dieses Projekt ist ein kleiner Prototyp, den ich gebaut habe, um zu zeigen, wie man mit **FastAPI** und etwas **Machine Learning** automatisch Software-Issues klassifizieren kann.  
Die Idee ist simpel: neue Tickets (z. B. von GitHub) kommen rein, und ein Modell schlägt vor, ob es sich um einen Bug, ein Feature, ein Dokumentationsproblem oder eine Verbesserung handelt.  
So spart man Zeit beim manuellen Einsortieren und hat eine einheitlichere Struktur.

---

## Warum „Bug Triage“?

Wer schon mal an einem Open-Source-Projekt oder in einem Entwicklungsteam gearbeitet hat, kennt das Problem:  
Es kommen jede Menge Issues rein – manche sind echte Bugs, manche nur Vorschläge, andere wieder Dokumentationsfehler.  
Das manuell zu sortieren ist mühsam und kostet Zeit.  

Mein Ziel war es, diesen Prozess **teilweise zu automatisieren**:  
- Neue Issues importieren (z. B. direkt von GitHub).  
- Automatisch eine Kategorie vorschlagen.  
- Das Modell kann immer wieder neu trainiert werden, sobald es mehr Daten gibt.  

---

## Features

- **/health** → einfacher Check, ob die API läuft  
- **/issues/import** → Issues aus einem GitHub-Repo holen (z. B. `tiangolo/fastapi`)  
- **/issues/classify** → neues Issue klassifizieren lassen  
- **/issues/classify?save=true** → das Issue gleichzeitig ins Dataset aufnehmen  
- **/issues/dataset** → aktuellen Datensatz ansehen (`issues.csv`)  
- **/issues/retrain** → Modell neu trainieren  

Die API ist mit Swagger dokumentiert und kann direkt im Browser unter `/docs` ausprobiert werden.

---

## Projektstruktur

```text
ai-bug-triage-system/
├── backend/
│   └── core/
│       ├── main.py            # Einstiegspunkt (FastAPI App)
│       ├── config.py          # Einstellungen (env Variablen)
│       ├── models/
│       │   └── schemas.py     # Pydantic Schemas
│       ├── routes/
│       │   └── issues.py      # API Endpunkte
│       └── services/
│           ├── github.py      # Import von GitHub Issues
│           └── classifier.py  # Klassifikations-Logik (ML)
├── data/
│   └── issues.csv             # Trainingsdaten
├── requirements.txt
└── README.md


## Installation & Start

Voraussetzung: Python 3.10+  

```bash
git clone <REPO_URL>
cd ai-bug-triage-system

python -m venv .venv
source .venv/bin/activate   # macOS/Linux
# .venv\Scripts\activate    # Windows

pip install -r requirements.txt


Falls man private GitHub-Repos importieren möchte, legt man eine .env Datei an mit:
GITHUB_TOKEN=ghp_...mein_token...
Starten des Servers:
python -m uvicorn backend.core.main:app --reload
Dann im Browser öffnen:
👉 http://127.0.0.1:8000/docs

Beispiel-Requests
Klassifizieren
curl -X POST "http://127.0.0.1:8000/issues/classify" \
  -H "Content-Type: application/json" \
  -d '{
        "title": "App crashes on upload",
        "body": "Uploading a PDF freezes the app and it crashes."
      }'
Antwort (Beispiel):
{
  "category": "bug",
  "confidence": 0.82,
  "rationale": "NaiveBayes auf issues.csv"
}
Machine Learning
Aktuell steckt hinter der Klassifizierung ein recht einfaches Modell:
Texte werden mit TF-IDF in Vektoren umgewandelt
Klassifikation mit einem Naive Bayes Modell
Trainingsdaten liegen in issues.csv
Das Schöne: wenn neue Daten reinkommen, kann das Modell direkt per API neu trainiert werden.
Später könnte man hier stärkere Modelle einsetzen (z. B. BERT oder Sentence Transformers), aber für den ersten Prototyp reicht das völlig.

Roadmap
Mehr Trainingsdaten sammeln
Modell vergleichen mit moderneren Ansätzen (Transformers)
Dataset-Upload über API ermöglichen
Integration mit externen Tools (z. B. JIRA, Slack)
Docker-Setup + CI/CD

