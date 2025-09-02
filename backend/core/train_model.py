import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import joblib

# CSV laden
data = pd.read_csv("issues.csv")

# Features = title + body zusammenfügen
X = data["title"] + " " + data["body"]
y = data["label"]

# ML-Pipeline: TF-IDF + Naive Bayes
model = Pipeline([
    ("tfidf", TfidfVectorizer()),
    ("clf", MultinomialNB())
])

# Trainieren
model.fit(X, y)

# Modell speichern
joblib.dump(model, "backend/core/model.pkl")

print("✅ Training abgeschlossen – Modell gespeichert unter backend/core/model.pkl")
