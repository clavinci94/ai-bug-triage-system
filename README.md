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
```

- Voraussetzung: Python 3.10+  
- GitHub Token (falls private Repos importiert werden sollen)

## Setup
```
# Repository klonen
git clone <REPO_URL>
cd ai-bug-triage-system

# Virtuelle Umgebung erstellen & aktivieren
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
# .venv\Scripts\activate    # Windows

# Dependencies installieren
pip install -r requirements.txt
```

## .env Datei
Falls ein privates GitHub Repo genutzt werden soll:
GITHUB_TOKEN=ghp_abc123meinToken
Starten des Servers:
python -m uvicorn backend.core.main:app --reload
Dann im Browser öffnen:
👉 http://127.0.0.1:8000/docs

## Starten
python -m uvicorn backend.core.main:app --reload

Die API ist dann erreichbar unter:
http://127.0.0.1:8000/docs

## Beispiel-Requests

### Alle Anfragen an die API folgen der gleichen Struktur:
```
{
    "title": "Kurze Zusammenfassung des Issues",
    "body": "Detaillierte Beschreibung des Issues."
}
```

### Klassifikation: Bug
```

  {
    "title": "New crash when exporting PDF",
    "body": "The app crashes immediately when exporting PDF."
  }
```

### Beispiel Antwort
```
{
  "category": "bug",
  "confidence": 0.91,
  "rationale": "ML-NaiveBayes auf Mini-Dataset"
}
```
### Beispiel 2

```
{
    "title": "UI freezes on logout",
    "body": "The application becomes unresponsive for 10 seconds after logging out."
}
```
### Beispiel Antwort
```
{
  "category": "bug",
  "confidence": 0.5017993320213663,
  "rationale": "ML-NaiveBayes auf issues.csv"
}
```
### Beispiel Feature
```
{
    "title": "Add dark mode",
    "body": "It would be great to have a dark mode for the UI."
}
```

## Machine Learning
Aktuell steckt hinter der Klassifizierung ein recht einfaches Modell:
Texte werden mit TF-IDF in Vektoren umgewandelt
Klassifikation mit einem Naive Bayes Modell
Trainingsdaten liegen in issues.csv
Das Schöne: wenn neue Daten reinkommen, kann das Modell direkt per API neu trainiert werden.
Später könnte man hier stärkere Modelle einsetzen (z. B. BERT oder Sentence Transformers), aber für den ersten Prototyp reicht das völlig.

## Fazit
Das Projekt hat mir geholfen, Backend-Entwicklung und Machine Learning in einem praktischen Kontext zu verbinden.
Besonders spannend war für mich der Workflow von Datenimport → Modelltraining → API-Endpunkt → Dokumentation in Swagger.
Es ist ein Lernprojekt, aber mit echter Relevanz für den Alltag von Entwicklern, die große Open-Source-Repos managen.







