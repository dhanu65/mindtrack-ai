import pandas as pd
import joblib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Load dataset
data = pd.read_csv("data/emotion_dataset.csv")

X = data["text"]
y = data["emotion"]

# Convert text to vectors
vectorizer = TfidfVectorizer()
X_vec = vectorizer.fit_transform(X)

# Train model
model = LogisticRegression()
model.fit(X_vec, y)

# Save model and vectorizer
joblib.dump(model, "models/emotion_model.pkl")
joblib.dump(vectorizer, "models/vectorizer.pkl")

print("Model trained and saved!")
